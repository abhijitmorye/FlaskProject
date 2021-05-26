from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os


projectdir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(
    os.path.join(projectdir, "mydatabase.db"))


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
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
    return redirect(url_for('index'))


@app.route('/expenses')
def expenses():
    expenses = Expense.query.all()
    # total = 0
    # total_food = 0
    # total_Travel = 0
    # total_Entertainment = 0
    # total_business = 0
    # total_other = 0
    total = sum([expense.price for expense in expenses])
    total_food = sum(
        [expense.price for expense in expenses if expense.category == "Food"])
    total_Travel = sum([
        expense.price for expense in expenses if expense.category == "Travel"])
    total_Entertainment = sum([
        expense.price for expense in expenses if expense.category == "Entertainment"])
    total_business = sum([
        expense.price for expense in expenses if expense.category == "business"])
    total_other = sum([
        expense.price for expense in expenses if expense.category == "other"])

    print(total, total_other, total_business,
          total_Entertainment, total_Travel, total_food)
    return render_template('expenses.html', expenses=expenses, total=total, total_business=total_business, total_Entertainment=total_Entertainment, total_Travel=total_Travel, total_food=total_food, total_other=total_other)


@app.route('/delete/<int:expense_id>')
def delete(expense_id):

    Expense.query.filter_by(id=expense_id).delete()
    db.session.commit()
    return redirect(url_for('expenses'))


@app.route('/update/<int:expense_id>')
def update(expense_id):

    expense = Expense.query.filter_by(id=expense_id).first()
    return render_template('update.html', expense=expense)


@app.route('/updateexpense/<int:expense_id>', methods=['POST'])
def updateexpense(expense_id):

    expense = Expense.query.filter_by(id=expense_id).first()
    expense.name = request.form['name']
    expense.date = request.form['date']
    expense.category = request.form['category']
    expense.price = request.form['price']
    db.session.commit()
    return redirect(url_for('expenses'))


if __name__ == "__main__":
    app.run(debug=True)
