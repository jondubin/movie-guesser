from bing_search_api import BingSearchAPI 
import json
from config import bing_api

def get_image(actor_name):
	my_key = bing_api
	query_string = actor_name
	bing = BingSearchAPI(my_key)
	params = {'ImageFilters':'"Face:Face"',
          '$format': 'json',
          '$top': 1,
          '$skip': 0}
	return bing.search('image',query_string,params).json()['d']['results'][0]['Image'][0]['MediaUrl']


print get_image("Jennifer Anniston")
print get_image("Jessica Biel")