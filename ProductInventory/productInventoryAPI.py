# productInventoryAPI
from flask import Flask, request, Response
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_restful import Resource, Api
from app import Products, Inventory
from app import ProductSerialization, InventorySerialization
import json


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


class GetProducts(Resource):
    def get(self):
        session = Session()
        products = session.query(Products).all()
        serializer = ProductSerialization()
        product_dict = {}
        counter = 0
        for product in products:
            output = serializer.dump(product)
            productcounter = "product_{}".format(counter)
            product_dict[productcounter] = output
            counter += 1
        session.close()
        return Response(json.dumps(product_dict), status=200)


class SearchProductOnQuery(Resource):
    def get(self, query):
        dbquery = "%{}%".format(query)
        session = Session()
        searchResults = session.query(Products).filter(
            Products.productName.like(dbquery)).all()
        session.close()
        searchdict = {}
        counter = 0
        serializer = ProductSerialization()
        if len(searchResults) == 1:
            output = serializer.dump(searchResults[0])
            searchdict["search_{}".format(counter)] = output
        elif len(searchResults) > 1:
            for product in searchResults:
                output = serializer.dump(product)
                searchcounter = "search_{}".format(counter)
                searchdict[searchcounter] = output
                counter += 1
        print(searchdict)
        return Response(json.dumps(searchdict), status=200)


class AddInventory(Resource):
    def post(self):
        session = Session()
        data = request.get_json()
        print(data['categoryName'])
        invetoryExist = session.query(Inventory).filter_by(
            categoryName=data['categoryName'].lower()).first()
        print(invetoryExist)
        if invetoryExist is None:
            newInventory = Inventory(categoryName=data['categoryName'])
            session.add(newInventory)
            session.commit()
            session.close()
            return Response("Succesffuly Added", status=201)
        else:
            return Response("Failed", status=503)


class GetInvetory(Resource):
    def get(self):
        session = Session()
        invetories = session.query(Inventory).all()
        serializer = InventorySerialization()
        invetory_dict = {}
        counter = 0
        for invetory in invetories:
            output = serializer.dump(invetory)
            inventorycounter = "Inventory_{}".format(counter)
            invetory_dict[inventorycounter] = output
            counter += 1
        print(invetory_dict)
        return Response(json.dumps(invetory_dict), status=200)
        session.close()


class SearchInvetory(Resource):
    def get(self, query):
        dbquery = "%{}%".format(query)
        session = Session()
        isInvetoryExists = session.query(Inventory).filter(
            Inventory.categoryName.like(dbquery)).all()
        serializer = InventorySerialization()
        invetory_dict = {}
        counter = 0
        if len(isInvetoryExists) == 1:
            output = serializer.dump(isInvetoryExists[0])
            invetory_dict["Inventory_{}".format(counter)] = output
        elif len(isInvetoryExists) > 1:
            for inventory in isInvetoryExists:
                output = serializer.dump(inventory)
                invetorycounter = "Invetory_{}".format(counter)
                invetory_dict[counter] = output
                counter += 1
        session.close()
        return Response(json.dumps(invetory_dict), status=200)


api.add_resource(AddProduct, '/addproduct')
api.add_resource(GetProducts, '/getproducts')
api.add_resource(SearchProductOnQuery, '/searchproduct/<query>')
api.add_resource(AddInventory, '/addinventory')
api.add_resource(GetInvetory, '/getinventories')
api.add_resource(SearchInvetory, '/searchinventory/<query>')


if __name__ == '__main__':
    productInvetoryApp.run(debug=True, port=80)
