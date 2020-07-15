from yelpapi import YelpAPI
from pprint import pprint

yelp_api = YelpAPI('8g-yyEi_zD7gTsiEegmXWrTx-0_M8SBDkWrw-vVHzMbeI4IzToQjj57lNuzlvhCSDgUZZKiJfgbqmTDDGfQsxRzB8-F59cr_kSXrQ1mIztVn0YAAMQrIQTke0_YNX3Yx')

term = 'coffee'
location = 'Seattle, WA'
search_limit = 10
response = yelp_api.search_query(term = term,
                                 location = location,
                                 limit = search_limit)
type(response)

pprint(response)
