from flask import Flask, jsonify, request,session, redirect
from passlib.hash import pbkdf2_sha256
from db import db
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

