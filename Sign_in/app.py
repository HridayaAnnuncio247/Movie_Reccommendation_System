from flask import Flask, render_template, redirect, session
from functools import wraps
app = Flask(__name__) #an app instance
app.secret_key = b'\xc9\x1fadsT\xbabw\xd1\\\x99\xe8\xb5\n\x8d'#

#Decorators
#wraps is a decorator helper from python's functools module. 
#It copies metadata from the original function f onto your wrapper function
#@wraps(f) uses the @ cuz we're applying wraps as a decorator. It is a cleaner shorthand to writing wrap = wraps(f)(wrap)
# args and kwargs help unpack any number of arguments without knowing them in advance
#args has 1 * and thus unpacks tuples
# KWARGS HAS 2 *s and thus unpacks dicts
def login_required(f): # a function will be passed as an argument to this function. for example dashboard could be passed. A check is done if we want to run it or not
	@wraps(f)
	def wrap (*args, **kwargs):
		if 'logged_in' in session: # if the user is logged in then run the function f
			return f(*args, **kwargs)
		else:#otherwise e redirected to the homepage
			return redirect('/')
	return wrap

#Routesapp has to have a secret key wheneer a session is used
from user import routes # gets all routes in user 

@app.route('/')
def home():
	return render_template("home.html")

@app.route('/setting_up/')
@login_required
def setting_up():
	return render_template("setting_up.html")

@app.route('/dashboard/')
@login_required
def dashboard():
	return render_template("dashboard.html")
