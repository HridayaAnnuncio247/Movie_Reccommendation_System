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

		
		"""#check if email entered by user hasn't already been used before. Cuz, 1 email should have only 1 account
		if db.users.find_one({"email":user['email']}):
			return jsonify({"error":"Email address already in use"}), 400 #first we repond with a dictionary where error is the ey, 400 indicates that it failed.

		#encrypt the password
		user['password'] = pbkdf2_sha256.encrypt(user['password'])
		
		if db.users.insert_one(user): # success of: the collection name is users
			return self.start_session(user)"""



