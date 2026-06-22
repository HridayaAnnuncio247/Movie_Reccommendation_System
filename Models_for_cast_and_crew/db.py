import pymongo
client = pymongo.MongoClient("mongodb+srv://hridaya_annuncio:hridaya_annuncio@moviereccommendationsys.idyz9nm.mongodb.net/")

#database
#client = pymongo.MongoClient('localhost', 27017) #arguments: host name, port
db = client.movie_reccommendation_system #created a database called user_login_system using the mongodb client instance



