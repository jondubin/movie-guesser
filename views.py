from flask import render_template, jsonify, request
from datetime import datetime
from operator import itemgetter
from application import engine
from sqlalchemy import and_, select
from populate_db import actors, movies, acts
import MySQLdb
import string
import random
from application import app
from application import conn
from application import r
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
    results = conn.execute(stmt).fetchall()
    movie_list = []
    print results
    for result in results:
        pass
        #print unicode(result[0], errors='replace')
        # movie_list.append(result[0])
    return movie_list


def get_actor_movies(name):
    actor_id = get_actor_id(name)
    if not actor_id:
        return None
    return get_movies_from_id(actor_id)


def get_actor_with_3_movies(results):
    for result in results:
        actor_name = result[1]
        actor_id = result[0]
        query = "select name " \
                "from movies M " \
                "JOIN acts AC on M.movie_id = AC.movie_id " \
                "where AC.actor_id = {}".format(actor_id)
        movies = engine.execute(query).fetchall()
        if len(movies) > 3:
            movies = [movie[0] for movie in movies]
            return jsonify({
                "actor_id": actor_id,
                "name": actor_name,
                "movies": movies
            })


def get_cast_excluding(movie_name, excluding):
    escaped = MySQLdb.escape_string(movie_name)
    escaped_excluding = MySQLdb.escape_string(excluding)
    query = "SELECT A.actor_id, A.name " \
            "FROM actors A " \
            "JOIN acts AC on AC.actor_id = A.actor_id " \
            "JOIN movies M on M.movie_id = AC.movie_id " \
            "WHERE M.name= '{}' AND A.name <> '{}'".format(escaped, escaped_excluding)
    cast = engine.execute(query).fetchall()
    return cast


@app.route('/get_acts_with')
def get_acts_with():
    name = request.args.get('name')
    actor_movies = get_actor_movies(name)
    if not actor_movies:
        return jsonify({})
    random.shuffle(actor_movies)
    for movie in actor_movies:
        cast = get_cast_excluding(movie, name)
        for actor in cast:
            actor_id = actor[0]
            actor_name = actor[1]
            if actor_name == name:
                continue
            cast_movies = get_movies_from_id(actor_id)
            if len(cast_movies) > 3:
                return jsonify({'name': actor_name,
                                 'movies': cast_movies,
                                 'acts_with': {'name': string.capwords(name),
                                               'movie': movie}})
    return jsonify({})


@app.route('/get_random')
def get_random_actor():
    while True:
        query = "select actor_id, name from actors ORDER BY rand() limit 200"
        results = engine.execute(query)
        actor = get_actor_with_3_movies(results)
        if actor:
            return actor


@app.route('/get_actor_photo')
def get_actor_photo():
    name = request.args.get('name')
    return return_from_cache('actors', get_actor_url, name)


@app.route('/get_poster_photo')
def get_poster():
    name = request.args.get('name')
    print name
    return return_from_cache('posters', get_poster_url, name)


@app.route('/get_movies')
def get_movies():
    name = request.args.get('name')
    movies = get_actor_movies(name)
    return jsonify({'name': string.capwords(name),
                    'movies': movies})


@app.route('/add_score', methods=['POST', 'GET'])
def add_score():
    content = request.get_json()
    print content
    user = content['name']
    score = content['score']
    curr_time = str(datetime.now())
    value = str(score) + "|" + curr_time + "|" + user
    r.rpush('scores', value)
    return jsonify({})


@app.route('/get_scores')
def get_high_scores():
    all_scores = r.lrange('scores', 0, -1)
    scores = []
    for score in all_scores:
        curr_score = {}
        entry_values =  score.split('|')
        curr_score['score'] = entry_values[0]
        curr_score['time'] = entry_values[1]
        curr_score['user'] = entry_values[2]
        scores.append(curr_score)

    newlist = sorted(scores, key=itemgetter('score'), reverse=True)
    return_val = {}
    return_val['scores'] = newlist
    return jsonify(return_val)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/high-scores')
def high_scores():
    return render_template('high_scores.html')
