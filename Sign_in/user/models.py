from flask import Flask, jsonify, request,session, redirect
from passlib.hash import pbkdf2_sha256
from db import db
import numpy as np
import uuid

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
		session.modified = True
		if not db.users.update_one({"_id":user_id}, {"$set": {"user_embedding":user_embedding.tolist(), 
															  "movies": movie_ids,
															  "update": True}}):
			return  jsonify({"error": "User embedding could not be added to the db"}), 401

		return  jsonify({"success": "User embedding created"}), 200


	def recommend(self):

		movie_ids = session["user"]["movies"]
		if not session['user']["update"]:
			return movie_ids

		user_embedding = session["user"]["user_embedding"]
		movie_embeddings = []
		rewards = []

		for i in movie_ids:
			movie = db.movies.find_one({"_id":i})
			if not movie:
				continue
			movie_embedding = np.array(movie.get("embedding"))
			movie_embeddings.append(user_embedding + movie_embedding.tolist())
			reward = movie.get("reward")
			if not reward:
				user_norm = user_embedding / np.linalg.norm(user_embedding)
				movie_norm = movie_embedding / np.linalg.norm(movie_embedding)
				reward = user_norm@movie_norm

			rewards.append(reward)

		







		