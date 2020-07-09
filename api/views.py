from flask import Blueprint, jsonify, request
from . import db # . looks in the __init__ file
from .models import Movie #.models looks in models file

main = Blueprint('main', __name__)

#POST /add_movie
#Goal: taking data from request, adding to db, commiting

@main.route('/add_movie', methods=['POST'])
def add_movie():
  movie_data = request.get_json()

  #new Movie object
  #title comes from movie_data that's a json
  #the key for title is 'title'
  new_movie = Movie(title=movie_data['title'], rating=movie_data['rating'])

  db.session.add(new_movie) #adding new movie
  db.session.commit() # .save in rails

  return 'Done', 201

#GET /movies
#list all movies
@main.route('/movies')
def movies():
    #sqlite query directly on class Movie, get all movies
    movie_list = Movie.query.all()
    movies = []
    
    #append dictionary to movies [] with data: title and rating
    #movie_list here matches movie_list variable that was set for the db query 
    for movie in movie_list:
        movies.append({'title' : movie.title, 'rating' : movie.rating})

    return jsonify({'movies' : movies})

#index page
@main.route('/', methods=['GET'])
def home():
    return "<h1>!Starbucks Coffee Shop App</h1><p>bunch of stuff here later</p>"