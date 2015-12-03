import tmdbsimple as tmdb
import redis
import requests
from config import tmdb_api
from config import redis_url
from config import password

tmdb.API_KEY = tmdb_api

def search_movies(all_movies):
	result = {}
	r = redis.StrictRedis(host=redis_url, port=12890, db=0, password=password)

	for movie in all_movies:
		search = tmdb.Search()
		response = search.movie(query=movie)
		movie_url = "http://image.tmdb.org/t/p/original" + search.results[0]['poster_path']
		result[movie] = movie_url
		print r.hset('poster', movie, movie_url)
		print r.hget('poster', movie)
	return result

# >>> r.set('foo', 'bar')
# True
# >>> r.get('foo')
# 'bar'

search_movies(["300", "Jackass"])