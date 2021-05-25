from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os


projectdir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(projectdir,"mydatabase.db"))


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] =  database_file
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)


@app.route('/')
def index():
    expenses = Expense.query.all()
    return render_template('add.html', expenses=expenses)

@app.route('/submitexpense', methods=['POST'])
def submitexpense():

    name = request.form['name']
    date = request.form['date']
    price = request.form['price']
    category = request.form['category']
    expense = Expense(name=name, date=date, price=price, category=category)
    db.session.add(expense)
    db.session.commit()

    expenses = Expense.query.all()
    return redirect(url_for('index'), expenses=expenses)




if __name__ == "__main__":
    app.run(debug=True)