from os import environ 

SECRET_KEY = environ.get('SECRET_KEY')
API_KEY = environ.get('API_KEY')
YELP_API_KEY = environ.get('YELP_API_KEY')