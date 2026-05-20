#all routes related to the user at every link, which function should work/ what should happen

from flask import Flask, jsonify
from app import app #from app.py import the app flask objct that we created
from user.models import User # from user folder, models file, import the User class
from db import db
@app.route('/user/signup/', methods=['POST']) # GET asks the browser to give it something., POST is sending something to the backend
def signup():

	return User().signup() #creates an instance of User

@app.route('/user/signout/') # GET asks the browser to give it something., POST is sending something to the backend
def signout():
	return User().signout() #creates an instance of User

@app.route('/user/settingup/')
def movies():
	collection = db["movies"]
	base_url = "https://image.tmdb.org/t/p/w500"
	movies = list(collection.find({"vote_count": {"$gt": 1000}}, {"title": 1, "poster_path": 1, "vote_average":1, "_id": 0}).sort("vote_average", -1).limit(10))
	return jsonify(movies)

@app.route('/user/login/', methods=['POST'])
def login():
	return User().login()