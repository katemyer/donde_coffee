from flask import Blueprint, jsonify, request, render_template
from . import db # . looks in the __init__ file
from .models import User, Favorite #.models looks in models file
from .models import Shop, Review
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
        token = create_access_token(identity=user.id,expires_delta=False)
        return jsonify({'token' : token, 'user_id': user.id}), 200        
        
    
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
@jwt_required
def favorties(user_id):
    print('favorites')

    # Check if user exist, use this user instead

    current_user_id = get_jwt_identity()
    if current_user_id:
        user_id = current_user_id
        
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
@jwt_required
def togglefavorite():
    print('togglefavorites')
    user_id = request.json.get('user_id')
    shop_id = request.json.get('shop_id')
    # user_id = request.args.get('user_id')
    # shop_id = request.args.get('shop_id')
    # Check if user exist, use this user instead
    current_user_id = get_jwt_identity()
    if current_user_id:
        user_id = current_user_id
        
    # get user favorites from DB

    # check if user_id and shop_id are filled correctly
    if not user_id or not shop_id:
        result = {
            'action' : "Did nothing",
            'user_id': user_id,
            'shop_id' : shop_id
        }  
        return jsonify({ 'toggledfavorite' : result}), 400
    
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

#*******************GETTING REVIEWS BY SHOPS ***********************#
# Get the reviews based on the shop_id
@main.route('/shopreviews/<shop_id>', methods=['GET'])
# @jwt_required
def shopReviews(shop_id):
    print('shopreviews')

    # Check if user exist, use this user instead
    # current_user_id = get_jwt_identity()
    # if current_user_id:
    #     user_id = current_user_id
        
    # get user reviews from DB
    shopReviews = Review.query.filter_by(shop_id=shop_id).all()
    formattedReviews = []

    for r in shopReviews:
        reviewhash = {
            'user_id' : r.user_id,
            'user_email' : r.user.email,
            'user_name' : r.user.name,
            'shop_id' : r.shop_id,
            'body' : r.body
        }
        formattedReviews.append(reviewhash)
    
    # return list of reviews by shop_id (should be same as yelpIDs)
    return jsonify({ 'shopReviews' : formattedReviews}), 200

#*******************GETTING REVIEWS BY USER ***********************#
# GET /reviews/2
# Get the reviews based on the user by grabbing their token
@main.route('/userreviews/', methods=['GET'])
#turning on protection to get the token
@jwt_required
def userReviews():
    print('userreviews')

    # Check if user exist, use this user instead
    user_id = get_jwt_identity()
 
    # get user reviews from DB
    userReviews = Review.query.filter_by(user_id=user_id).all()
    formattedReviews = []

    for r in userReviews:
        reviewhash = {
            'user_id' : r.user_id,
            'user_email' : r.user.email,
            'user_name' : r.user.name,
            'shop_id' : r.shop_id,
            'body' : r.body
        }
        formattedReviews.append(reviewhash)
    
    # return list of reviews by shop_id (should be same as yelpIDs)
    return jsonify({ 'userReviews' : formattedReviews}), 200

#*******************POSTING REVIEWS***********************#
# POST /reviews {user_id: 1, shop_id:hdaksdh, body: "loved it"}
@main.route('/review', methods=['POST'])
@jwt_required
def postReview():
    print('postingreviews')
    # user_id = request.json.get('user_id') : going to use token instead of this
    shop_id = request.json.get('shop_id')
    body = request.json.get('body')
  
    # Check if user exist, use this user's token instead
    user_id = None
    current_user_id = get_jwt_identity()
    if current_user_id:
        user_id = current_user_id
        
    # get reviews from DB
    # check if user_id and shop_id are filled correctly
    if not user_id or not shop_id or not body:
        result = {
            'action' : "Did nothing",
            'user_id': user_id,
            'shop_id' : shop_id,
            'body' : body
        }  
        return jsonify({ 'postReview' : result}), 400
    
    
    action = 'posting review'
    # user shop record exists, then we want to remove it and vice versa
      
    print('adding review')
    usershopReview = Review(user_id=user_id,shop_id=shop_id,body=body)
    db.session.add(usershopReview)
    db.session.commit()
 
    result = {
        'action' : action,
        'user_id': user_id,
        'shop_id' : shop_id
    }
 
    # return list of reviews 
    return jsonify({ 'postReview' : result}), 200