from flask import Flask, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import MoviesSchema, Movies


movieapi = Flask(__name__)
api = Api(movieapi)
engine = create_engine('sqlite:///mydatabase.db')
Session = sessionmaker(bind=engine)
movie_list = []
movie_dict = {}


class ListMovieAPI(Resource):
    def get(self):
        session = Session()
        movies = session.query(Movies).all()
        movieSchema = MoviesSchema()
        for movie in movies:
            output = movieSchema.dump(movie)
            movie_list.append(output)
        for movie in movie_list:
            movie_dict[movie['name']] = {}
            for key in movie.keys():
                movie_dict[movie['name']][key] = movie[key]
        session.close()
        return movie_dict


class ListSingleMovie(Resource):
    def get(self, id):
        session = Session()
        movie = session.query(Movies).filter_by(id=id).first()
        movieSchema = MoviesSchema()
        output = movieSchema.dump(movie)
        print(output)
        session.close()
        return jsonify({'Result': output})


api.add_resource(ListMovieAPI, '/movies/')
api.add_resource(ListSingleMovie, '/movies/<int:id>')


if __name__ == '__main__':
    movieapi.run(port=80, debug=True)
