from flask import Blueprint, jsonify, request, render_template
from . import db # . looks in the __init__ file
from .models import User #.models looks in models file
from .models import Shop
from flask_login import login_required, current_user
from . import yelp_api

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

#GET /shops
#list all shops
@main.route('/shops')
def shops():
    #sqlite query directly on class User, get all users
    shop_list = Shop.query.all()
    shops = []

    #append dictionary to users [] with data: title and rating
    #user_list here matches user_list variable that was set for the db query 
    for shop in shop_list:
        shops.append({'name' : shop.name,'description' : shop.description,'address' : shop.address, 'phone' : shop.phone, 'website' : shop.website,'price_level' : shop.price_level})

    return jsonify({'shops' : shops})


#GET /coffeeshops?location=98055
#GET /coffeeshops body: {location:98055}
#list all yelp coffeeshops by me
@main.route('/coffeeshops')
def coffeeshops():
    location = request.args.get('location')
    #query yelp for coffe shops by me (location)
    term = 'coffee'
    #location = 'Seattle, WA'
    search_limit = 10
    response = yelp_api.search_query(term = term,
                                 location = location,
                                 limit = search_limit)
    coffeeshops = response['businesses']

    #append dictionary to users [] with data: title and rating
    #user_list here matches user_list variable that was set for the db query 

    shops =[]
    for shop in coffeeshops:
        shops.append({
            'name' : shop['name'],
            'address' : shop['location']['display_address'],
            'phone' : shop['phone'], 
            })

    return jsonify({'shops' : shops})

#index page
@main.route('/')
def index():
    # return "<h1>DONDE COFFEE! </h1><p>bunch of stuff here later</p>"
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)