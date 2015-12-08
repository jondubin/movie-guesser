import json
from sqlalchemy import (Table, Column, Integer,
                        Unicode, MetaData,
                        ForeignKey, create_engine)
from movie_guessr import ENGINE_URL

metadata = MetaData()

actors = Table('actors', metadata,
               Column('actor_id', Integer, primary_key=True),
               Column('name', Unicode(100))
)

movies = Table('movies', metadata,
               Column('movie_id', Integer, primary_key=True),
               Column('name', Unicode(100))
)

acts = Table('acts', metadata,
             Column('actor_id', Integer, ForeignKey('actors.actor_id')),
             Column('movie_id', Integer, ForeignKey('movies.movie_id'))
)

engine = create_engine(ENGINE_URL, echo=True)

def create_all():
    metadata.create_all(engine)


def get_json(filename):
    records = []
    with open('TMDB/{}'.format(filename)) as data_file:
        record_str = ""
        depth = 0
        while True:
            char = data_file.read(1)
            if not char:
                break
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
            record_str += char
            if depth == 0:
                if record_str.isspace():
                    continue
                print record_str
                record = json.loads(record_str)
                records.append(record)
                record_str = ""
    return records

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def insert_in_chunks(table, items_to_insert):
    conn = engine.connect()
    for chunk in chunks(items_to_insert, 5000):
        conn.execute(table.insert(), chunk)

def insert_people():
    people = get_json("TMDBPersonInfo")
    to_insert = []

    for person in people:
        name = person["name"]
        person_id = person["personId"]
        to_insert.append({"actor_id": person_id, "name": name})

    insert_in_chunks(actors, to_insert)


def insert_movies_and_acts():
    movies_json = get_json("TMDBMovieInfo")
    to_insert_movies = []
    to_insert_acts = []
    for movie in movies_json:
        name = movie["title"]
        movie_id = movie["id"]
        to_insert_movies.append({"movie_id": movie_id, "name": name})

        for actor in movie["cast"]:
            actor_id = actor["personId"]
            to_insert_acts.append({"movie_id": movie_id, "actor_id": actor_id})

    insert_in_chunks(movies, to_insert_movies)
    insert_in_chunks(acts, to_insert_acts)
