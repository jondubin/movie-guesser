from flask import Flask, render_template, jsonify, request, send_file
from populate_db import engine
from sqlalchemy import and_, select, func
from populate_db import actors, movies, acts
import random
from StringIO import StringIO

from movie_guessr import app
from movie_guessr import conn
from movie_guessr import r
from utils import return_from_cache
from utils import get_poster_url
from utils import get_actor_url


def get_actor_id(name):
    stmt = select([actors.c.actor_id], actors.c.name == name)
    actor_ids = conn.execute(stmt)
    if actor_ids:
        for actor in actor_ids:
            actor_ids.close()
            return actor


def get_movies_from_id(actor_id):
    stmt = select([movies.c.name],
                  and_(actor_id == acts.c.actor_id,
                       acts.c.movie_id == movies.c.movie_id))
    results = conn.execute(stmt)
    movie_list = []
    for result in results:
        movie_list.append(result[0])
    results.close()
    return movie_list


def get_actor_movies(name):
    actor_id = get_actor_id(name)
    if not actor_id:
        return None
    return get_movies_from_id(actor_id)


def get_actor_with_movies(results):
    # stmt = select.order_by(func.rand([actors.c.actor_id])).limit(1)
    for result in results:
        actor_name = result[1]
        actor_id = result[0]
        query = "select name from movies M JOIN acts AC on M.movie_id = AC.movie_id where AC.actor_id = {}".format(actor_id)
        movies = engine.execute(query).fetchall()
        if len(movies) > 3:
            movies = [movie[0] for movie in movies]
            return jsonify({
                "actor_id": actor_id,
                "name": actor_name,
                "movies": movies
            })


@app.route('/get_random')
def get_random_actor():
    while True:
        query = "select actor_id, name from actors ORDER BY rand() limit 200"
        results = engine.execute(query)
        actor = get_actor_with_movies(results)
        if actor:
            return actor


@app.route('/get_actor_photo')
def get_actor_photo():
    name = request.args.get('name')
    return return_from_cache('actors', get_actor_url, name)


@app.route('/get_poster_photo')
def get_poster():
    name = request.args.get('name')
    return return_from_cache('posters', get_poster_url, name)


@app.route('/get_movies')
def get_movies():
    name = request.args.get('name')
    movies = get_actor_movies(name)
    return jsonify({'movies': movies})


@app.route('/')
def index():
    return render_template('index.html')
