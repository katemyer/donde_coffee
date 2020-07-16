from yelpapi import YelpAPI
from pprint import pprint

yelp_api = YelpAPI('API_KEY')

#categories list: https://www.yelp.com/developers/documentation/v3/all_category_list
term = 'coffee'
location = 'Seattle, WA'
search_limit = 10
categories= 'coffee'
print('**search for business by term/category***')
response = yelp_api.search_query(term = term,
                                 location = location,
                                 limit = search_limit,
                                 categories = categories)
type(response)
pprint(response)


# Example phone search query.
# Phone Search API: https://www.yelp.com/developers/documentation/v3/business_search_phone

print('***** search for business by phone number *****\n{}\n'.format("yelp_api.phone_search_query("
                                                                     "phone='+13193375512')"))
response = yelp_api.phone_search_query(phone='+13193375512')
pprint(response)


# Example reviews query.
# Reviews API: https://www.yelp.com/developers/documentation/v3/business_reviews

print("***** selected reviews for Amy's on 6th St. *****\n{}\n".format("yelp_api.reviews_query(id='amys-ice-"
                                                                       "creams-austin-3')"))
response = yelp_api.reviews_query(id='amys-ice-creams-austin-3')
pprint(response)