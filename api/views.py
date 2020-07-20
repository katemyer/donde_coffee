from flask import Blueprint, jsonify, request, render_template
from . import db # . looks in the __init__ file
from .models import User, Favorite #.models looks in models file
from .models import Shop
from flask_login import login_required, current_user
from . import yelp_api
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

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
# applying requirement that you must have a valid token 
# in order call this route
@jwt_required
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
#list all shops from db
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
#list all yelp coffeeshops by me
@main.route('/coffeeshops')
#applying requirement for valid token
# in order to search for coffee shops by location
@jwt_required
def coffeeshops():
    location = request.args.get('location')
    #query yelp for coffe shops by me (location)
    #synchronous call
    term = 'coffee'
    search_limit = 30
    radius = 16093
    open_now = True
    sort_by = 'rating'

    response = yelp_api.search_query(term = term,
                                 location = location,
                                 limit = search_limit,
                                 radius = radius,
                                 open_now = open_now,
                                 sort_by = sort_by
                                 )
    coffeeshops = response['businesses']

    #append dictionary to users [] with data: title and rating
    #user_list here matches user_list variable that was set for the db query 

    #info passing back to react side
    shops =[]
    for shop in coffeeshops:
        isPrice = False
        if 'price' in shop:
            isPrice = True
        shops.append({
            'id' : shop['id'],
            'image_url' : shop['image_url'],
            'name' : shop['name'],
            'address' : shop['location']['display_address'],
            'phone' : shop['phone'], 
            'rating' : shop['rating'],
            'price' : shop['price'] if (isPrice) else '',
            'distance' : shop['distance']
            })

    return jsonify({'coffeeshops' : shops})

#query to get shop id = {id}
#/GET https://api.yelp.com/v3/businesses/{id}
@main.route('/coffeeshops/<id>')
def shop_details(id):
    print(id)
    response = yelp_api.business_query(id=id)
    shop_details = response
    return jsonify({'coffeeshops' : shop_details})

#index page
@main.route('/')
def index():
    # return "<h1>DONDE COFFEE! </h1><p>bunch of stuff here later</p>"
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/login2', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = User.query.filter_by(email=username).first()

    #if user name and password are valid
    # create token, this comes from library at very top
    if (user and check_password_hash(user.password, password)):
        token = create_access_token(identity=username,expires_delta=False)
        return jsonify({'token' : token}), 200        
        
    
    return jsonify({"msg": "Wrong password or username"}), 401


@main.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# GET /favorites/2
# Get the favorites shops based on the user_id
@main.route('/favorites/<user_id>', methods=['GET'])
def favorties(user_id):
    print('favorites')

    # Check if user exist, use this user instead
    # current_user = get_jwt_identity()
    # if current_user:
    #      user_id = current_user.id
        
    # get user favorites from DB
    userFavorites = Favorite.query.filter_by(user_id=user_id).all()
    formattedFavorites = []

    for f in userFavorites:
        formattedFavorites.append(f.shop_id)

    # {
    #     'favorites' : [shopid1, shop2, shopid3]
    # }
    
    # return list of favorite shop_id (should be same as yelpIDs)
    return jsonify({ 'favorited_shop_ids' : formattedFavorites}), 200

# POST /togglefavorite?user_id=1&shop_id=2
# Toggle favorte/unfavorite for the user/shop combination
@main.route('/togglefavorite', methods=['POST'])
def togglefavorite():
    print('togglefavorites')
    user_id = request.args.get('user_id')
    shop_id = request.args.get('shop_id')
    # Check if user exist, use this user instead
    # current_user = get_jwt_identity()
    # if current_user:
    #      user_id = current_user.id
        
    # get user favorites from DB
    usershopFavorite = Favorite.query.filter_by(user_id=user_id, shop_id=shop_id).first()

    action = 'favorited'
    # user shop record exists, then we want to remove it and vice versa
    if usershopFavorite:
        #toggle it to not favorite by removing the record
        print('deleting record')
        action = 'unfavorited'
        db.session.delete(usershopFavorite)
        db.session.commit()
    else:
        print('adding record')
        usershopFavorite = Favorite(user_id=user_id,shop_id=shop_id)
        db.session.add(usershopFavorite)
        db.session.commit()
    
    

    result = {
        'action' : action,
        'user_id': user_id,
        'shop_id' : shop_id
    }

    # {
    #     'favorites' : [shopid1, shop2, shopid3]
    # }
    
    # return list of favorite shop_id (should be same as yelpIDs)
    return jsonify({ 'toggledfavorite' : result}), 200
