from flask import Flask, render_template, jsonify, request
from sqlalchemy import and_, select, func
from populate_db import engine, actors, movies, acts
import random

app = Flask(__name__)

conn = engine.connect()

def get_actor_id(name):
    stmt = select([actors.c.actor_id], actors.c.name==name)
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


# def get_random_actor_id():
#     stmt = select([func.max(actors.c.actor_id)]).select_from(actors)
#     results = conn.execute(stmt)
#     max_id = results.fetchone()[0]
#     stmt = select([func.min(actors.c.actor_id)]).select_from(actors)
#     results = conn.execute(stmt)
#     min_id = results.fetchone()[0]
#     random_actor_id = None
#     while not random_actor_id:
#         rand_id = random.randint(min_id, max_id)
#         print rand_id
#         rand_id = 1
#         stmt = select([actors.c.actor_id], actors.c.actor_id == rand_id)
#     results.close()
#     return random_actor_id


# @app.route('/get_random')
# def get_random():
#     print get_random_actor_id()
#     return jsonify({})


@app.route('/get_movies')
def get_movies():
    name = request.args.get('name')
    movies = get_actor_movies(name)
    return jsonify({'movies': movies})


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
