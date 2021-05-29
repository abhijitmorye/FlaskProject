from flask import Flask, session, jsonify
from flask_restful import Resource, Api
from webapi import Movie, MovieSchema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# creaating connection to DB
engine = create_engine('sqlite:///nydatabase.db')
Session = sessionmaker(bind=engine)


app = Flask(__name__)
api = Api(app)
movie_list = []
movie_dict = {}


class Hello(Resource):
    def get(self, name):
        return {"Hello": name}


class ListAppMovies(Resource):
    def get(self):
        session = Session()
        movies = session.query(Movie).all()
        movieSchema = MovieSchema()
        for movie in movies:
            output = movieSchema.dump(movie)
            movie_list.append(output)
        for movie in movie_list:
            movie_dict[movie['name']] = {}
            for key in movie.keys():
                movie_dict[movie['name']][key] = movie[key]
        print(movie_dict)
        session.close()
        return movie_dict


class ListSingleMovie(Resource):
    def get(self, name):
        session = Session()
        movie = session.query(Movie).filter_by(name=name).first()
        movieSchema = MovieSchema()
        output = movieSchema.dump(movie)
        session.close()
        return jsonify({'Result': output})


api.add_resource(Hello, '/hello/<name>')
api.add_resource(ListAppMovies, '/movies')
api.add_resource(ListSingleMovie, '/movies/<name>')


if __name__ == "__main__":
    app.run(debug=True)
