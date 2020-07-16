from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
# from flask_api import status
from yelpapi import YelpAPI
from flask_dotenv import DotEnv
# from config import Config
from flask_migrate import Migrate
from pprint import pprint

# app = Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)
db = SQLAlchemy() #don't pass anything bc initialize later
yelp_api = YelpAPI('8g-yyEi_zD7gTsiEegmXWrTx-0_M8SBDkWrw-vVHzMbeI4IzToQjj57lNuzlvhCSDgUZZKiJfgbqmTDDGfQsxRzB8-F59cr_kSXrQ1mIztVn0YAAMQrIQTke0_YNX3Yx')

def create_app():
    app = Flask(__name__)
    CORS(app)
    env = DotEnv(app)
    # cors = CORS(app, resources={r"/signup": {"origins": "http://localhost:3000"}})
    # app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SECRET_KEY'] = 'SECRET_KEY'
    #TODO: will just need to change this to POSTGRES
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config.from_pyfile('settings.py')
    db.init_app(app) #initialize app here
    migrate = Migrate(app, db)
    api_key = app.config.get("API_KEY")
    pprint(f'API_KEY = { app.config.get("API_KEY") }')

    from .views import main
    app.register_blueprint(main)
    # blueprint for auth routes in our app
    from .auth import auth as auth
    app.register_blueprint(auth)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    



    return app