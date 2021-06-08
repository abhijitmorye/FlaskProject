from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os
from flask_marshmallow import Marshmallow
import json
import requests

proj_dir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///{}".format(os.path.join(proj_dir, 'productinvetory.db'))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Inventory(db.Model):
    __tablename__ = 'inventory'
    categoryName = db.Column(db.String(100), primary_key=True, nullable=False)
    categoryQuantity = db.Column(db.Integer())
    categoryTotalAmount = db.Column(db.Float())


class Products(db.Model):
    __tablename__ = 'products'
    productID = db.Column(db.Integer(), primary_key=True)
    productName = db.Column(db.String(100), nullable=False)
    prductQuantity = db.Column(db.Integer(), nullable=False)
    productCategory = db.Column(db.String(100), nullable=False)
    prodcutSinglePrice = db.Column(db.Float(), nullable=False)
    procuctTotalPrice = db.Column(db.Float())


class ProductSerialization(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Products


class InventorySerialization(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory


@app.route('/')
def index():
    resp = requests.get('http://localhost:80/getinventories')
    data = json.loads(resp.text)
    category_list = []
    for key, value in data.items():
        category_list.append(data[key]['categoryName'])
    return render_template('index.html', category_list=category_list)


@app.route('/addproduct', methods=['POST'])
def addProduct():

    productName = request.form['productName']
    productQuantity = request.form['prductQuantity']
    productCategory = request.form['productCategory']
    prodcutSinglePrice = request.form['prodcutSinglePrice']

    data = {
        'name': productName,
        'quantity': productQuantity,
        'category': productCategory,
        'price': prodcutSinglePrice
    }

    resp = requests.post('http://localhost:80/addproduct',
                         data=json.dumps(data),
                         headers={"Content-Type": "application/json",
                                  'Connection': 'keep-alive'})

    if resp.status_code == 201:
        return redirect(url_for('index'))
    else:
        return "Failed"


@app.route('/getproducts')
def getproducts():
    resp = requests.get('http://localhost:80/getproducts')
    json_response = json.loads(resp.text)
    return render_template('viewProducts.html', resp=json_response, flag=False)


@app.route('/searchproduct', methods=['POST'])
def searchProduct():
    query = request.form['query']
    resp = requests.get('http://localhost:80/searchproduct/{}'.format(query))
    json_response = json.loads(resp.text)
    return render_template('viewProducts.html', resp=json_response, flag=True)


@app.route('/addinventory')
def addInvetory():
    return render_template('addInventory.html', flag=False, msg="First Time")


@app.route('/submitinventory', methods=['POST'])
def submitInventory():
    categoryName = request.form['categoryName']
    data = {
        'categoryName': categoryName,
    }
    print(data)
    resp = requests.post('http://localhost:80/addinventory', headers={
                         "Content-Type": "application/json",
                         "Connection": 'keep-alive'
                         }, data=json.dumps(data))
    if resp.status_code == 201:
        return render_template('addInventory.html', flag=True, msg="Inventory created successfully")
    else:
        return render_template('addInventory.html', flag=True, msg="Failure")


@app.route('/viewinvetory')
def viewinvetory():
    resp = requests.get('http://localhost:80/getinventories')
    print(resp.text)
    return render_template('viewinventory.html', resp=json.loads(resp.text))


@app.route('/searchinventory', methods=['POST'])
def searchinventory():
    query = request.form['query']
    resp = requests.get('http://localhost:80/searchinventory/{}'.format(query))
    return render_template('viewinventory.html', resp=json.loads(resp.text))


if __name__ == '__main__':
    app.run(debug=True)
