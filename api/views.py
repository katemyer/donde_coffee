from flask import Blueprint, jsonify, request
# from . import db 
# from .models import Movie

main = Blueprint('main', __name__)

@main.route('/add_movie', methods=['POST'])
def add_movie():
    movie_data = request.get_json()

    # new_movie = Movie(title=movie_data['title'], rating=movie_data['rating'])

    # db.session.add(new_movie)
    # db.session.commit()

    return 'Done', 201

@main.route('/movies')
def movies():
    movies = ['hi']
    # movie_list = Movie.query.all()
    # for movie in movie_list:
    #     movies.append({'title' : movie.title, 'rating' : movie.rating})
    return jsonify({'movies' : movies})

#index page
@main.route('/', methods=['GET'])
def home():
    return "<h1>!Starbucks Coffee Shop App</h1><p>bunch of stuff here later</p>"