import datetime
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor, db
from auth import AuthError, requires_auth

def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


'''
ACTORS
'''

@app.route('/', methods=['GET'])
def home():
    return 'hello'

@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(token):
    return 'hello'
  # try:
  #   actors = Actor.query.order_by('id').all()
  #
  #   if len(actors) == 0:
  #     abort(404)
  #
  #   formatted_actors = [actor.format() for actor in actors]
  #   return jsonify({
  #       'success': True,
  #       'total_actors': len(actors),
  #       'actors': formatted_actors
  #   }), 200

  # except AuthError:
  #   abort(422)


@app.route("/actors", methods=['POST'])
@requires_auth('post:actor')
def add_actor(payload):
    body = request.get_json()
    if body == None:
        abort(404)

    try:
        name = body['name']
        age = body['age']
        gender = body['gender']

        new_actor = Actor(
            name=name,
            age=age,
            gender=gender
        )

        new_actor.insert()

        return jsonify({
            'success': True,
            'actor': new_actor.format(),
            'total_actors': len(Actor.query.all())
        })
    except AuthError:
        abort(422)


@app.route('/actors/<id>', methods=['PATCH'])
@requires_auth('patch:actor')
def update_actor(payload, actor_id):
    body = request.get_json()
    actor = Actor.query.get(actor_id)

    if body == None or actor == None:
        abort(404)

    try:
        if 'name' in body:
            actor.name = body['name']

        if 'age' in body:
            actor.age = body['age']

        if 'gender' in body:
            actor.gender = body['gender']

        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.format(),
            'total_actors': len(Actor.query.all())
        })

    except AuthError:
        abort(422)



@app.route("/actors/<int:actor_id>", methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor == None:
        abort(404)

    try:
        actor.delete()
        return jsonify({
            'success': True,
            'deleted': actor_id
        })
    except AuthError:
        abort(422)



'''
MOVIES
'''


@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(token):
  try:
    movies = Movie.query.order_by('id').all()

    if len(movies) == 0:
      abort(404)

    formatted_movies = [movie.format() for movie in movies]
    return jsonify({
        'success': True,
        'total_movies': len(movies),
        'movies': formatted_movies
    }), 200

  except AuthError:
    abort(422)


@app.route("/movies", methods=['POST'])
@requires_auth('post:movie')
def add_movie(payload):
    body = request.get_json()

    if body == None:
        abort(404)

    try:
        title = body['title']
        release_date = body['release_date']

        new_movie = Movie(
            title=title,
            releaseDate=release_date
        )

        new_movie.insert()

        return jsonify({
            'success': True,
            'movie': new_movie.format(),
            'total_movies': len(Movie.query.all())
        })
    except AuthError:
        abort(422)



@app.route('/movies/<id>', methods=['PATCH'])
@requires_auth('patch:movie')
def update_movie(payload, movie_id):
  body = request.get_json()
  movie = Movie.query.get(movie_id)

  if body == None or movie == None:
      abort(404)

  try:
    if 'title' in body:
      movie.title = body['title']

    if 'release_date' in body:
      movie.release_date = body['release_date']

    movie.update()

    return jsonify({
        'success': True,
        'movie': movie,
        'total_movies': len(Movie.query.all())
    }), 200

  except AuthError:
      abort(422)




@app.route("/movies/<int:movie_id>", methods=['DELETE'])
@requires_auth('delete:movie')
def delete_movie(payload, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie == None:
        abort(404)

    try:
        movie.delete()
        return jsonify({
            'success': True,
            'deleted': movie_id
        })
    except AuthError:
        abort(422)



@app.errorhandler(AuthError)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401

@app.errorhandler(404)
def not_found(error):
  return jsonify({
    "success": False,
    "error": 404,
    "message": "not found"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
  return jsonify({
    "success": False,
    "error": 422,
    "message": "unprocessable"
    }), 422

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    }), 500
