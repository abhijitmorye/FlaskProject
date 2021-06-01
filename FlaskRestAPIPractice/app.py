import re
from flask import Flask, jsonify, render_template, request, redirect, url_for
import requests
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json


proj_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(proj_dir, 'mydatabase.db'))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100))
    desc = db.Column(db.String(100))
    rating = db.Column(db.Float)


class MoviesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movies


@app.route('/movieList')
def movieList():
    resp = requests.get('http://localhost:80/movies/')
    return render_template('index.html', resp=json.loads(resp.text))


@app.route('/movie/<int:id>')
def movie(id):
    resp = requests.get('http://localhost:80/movies/{}'.format(id))
    return render_template('singledetail.html', resp=json.loads(resp.text))


@app.route('/addmovie')
def addmovie():
    return render_template('addmovie.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    desc = request.form['desc']
    rating = request.form['rating']

    data = {
        'name': name,
        'desc': desc,
        'rating': rating
    }

    resp = requests.post('http://localhost:80/addmovie',
                         data=json.dumps(data), headers={'Content-Type': 'application/json',
                                                         'Connection': 'keep-alive'})
    return redirect(url_for('movieList'))


@app.route('/deletemovie/<int:movie_id>')
def deletemovie(movie_id):

    resp = requests.delete(
        'http://localhost:80/deletemovie/{}'.format(movie_id))

    return resp.text


if __name__ == "__main__":
    app.run(debug=True)
