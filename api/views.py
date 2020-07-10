from flask import Blueprint, jsonify, request
from . import db # . looks in the __init__ file
from .models import User #.models looks in models file

main = Blueprint('main', __name__)

#POST /add_user
#Goal: taking data from request, adding to db, commiting

@main.route('/add_user', methods=['POST'])
def add_user():
  user_data = request.get_json()

  #new User object
  #name comes from user_data that's a json
  #the key for name is 'name'
  new_user = User(name=user_data['name'], email=user_data['email'])

  db.session.add(new_user) #adding new user
  db.session.commit() # .save in rails

  return 'Done', 201

#GET /users
#list all users
@main.route('/users')
def users():
    #sqlite query directly on class User, get all users
    user_list = User.query.all()
    users = []
    
    #append dictionary to users [] with data: title and rating
    #user_list here matches user_list variable that was set for the db query 
    for user in user_list:
        users.append({'name' : user.name,'email' : user.email})

    return jsonify({'users' : users})

#index page
@main.route('/', methods=['GET'])
def home():
    return "<h1>!Starbucks Coffee Shop App</h1><p>bunch of stuff here later</p>"