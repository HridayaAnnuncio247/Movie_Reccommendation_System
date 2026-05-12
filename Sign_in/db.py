import pymongo

#database
client = pymongo.MongoClient('localhost', 27017) #arguments: host name, port
db = client.movie_reccommendation_system #created a database called user_login_system using the mongodb client instance
