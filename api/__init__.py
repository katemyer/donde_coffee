from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
# from flask_api import status
from yelpapi import YelpAPI

# from config import Config
from flask_migrate import Migrate

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


# app = Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)
db = SQLAlchemy() #don't pass anything bc initialize later
yelp_api = YelpAPI('8g-yyEi_zD7gTsiEegmXWrTx-0_M8SBDkWrw-vVHzMbeI4IzToQjj57lNuzlvhCSDgUZZKiJfgbqmTDDGfQsxRzB8-F59cr_kSXrQ1mIztVn0YAAMQrIQTke0_YNX3Yx')

def create_app():
    app = Flask(__name__)
    CORS(app)
    # cors = CORS(app, resources={r"/signup": {"origins": "http://localhost:3000"}})
    # app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'db34ee5752b1bd504abb0bdd8da928d8'
    #TODO: will just need to change this to POSTGRES
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app) #initialize app here
    migrate = Migrate(app, db)

    from .views import main
    app.register_blueprint(main)
    # blueprint for auth routes in our app
    from .auth import auth as auth
    app.register_blueprint(auth)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    
    app.config['JWT_SECRET_KEY'] = 'my-super-secret-flask-key'  # Change this!
    jwt = JWTManager(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    
    return app