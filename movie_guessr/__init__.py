from flask import Flask
from populate_db import engine
import redis
from config import redis_url, password

app = Flask(__name__)
r = redis.StrictRedis(host=redis_url, port=12890, db=0, password=password)
conn = engine.connect()

import movie_guessr.views
import movie_guessr.utils
