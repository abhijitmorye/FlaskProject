# Flask Docs

1. sudo pip install flask

## Create an app.py file

## In app.py file

	
	from flask import Flask
	
	app = Flask(__name__)   
	
	app.run()

	
	
	
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

## POST method and how to access data from POST methods

	# addbook.html


		<form action="/submitbook" method="POST">
		<input type="text" name="title">
		<input type="submit">
		</form>

	# app.py

		@app.route('/addbook')
		def addBook():
			return render_template('addbook.html')



		@app.route('/submitbook', methods=['POST'])
		def sbmitBook():

			name = request.file['title']

			return "Output --> %s" %name


## configuring database in FlaskProject

	1. make sure flask_sqlalchemy and sqlalchemy is installed before


		from flask_sqlalchemy import SQLAlchemy
		import os

		#first create an database under our project directory
		project_dir = os.path.dirname(os.path.abspath(__file__)) <-- take directory path of current file i.e. app.py
		database_file = "sqlite:///{}".format(os.path.join(project_dir, mydatabase.db)) <-- under project directory create Db

		#configure your DB to your app
		app = Flask(__name__)
		app.config["SQLALCHEMY_DATABASE_URI"] = database_file
		db = SQLAlchemy(app)


		#now create Model which represents your Table in Db

		class Book(db.Model):

			name = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
			price = db.Column(db.Integer, nullable=False)

		
	2. To create DB, go to cmd and start python

		>>> from app import db
		>>> db.create_all() <-- this will create mydatabase.db under root project directory


	3. adding an field/object to Table/Model

		@app.route('/submitbook', methods=['POST'])
		def submitBook():

			name = request.form['name']
			price = request.form['price']

			book = Book(name=name, price=price)
			db.session.add(book)
			db.session.commit()

	4. Retrieving all books objects/fields from Model/Table

		books = Book.query.all()

		return render_template('books.html', books=books)

	
	5. For updating an object/field in Model/Table

		@app.route('/update', methods=['POST'])
		def update():

			name = request.form['name']
			price = request.form['price']
			book = Book.query.filter_by(name=name).first()
			book.name = Name
			book.price = new
			db.sesssion.commit()
			return redirect(url_for('books'))

	6. Deleting field/object from Table/Model

		book = Book.query.filter_by(name=request.form['name']).first()
		db.session.delete(book)
		db.session.commit()
		





	

	
