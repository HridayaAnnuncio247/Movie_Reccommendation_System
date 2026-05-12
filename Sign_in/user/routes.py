#all routes related to the user at every link, which function should work/ what should happen

from flask import Flask
from app import app #from app.py import the app flask objct that we created
from user.models import User # from user folder, models file, import the User class

@app.route('/user/signup/', methods=['POST']) # GET asks the browser to give it something., POST is sending something to the backend
def signup():

	return User().signup() #creates an instance of User

@app.route('/user/signout/') # GET asks the browser to give it something., POST is sending something to the backend
def signout():
	return User().signout() #creates an instance of User

@app.route('/user/login/', methods=['POST'])
def login():
	return User().login()