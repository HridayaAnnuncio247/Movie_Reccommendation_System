import requests
from bs4 import BeautifulSoup

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

for row in tables.find_all("tr"):
    header = row.find("th")
    
    if header and "Starring" in header.text:
    	value = row.find("td")
    	for a in value.find_all("a"):
    		cast += a
    	break
      

print(cast)