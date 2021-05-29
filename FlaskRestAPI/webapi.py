from flask import Flask, render_template
import requests
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

proj_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(proj_dir, 'nydatabase.db'))
webapp = Flask(__name__)
webapp.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(webapp)
ma = Marshmallow(webapp)


class Movie(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
    rating = db.Column(db.Float(), nullable=False)


class MovieSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movie


@webapp.route('/hello/<name>')
def index(name):
    resp = requests.get("http://localhost:5000/hello/{}".format(name))
    return resp.text


@webapp.route('/movies')
def movies():
    resp = requests.get("http://localhost:5000/movies")
    return render_template("movies.html", resp=resp.text)


@webapp.route('/movies/<name>')
def movie(name):
    resp = requests.get("http://localhost:5000/movies/{}".format(name))
    return resp.text


if __name__ == "__main__":
    webapp.run(port=80, debug=True)
