import requests
import time
API_KEY = "96e28253d91e3dfe2b7e5a61c83fc998"
#url = f"https://api.themoviedb.org/3/movie/001?api_key={API_KEY}"
"""
for pg in range(1, 21):
	url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&page=" + str(pg)
	response = requests.get(url)
	data = response.json()
	#print(data)
	#print(type(data))
	
	for i in data:
		print(i, data[i])
	for i in data["results"]:
		print(i["title"])
	time.sleep(2)
	"""
#bollywood titles
x = 1
for year in range(2025, 2027):
	for page in range(1, 5):
		url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_original_language=hi&primary_release_year={year}&sort_by=popularity.desc&page={page}&append_to_response=credits"
		response = requests.get(url)
		data = response.json()

		for i in data["results"]:
			print(i)
			break
			print(i["title"])
			print(i.keys())
		time.sleep(2)
		break
	break
"""
a = pd.DataFrame([[6, 'William', 5532, 1, 'UAE']],
                       columns=['ID', 'NAME', 'RANK', 'ARTICLE', 'COUNTRY'])
a.to_csv('event.csv', mode='a', index=False, header=False)"""