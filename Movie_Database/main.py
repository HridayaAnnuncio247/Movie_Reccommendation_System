from movie import Movie
from db import db
from time import sleep
m = Movie()

year_range = [2000, 2015]#[2016, 2026]

language = "hi"#"en"#"Hindi"

API_KEY = "96e28253d91e3dfe2b7e5a61c83fc998"


m.run_api(year_range, language, API_KEY)
m.add_cast_and_crew("movies")
#m.frequencies("movies")

"""Cast = db.Cast.find().sort({"frequency":-1})
for i in Cast:
	#print(i)
	name = i.get("name:")
	frequency = i.get("frequency")
	#print(frequency, type(frequency))
	if name == "_id":
		continue
	if frequency<5:
		continue
	print(name, frequency)
	"""