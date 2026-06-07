from db import db
from gensim.models import Word2Vec

collection = db["movies"]
cast = []
director = []
writer = []
music = []
all = []
for row in collection.find({}, {"Cast": 1, "Director": 1, "Writer":1, "Music": 1}): 

	c = row.get("Cast")
	d = row.get("Director")
	w = row.get("Writer")
	m = row.get("Music")

	if c:
		all += c
	if d:
		all += d
	if w:
		all += w
	if m:
		all += m


#training
for i in [10, 16, 24, 32]
	model_cast = Word2Vec(
	    sentences=all,
	    vector_size=i,
	    window=5, #look at 5 neighbouring items 
	    min_count=2, #ignore cast names etc that occur <2 times
	    workers=8, #cpu threads use for training in parallel. Make it = number of core the machine has. affects speed
	    epochs=20
	)
	model.save("cast_word2vec"+ str(i)+".model")

	#model = Word2Vec.load("cast_word2vec.model")
	#model.wv is like a dictionary. basically a look up table
	similar = model.wv.most_similar("Christopher Nolan", topn=5)
	print(i, similar)
