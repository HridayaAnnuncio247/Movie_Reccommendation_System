#all routes related to the user at every link, which function should work/ what should happen

from flask import Flask, jsonify,request
from app import app #from app.py import the app flask objct that we created
from user.models import User # from user folder, models file, import the User class
from db import db
import sys

genre_dict = {'Action': 28, 'Adventure': 12, 'Animation': 16, 'Comedy': 35, 'Crime': 80, 'Documentary': 99, 'Drama': 18, 'Family': 10751, 'Fantasy': 14, 'History': 36, 'Horror': 27, 'Music': 10402, 'Mystery': 9648, 'Romance': 10749, 'Science Fiction': 878, 'TV Movie': 10770, 'Thriller': 53, 'War': 10752, 'Western': 37}

@app.route('/user/signup/', methods=['POST']) # GET asks the browser to give it something., POST is sending something to the backend
def signup():

	return User().signup() #creates an instance of User

@app.route('/user/signout/') # GET asks the browser to give it something., POST is sending something to the backend
def signout():
	return User().signout() #creates an instance of User

@app.route('/user/settingup/')
def movies():
	genre = request.args.get('genre')
	print(genre, genre_dict[genre])
	sys.stdout.flush()
	collection = db["movies"]
	base_url = "https://image.tmdb.org/t/p/w500"
	movies = list(collection.find({"vote_count": {"$gt": 1000}, "genre_ids": genre_dict[genre]  }, {"title": 1, "poster_path": 1, "vote_average":1, "_id": 0}).sort("vote_average", -1).limit(10))
	return jsonify(movies)

@app.route('/user/login/', methods=['POST'])
def login():
	return User().login()