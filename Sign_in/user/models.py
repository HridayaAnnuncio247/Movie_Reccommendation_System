from flask import Flask, jsonify, request,session, redirect
from passlib.hash import pbkdf2_sha256
from db import db
import numpy as np
import uuid
import random

class User:

	def start_session(self, user):
		del user['password'] #deleting password before displaying on dashboard
		session['logged_in'] = True
		session['user'] = user
		return jsonify(user)

	def signup(self):

		#object to represent user:
		user = {
		"_id": uuid.uuid4().hex,  #mongodb uses _id as the ey for ids. thus using underscore
		"name":request.form.get('name'),
		"email":request.form.get('email'),
		"password":request.form.get('password')
		}

		
		#check if email entered by user hasn't already been used before. Cuz, 1 email should have only 1 account
		if db.users.find_one({"email":user['email']}):
			return jsonify({"error":"Email address already in use"}), 400 #first we repond with a dictionary where error is the ey, 400 indicates that it failed.

		#encrypt the password
		user['password'] = pbkdf2_sha256.encrypt(user['password'])
		
		if db.users.insert_one(user): # success of: the collection name is users
			return self.start_session(user)

		return jsonify({"error":"Signup error"}), 400 
		#we want usr info to come in json format, 200 is the status code that indicates a success
	
	def signout(self):
		session.clear()
		return redirect("/")

	def login(self):
		user = db.users.find_one({"email": request.form.get('email')})
		if user: 
			if pbkdf2_sha256.verify(request.form.get('password'), user['password']):
				return self.start_session(user)
			return jsonify({"error": "Invalid Password"}), 401
		
		return jsonify({"error": "Invalid email"}), 401


	def preferences(self):
		"""
		In this function we retrieve the movie ids that the user selected on creating their account. 
		The embeddings of those movies are used to create the user embedding by averaging.
		"""
		user_embedding = None
		movie_ids = list(set(request.get_json()["selected_movies"]))
		print("mvie_ids in preferences", movie_ids)
		for i in movie_ids:
			movie = db.movies.find_one({"_id":i})
			if not movie:
				continue
			embedding = np.array(movie.get("embedding"))
			if user_embedding is not None:
				user_embedding += embedding
			else:
				user_embedding = embedding
		if user_embedding is None:
			return jsonify({"error": "No valid movie id"}), 401


		user_embedding = user_embedding/len(movie_ids)

		user_id = session['user']["_id"]
		session['user']["user_embedding"] = user_embedding.tolist()
		session['user']["movies"] = movie_ids
		session['user']["update"] = True # indicates if the RL algo should learn news recs to add to the dashboard
		movie_ids = self.rewards()
		session['user']["movies"] = movie_ids
		session.modified = True

		if not db.users.update_one({"_id":user_id}, {"$set": {"user_embedding":user_embedding.tolist(), 
															  "movies": movie_ids,
															  "update": True}}):
			return  jsonify({"error": "User embedding could not be added to the db"}), 401

		return  jsonify({"success": "User embedding created"}), 200


	def rewards(self, p_new = 0.1, e = 0.1, k = 40):
		"""
		float pnew: between 0 and 1. Probability of selecting a non top K reward movie.
		float e: represents epsilon in epsilon greedy. it is the probability that from top K movies the highest reward movie is not chosen.
		int k: number of top k reward movies to choose.
		"""
		print("in rewards")
		movie_ids = session["user"]["movies"]
		if not session['user']["update"]:
			print("no updating")
			return movie_ids

		if "disliked" not in session["user"]:
			disliked = []
		else:
			disliked = session["user"]["disliked"]

		user_embedding = session["user"]["user_embedding"]
		print("user_embedding", user_embedding)
		movie_rewards_old = db.users.find_one({"_id": session["user"]["_id"]}).get("rewards")
		if not movie_rewards_old:
			movie_rewards_old = {}
		
		id_rewards = []
		user_norm = np.array(user_embedding)/ np.linalg.norm(user_embedding)

		for movie in db.movies.find():

			if not movie:
				continue
			i = movie.get("_id")
			movie_embedding = np.array(movie.get("embedding"))
			#movie_embeddings.append(user_embedding + movie_embedding.tolist())
			if i in movie_rewards_old:
				reward = movie_rewards_old[i]
			else:
				movie_norm = movie_embedding / np.linalg.norm(movie_embedding)
				reward = user_norm@movie_norm

			id_rewards.append([i,reward])

		sorted_rewards = sorted(id_rewards, key = lambda x: x[1], reverse = True)

		top_k = sorted_rewards[:k]
		rest = sorted_rewards[k:]

		recommend = [] #movie ids to be recommended on the dashboard
		cnt = 0
		while True: #for i in range(30):
			if cnt == 35 or (not top_k and not rest):
				break
			random_new = random.random()
			if random_new < p_new:
				random_greedy = random.random()
				if random_greedy < e - (e/k):
					new = random.choice(rest[1:])
					if new[0] in disliked:
						rest.remove(new)
						continue
					print("new choice", new)
					recommend.append(new[0])
					rest.remove(new)
					cnt+=1
				else:
					if rest[0][0] in disliked:
						rest.pop(0)
						continue
					recommend.append(rest[0][0])
					rest.pop(0)
					cnt+=1
			else:
				random_greedy = random.random()
				if random_greedy < e - (e/k):
					new = random.choice(top_k[1:])
					if new[0] in disliked:
						top_k.remove(new)
						continue
					print("old choice - random", new)
					recommend.append(new[0])
					top_k.remove(new)
					cnt+=1
				else:
					if top_k:
						if top_k[0][0] in disliked:
							top_k.pop(0)
							continue
						print("old choice - best", top_k[0][0])
						recommend.append(top_k[0][0])
						top_k.pop(0)
						cnt+=1
			
		print("recommended list",len(recommend), recommend)
		session['user']["update"] = False
		return recommend

	def update_preferences(self, a = 0.05):
		"""
		a: learning rate or alpha
		"""
	
		movie_ids = list(request.get_json()["movie_ids"])
		rewards = list(request.get_json()["rewards"])

		all_movies = session["user"]["movies"]
		all_embeddings = []
		user_embedding = session["user"]["user_embedding"]
		predicted_rewards = []

		for i in all_movies:
			if i not in movie_ids:
				movie_ids.append(i)
				rewards.append(0)
		for i in movie_ids:
			movie_embedding = db.movies.find_one({"_id": i}).get("embedding")
			all_embeddings.append(user_embedding + movie_embedding)

		print("movie ids:", movie_ids)
		print("rewards:", rewards)
				
		
		X = np.array(all_embeddings)
		Y = np.array(rewards)
		if "disliked" not in session["user"]:
			disliked = []
		else:
			disliked = session["user"]["disliked"]

		print("X shape:", X.shape)
		print("Y shape:", Y.shape)
		user = db.users.find_one({"_id":session["user"]["_id"]})
		cov = user.get("covariance")
		if not cov:
			cov = X.T @ X 
			rewards_X = X.T@Y
		else:
			cov = np.array(cov)
			rewards_X = np.array(user.get("rewards_X"))
			for i in range(len(all_embeddings)):
				x = X[i]
				r = rewards[i]
				if r == -1:
					disliked.append(movie_ids[i])
				cov += np.outer(x,x)
				rewards_X += r*x

		#ucb values
		cov_inverse = np.linalg.inv(cov + np.eye(cov.shape[0]) * 1e-5) # adding a bit of values to make sure the covariance matrix is not singular
		predicted_y = cov_inverse@rewards_X
		ucb = []
		for i in range(len(all_movies)):
			print("in ucb loop")
			ucb_i = predicted_y@X[i] + a*((X[i]@cov_inverse@X[i].T)**0.5)
			ucb.append(ucb_i)
		new_rewards_ucb = {}
		for i in range(len(all_movies)):
			print("in ucb dictionary loop")
			new_rewards_ucb[movie_ids[i]] = ucb[i]

		
		#session["user"]["covariance"] = cov.tolist()
		#session["user"]["rewards_X"] = rewards_X.tolist()
		session["user"]["rewards"] = new_rewards_ucb
		print("edited rewards:", new_rewards_ucb)

		session['user']["update"] = True
		movie_ids = self.rewards()
		print("rewards function done", movie_ids)
		session["user"]["movies"] = movie_ids
		session["user"]["disliked"] = disliked
		print("session movies", session["user"]["movies"])
		session.modified = True 		


		if not db.users.update_one({"_id":session["user"]["_id"]}, {"$set": {"rewards":new_rewards_ucb, "covariance": cov.tolist(), "rewards_X":rewards_X.tolist(), "movies":movie_ids, "disliked":disliked}}):
			return  jsonify({"error": "User embedding could not be added to the db"}), 40

		return  jsonify({"success": "User embedding created"}), 200


	

















		