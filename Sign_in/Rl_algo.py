from flask import Flask, jsonify, request,session, redirect
import numpy as np
from db import db



movie_ids = session["user"]["movies"]
user_embedding = session["user"]["user_embedding"]
movie_embeddings = []

for i in movie_ids:
	movie = db.movies.find_one({"_id":i})
	if not movie:
		continue
	movie_embeddings.append(user_embedding + np.array(movie.get("embedding")).tolist())

