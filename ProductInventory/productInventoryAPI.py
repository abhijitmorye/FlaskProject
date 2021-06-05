# productInventoryAPI
from flask import Flask, request, Response
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_restful import Resource, Api
from app import Products, Inventory


productInvetoryApp = Flask(__name__)
api = Api(productInvetoryApp)

engine = create_engine('sqlite:///productinvetory.db')
Session = sessionmaker(bind=engine, autoflush=False)


class AddProduct(Resource):
    def post(self):
        data = request.get_json()
        if data is not None:
            session = Session()
            totalPrice = float(data['price']) * float(data['quantity'])
            product = Products(
                productName=data['name'],
                prductQuantity=int(data['quantity']),
                productCategory=data['category'].lower(),
                prodcutSinglePrice=float(data['price']),
                procuctTotalPrice=totalPrice)
            session.add(product)
            inventoryExists = session.query(Inventory).filter_by(
                categoryName=data['category'].lower()).first()
            if inventoryExists is not None:
                inventoryExists.categoryQuantity += int(data['quantity'])
                inventoryExists.categoryTotalAmount += float(totalPrice)
            else:
                inventory = Inventory(categoryName=data['category'].lower(), categoryQuantity=int(data['quantity']),
                                      categoryTotalAmount=totalPrice)
                session.add(inventory)
            session.commit()
            session.close()
            return Response('Added', status=201)
        else:
            return Response('False', status=500)


api.add_resource(AddProduct, '/addproduct')


if __name__ == '__main__':
    productInvetoryApp.run(debug=True, port=80)
