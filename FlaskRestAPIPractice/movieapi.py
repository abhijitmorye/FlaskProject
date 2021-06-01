from flask import Flask, jsonify, request, Response
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


class AddMovie(Resource):
    def post(self):
        session = Session()
        data = request.get_json()
        movie = Movies(name=data['name'],
                       desc=data['desc'], rating=data['rating'])
        session.add(movie)
        session.commit()
        session.close()
        return Response('True', status=201)


class DeleteMovie(Resource):
    def delete(self, movie_id):
        session = Session()
        movie = session.query(Movies).filter_by(id=movie_id).first()
        flag = False
        if movie is not None:
            session.delete(movie)
            session.commit()
            flag = True
        session.close()
        if flag:
            return 'Deleted'
        else:
            return "Not deleted"


api.add_resource(ListMovieAPI, '/movies/')
api.add_resource(ListSingleMovie, '/movies/<int:id>')
api.add_resource(AddMovie, '/addmovie')
api.add_resource(DeleteMovie, '/deletemovie/<int:movie_id>')


if __name__ == '__main__':
    movieapi.run(port=80, debug=True)
