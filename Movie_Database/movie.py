import requests
import time
from db import db
import uuid

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
		for row in collection.find({}, {"title": 1}): 

			movie = row.get("title")
			if movie:
				updates = self.call_wiki(movie)
				collection.update_one({"_id":row["id"]}, {"$set": updates})



	def call_wiki(self, movie):
		"""
		string movie: Name of the movie. The spaces will be replaced with "_" to create the wiki link.
		"""

		movie_link = movie.replace(" ", "_")

		url = "https://en.wikipedia.org/wiki/3_Idiots"
		headers = {
		    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
		response = requests.get(url, headers = headers) # request is sent to the url
		#response.text contains the entire HTML content as a string
		soup = BeautifulSoup(response.text, "html.parser")
		#html.parser is Python'e inbuilt HTML parser (can use other parsers lie lxml and html5lib.)
		#soup.prettify() prints well formatted HTML
		#print(soup.prettify())
		tables = soup.find("table", class_ = "infobox vevent")
		cast = []
		cnt = 0
		Director = []
		Writer = []
		Musician = []


		for row in tables.find_all("tr"):
		    header = row.find("th")

		    if not header:
		    	continue
		    
		    if "Starring" in header.text:
		    	value = row.find("td")
		    	for a in value.find_all("a"):
		    		cast += a
		    	cnt += 1
		    elif "Directed" in header.text:
		    	value = row.find("td")
		    	for a in value.find_all("a"):
		    		Director += a
		    	cnt += 1
		    elif "Written" in header.text:
		    	value = row.find("td")
		    	for a in value.find_all("a"):
		    		Writer += a
		    	cnt += 1
		    elif "Music" in header.text:
		    	value = row.find("td")
		    	for a in value.find_all("a"):
		    		Musician += a
		    	cnt += 1

		    if cnt == 4:
		    	break

		return {"Cast": cast, "Director": Director, "Writer":Writer, "Music": Musician}



