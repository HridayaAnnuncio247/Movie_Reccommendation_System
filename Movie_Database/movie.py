import requests
import time
from db import db
import uuid
import requests
from bs4 import BeautifulSoup


class Movie:

	def api_call(self, url, retries=30, backoff=5):
		for attempt in range(retries):
			        try:
			            response = requests.get(url, timeout=10)
			            if response.status_code == 429:
			                wait = int(response.headers.get("Retry-After", backoff))
			                print(f"Rate limited. Waiting {wait}s...")
			                time.sleep(wait)
			                continue
			            response.raise_for_status()
			            return response.json()
			        except requests.exceptions.RequestException as e:
			            print(f"Attempt {attempt+1} failed: {e}")
			            # exponential-ish backoff
			            time.sleep(backoff * (attempt + 1))
		return None

	def add_to_db(self, data):
		return db.movies.insert_one(data)


	def run_api(self, year_range, language, API_KEY):
		"""
		returns a list o
		"""

		for year in range(year_range[0],year_range[1] + 1):
			print(year)
			for page in range(1, 21):
				url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_original_language={language}&primary_release_year={year}&sort_by=popularity.desc&page={page}&append_to_response=credits"
				data = 	self.api_call(url)	
				if not data:
					break
				for movie in data["results"]: 
					movie["_id"] = "M" + uuid.uuid4().hex
					print(movie['title'])
					self.add_to_db(movie)

	def add_cast_and_crew(self, collection_name):
		collection = db[collection_name]

		# {} like select * from table, thus selects all rows. "title":1 says that only extract the field title from every row. THis helps us with not etracting unrequired fields too. If i added "_id":0 then "_id" would be excluded. Currently it is included.
		for row in collection.find({"original_language":"hi"}, {"title": 1, "release_date":1, "original_language":1}): 

			movie = row.get("title")
			year = row.get("release_date")[:4]
			
			language = row.get("original_language")
			if int(year)>2015:
				continue
			if language == "hi":
				lang = "Hindi"
			elif language == "en":
				lang = "English"
			if movie:
				updates = self.call_wiki(movie,year,lang )
				if not updates:
					continue
				collection.update_one({"_id":row["_id"]}, {"$set": updates})
				print(movie)



	def call_wiki(self, movie, year, language):
		"""
		string movie: Name of the movie. The spaces will be replaced with "_" to create the wiki link.
		"""

		movie_name = movie.replace(" ", "_")
		movie_links = [movie_name, movie_name + "_(film)", movie_name+"_("+year+"_film)",movie_name+"_("+year+"_" + language + "_film)" ]
		#print(movie_link)

	
		headers = {
		    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
		x = 0
		for i in movie_links:
			url = "https://en.wikipedia.org/wiki/" + i
			#print(url)
			response = requests.get(url, headers = headers) # request is sent to the url
			#response.text contains the entire HTML content as a string
			soup = BeautifulSoup(response.text, "html.parser")
			#html.parser is Python'e inbuilt HTML parser (can use other parsers lie lxml and html5lib.)
			#soup.prettify() prints well formatted HTML
			#print(soup.prettify())
			tables = soup.find("table", class_ = "infobox vevent")
			if tables:
				x = 1
				break
		if x==0:
			db.movies_without_cast_and_crew.insert_one({"title":movie})
			print("nocast and crew:", movie)
			return None

		cast = []
		cnt = 0
		Director = []
		Writer = []
		Musician = []
		missing = []

		for row in tables.find_all("tr"):
		    header = row.find("th")

		    if not header:
		    	continue

		    header_text = header.get_text(separator=" ").strip()
		    #print(header_text)
		    
		    if "Starring" in header_text or "Cast" in header_text:
		    	value = row.find("td")
		    	cast = self.extract_names(value)
		    	if not cast:
		    		missing.append("cast")
		    	cnt += 1

		    elif "Direct" in header_text:
		    	value = row.find("td")
		    	Director = self.extract_names(value)
		    	if not Director:
		    		missing.append("Director")
		    	cnt += 1

		    elif "Written" in header_text or "Writer" in header_text:
		    	value = row.find("td")
		    	Writer = self.extract_names(value)
		    	if not Writer:
		    		missing.append("Writer")
		    	cnt += 1

		    elif "Music" in header_text:
		    	value = row.find("td")
		    	Musician = self.extract_names(value)
		    	if not Musician:
		    		missing.append("Musician")
		    	cnt += 1

		    if cnt == 4:
		    	break
		if missing:
		   	db.movies_without_specific_things.insert_one({"title":movie, "missing":missing})
		   	print(missing, movie)

		return {"Cast": cast, "Director": Director, "Writer":Writer, "Music": Musician}


	def extract_names(self, value):
		l = []
		if not value:
			return l

		links = value.find_all("a")
		if not links:
			for text in value.stripped_strings:
				l.append(text)
		else:
			for a in links:
				l.append(a.get_text())
		return l

	def movie_embeddings(self):

		columns = ["_id", "adult", "genre_Action_28", "genre_Adventure_12", "genre_Animation_16", "genre_Comedy_35", "genre_Crime_80", "genre_Documentary_99", "genre_Drama_18", "genre_Family_10751", "genre_Fantasy_14", "genre_History_36", "genre_Horror_27", "genre_Music_10402", "genre_Mystery_9648", "genre_Romance_10749", "genre_Science_Fiction_878", "genre_TV_Movie_10770", "genre_Thriller_53", "genre_War_10752", "genre_Western_37", "language_Hindi", "language_English", "popularity", "release_month_sin", "release_month_cos", "release_year", "vote_average", "vote_count"]

	def frequencies(self, collection_name):
		collection = db[collection_name]

		frequencies_cast = {}
		frequencies_director={}
		frequencies_musician={}
		frequencies_writer={}

		frequencies_cast["id"] = "Cast"
		frequencies_director["id"] = "Director"
		frequencies_musician["id"] = "Writer"
		frequencies_writer["id"] = "Music"

		# {} like select * from table, thus selects all rows. "title":1 says that only extract the field title from every row. THis helps us with not etracting unrequired fields too. If i added "_id":0 then "_id" would be excluded. Currently it is included.
		for row in collection.find({}, {"Cast": 1, "Director": 1, "Writer":1, "Music": 1}): 

			cast = row.get("Cast")
			director = row.get("Director")
			Writer = row.get("Writer")
			Music = row.get("Music")
			
			if cast:
				for i in cast:
					if i in frequencies_cast:
						frequencies_cast[i] += 1
					else:
						frequencies_cast[i] = 1

			if director:
				for i in director:
					if i in frequencies_director:
						frequencies_director[i] += 1
					else:
						frequencies_director[i] = 1

			if Music:
				for i in Music:
					if i in frequencies_musician:
						frequencies_musician[i] += 1
					else:
						frequencies_musician[i] = 1
			if Writer:
				for i in Writer:
					if i in frequencies_writer:
						frequencies_writer[i] += 1
					else:
						frequencies_writer[i] = 1


		db.frequencies.insert_one(frequencies_cast)
		db.frequencies.insert_one(frequencies_director)
		db.frequencies.insert_one(frequencies_musician)
		db.frequencies.insert_one(frequencies_writer)
		
		print(len(frequencies_cast))
		#print(frequencies_director)
		#print(frequencies_musician)
		#print(frequencies_writer)

		self.create_tables([frequencies_cast, frequencies_writer, frequencies_musician, frequencies_director])

	def create_tables(self, l):

		for dic in l:
			table_name = dic["id"]

			del dic["id"]

			for j in dic:
				db[table_name].insert_one({"name:": j, "frequency": dic[j]})


