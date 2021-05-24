from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os


# take the current file path as directory path for out database file path
project_dir = os.path.dirname(os.path.abspath(__file__)) 
database_file = "sqlite:///{}".format(os.path.join(project_dir,"mydatabase.db"))


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


class Book(db.Model):

    name = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    author = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Integer, nullable=False)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile/<user>')
def profile(user):
    return render_template('profile.html', user=user, isActive = True)

@app.route('/admin')
def admin():
    return "<h1> Welcome Admin</h1>"

@app.route('/user/<user>/')
def user(user):
    return "<h1> Welcome %s </h1>" %user

@app.route('/welcome/<name>/')
def welcome(name):

    if name == 'admin':
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('user', user=name))

@app.route('/books')
def book():

    books = Book.query.all()
    return render_template('books.html', books=books)

@app.route('/addbook/')
def addBook():

    return render_template('addbook.html')

@app.route('/submitbook', methods=['POST'])
def submitBook():
    name = request.form['title']
    author = request.form['author']
    price = request.form['price']

    book = Book(name=name, author=author, price=price)
    db.session.add(book)
    db.session.commit()

    return redirect(url_for('book'))

@app.route('/updatebooks')
def updateBooks():
    books = Book.query.all()
    return render_template('updatebooks.html', books=books)


@app.route('/update', methods=['POST'])
def updateBook():
    book = Book.query.filter_by(name=request.form['oldname']).first()

    old_name = book.name
    old_author = book.author
    old_price = book.price

    new_name = request.form['newname']
    new_author = request.form['newauthor']
    new_price = request.form['newprice']

    if new_name == "":
        book.name = old_name
    else:
        book.name = new_name
    
    if new_author == "":
        book.author = old_author
    else:
        book.author = new_author

    if new_price == "":
        book.price = old_price
    else:
        book.price = new_price
    
    db.session.commit()

    return redirect(url_for('book'))


@app.route('/delete', methods=['POST'])
def delete():

    book = Book.query.filter_by(name=request.form['name']).first()

    db.session.delete(book)
    db.session.commit()

    return redirect(url_for('book'))
    
    








if __name__ == "__main__":
    app.run(debug=True)

