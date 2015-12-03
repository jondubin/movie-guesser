#name, score as input
#get curr time
#store score, time as tuple in a list in redis
#add score
#get high scores

#scores with score dictionary inside

import redis
from datetime import datetime
from operator import itemgetter
from config import password
from redis import redis_url

def add_score(user, score):
        r = redis.StrictRedis(host=redis_url, port=12890, db=0, password=password)
        curr_time = str(datetime.now())
        value = str(score) + "|" + curr_time + "|" + user
        r.rpush('scores', value)

def high_scores():
        r = redis.StrictRedis(host=redis_url, port=12890, db=0, password=password)
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

        print return_val


high_scores()
