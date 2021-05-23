# Flask Docs

1. sudo pip install flask

## Create an app.py file

## In app.py file

	
	from flask import Flask
	
	app = Flask(__name__)   
	
	app.run	

	
	
	
##   __name__ if app.py is run directly then __name__ == __main__ but if it is imported then __name__ == app

##	route -- it is used to create route for specific url pattern so whenever an end user types any url this route will match typed url with associated pattern

	
	@app.route('/')
	def index():
	
		return "Hello World"
	
		

## variable -- It is used to  pass dynamic values to url/route and then to function associated with particular route
	
	
	@app.route('/profile/<username>')
	def profile(username):
		return "Hello {}".format(username)
	
	
		
	
	#### Note - for intger values -- @app.route('/profile/<int:id>')
	
## Debug mode - Allows to reflect the changes in the browser during development

	
	app.run(debug=True)
	

## redirecting - redirecting a url to another url 

	

	from flask import Flask, redirect, url_for
	@app.route('/admin/')
	def admin():
		return "Welcome admin"
	

	@app.route('/user/<user>'):
	def user(user):
		return "Welcome %s" %user
	
	@app.route('/welcome/<name>/')
	def welcome(name):
		if name == 'admin':
			return redirect(url_for('admin'))
		else:
			return redirect(url_for('user', user=name))

	

## accessing request data

	
	from flask import request

	@app.route('/')
	def index():
		return "This is request to view request headers <br> %s" %request.headers

	
	

## rendering html tempate in flask

	
	from flask import render_template

	@app.route('/')
	def index():
		return render_template('index.html')

	

## passing values from functions or url  to html pages

	
	from flask import Flask, render render_template

	@app.route('/profile/<name>')
	def profile(name):
		return render_template('profile.html', name=name)

	
	

	
	<h1> Name -- {{name}} <h1>

## Adding an css file in html in flask project

	flask directory/
		|
		|__static/
			 |
			 |__css/
			 	|
				|style.css

	in base  html file

	<link rel="stylesheet" href="{{ url_for('static', filename="css/>style.css") }}">
	

	