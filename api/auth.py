from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, Response
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required
from .models import User
# from flask_api import status
# from flask_cors import CORS

auth = Blueprint('auth', __name__)
# CORS(auth)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():

    request_json = request.json

    email = request_json['user']['email']
    password = request_json['user']['password']
    # remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    print(user)
    if not user or not check_password_hash(user.password, password):
        return Response("{'status': 'error'}",  status=400, mimetype='application/json')

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    print(login_user)
    return Response("{'status': 'ok'}",  status=200, mimetype='application/json')


@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
# @cross_origin()
def signup_post():
    # breakpoint()

    request_json = request.json

    email = request_json['user']['email']
    name = request_json['user']['name']
    password = request_json['user']['password']

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        # return redirect(url_for('auth.signup'))
        return Response("{'error':'user already exists'}", status=400, mimetype='application/json')

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # return redirect(url_for('auth.login'))
    return Response("{'status':'ok'}", status=200, mimetype='application/json')

@auth.route("/users")
def users():
    # query db table
    user_list = User.query.all()
    users = []
    for user in user_list:
      users.append({'name': user.name, 'email': user.email, 'password': user.password})
      return jsonify({'users': users})

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return Response("{'status': 'successfully logged out'}",  status=200, mimetype='application/json')