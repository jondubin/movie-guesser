import json
# from pprint import pprint


def get_json(filename):
    records = []
    with open('TMDB/{}'.format(filename)) as data_file:
        record_str = ""
        depth = 0
        while True:
            char = data_file.read(1)
            if not char:
                break
            if char.isspace():
                continue
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
            record_str += char
            if depth == 0:
                record = json.loads(record_str)
                records.append(record)
                record_str = ""
    return records


def insert_people():
    people = get_json("TMDBPersonInfo")
    for person in people:
        name = person["name"]
        person_id = person["personId"]
        # insert person


def insert_movies_and_acts():
    movies = get_json("TMDBMovieInfo")
    for movie in movies:
        title = movie["title"]
        movie_id = movie["id"]
        # insert movie
        for actor in movie["cast"]:
            person_id = actor["personId"]
            #insert acts

# remove non actors
