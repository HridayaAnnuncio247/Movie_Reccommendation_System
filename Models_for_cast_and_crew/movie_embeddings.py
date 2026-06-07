from gensim.models import Word2Vec
from db import db
import numpy as np


def get_word2vec_embedding(model, data):
	vec = np.zeros(16)
	cnt = 0
	if data:
		for i in data:
			if i in model.wv:
				vec += np.array(model.wv[i])
				cnt += 1
		if cnt>0:
			vec = vec/cnt
	#print(vec)
	return vec


model = Word2Vec.load("castCrew_word2vec16.model")

columns = ["_id", "adult", "language_en", "language_hi", "release_year", "release_month_sin", "release_month_cos", "popularity","vote_average","vote_count" ]

genres = [28,12, 16, 35, 80, 99, 18, 10751, 14, 36, 27, 10402, 9648, 10749, 878, 10770, 53, 10752, 37]
for i in genres:
	columns.append("genre_" + str(i))

for i in range(16):
	columns.append("cast_" + str(i)) 
for i in range(16):
	columns.append("director_" + str(i)) 
for i in range(16):
	columns.append("writer_" + str(i))
for i in range(16):
	columns.append("musician_" + str(i))




for movie in db.movies.find():
	movie_embedding = []

	movie_embedding.append(movie.get("_id"))
	movie_embedding.append(movie.get("adult"))

	lang = movie.get("original_language")
	if lang == "en":
		movie_embedding += [1,0]
	elif lang == "hi":
		movie_embedding += [0,1]
	
	release =  movie.get("release_date")
	movie_embedding.append(int(release[:4]))
	month_angle = 2 * np.pi * int(release[5:7])/12

	movie_embedding.append(np.sin(month_angle))
	movie_embedding.append(np.cos(month_angle))

	movie_embedding.append(movie.get("popularity"))
	movie_embedding.append(movie.get("vote_average"))
	movie_embedding.append(movie.get("vote_count"))

	movie_g = movie.get("genre_ids")

	for i in genres:
		if i in movie_g:
			movie_embedding.append(1)
		else:
			movie_embedding.append(0)


	movie_embedding += list(get_word2vec_embedding(model, movie.get("Cast")))
	

	movie_embedding += list(get_word2vec_embedding(model,movie.get("Director")))
	
	movie_embedding += list(get_word2vec_embedding(model,movie.get("Writer")))
	
	movie_embedding += list(get_word2vec_embedding(model,movie.get("Music")))

	updates = {"embedding":movie_embedding}
	
	db.movies.update_one({"_id":movie["_id"]}, {"$set": updates})
	








