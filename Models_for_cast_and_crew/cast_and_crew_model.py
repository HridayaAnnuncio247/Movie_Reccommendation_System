from db import db
from gensim.models import Word2Vec

collection = db["movies"]
dataset = []
for row in collection.find({}, {"Cast": 1, "Director": 1, "Writer":1, "Music": 1}): 
	all = []
	c = row.get("Cast")
	d = row.get("Director")
	w = row.get("Writer")
	m = row.get("Music")

	if c:
		if "Kareena Kapoor Khan" in c:
			c.remove("Kareena Kapoor Khan")
			c.append("Kareena Kapoor")
		all += c
	if d:
		all += d
	if w:
		all += w
	if m:
		all += m
	dataset.append(all)
#print(dataset)

#training
for i in [10, 16, 24, 32]:
	model = Word2Vec(
	    sentences=dataset,
	    vector_size=i,
	    window=5, #look at 5 neighbouring items 
	    min_count=6, #ignore cast names etc that occur <6 times
	    workers=8, #cpu threads use for training in parallel. Make it = number of core the machine has. affects speed
	    epochs=60
	)
	model.save("castCrew_word2vec"+ str(i)+".model")

	
	#model.wv is like a dictionary. basically a look up table
	similar = model.wv.most_similar("Karan Johar", topn=5)
	print(i, similar)
