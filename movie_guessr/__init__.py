from flask import Flask
import redis
import os
import os.path
import logging
import sys
sys.setdefaultencoding('utf8')

if os.path.isfile(os.getcwd() + '/movie_guessr/config.py'):
    import config
    os.environ['REDIS_URL'] = config.REDIS_URL
    os.environ['BING_KEY'] = config.BING_KEY
    os.environ['REDIS_PASSWORD'] = config.REDIS_PASSWORD
    os.environ['TMDB_KEY'] = config.TMDB_KEY
    os.environ['ENGINE_URL'] = config.ENGINE_URL

REDIS_URL = os.environ.get('REDIS_URL')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
BING_KEY = os.environ.get('BING_KEY')
TMDB_KEY = os.environ.get('TMDB_KEY')
ENGINE_URL = os.environ.get('ENGINE_URL')
DEBUG = True

from populate_db import engine
app = Flask(__name__)
r = redis.StrictRedis(host=REDIS_URL, port=12890, db=0, password=REDIS_PASSWORD)
conn = engine.connect()

import movie_guessr.views
import movie_guessr.utils
