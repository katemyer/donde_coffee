from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
# from flask_api import status

# from config import Config
from flask_migrate import Migrate

# app = Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)
db = SQLAlchemy() #don't pass anything bc initialize later

def create_app():
    app = Flask(__name__)
    CORS(app)
    # cors = CORS(app, resources={r"/signup": {"origins": "http://localhost:3000"}})
    # app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'db34ee5752b1bd504abb0bdd8da928d8'
    #TODO: will just need to change this to POSTGRES
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://btsuvoxiobfgpe:f438b96451ee8c29892c77db3b5408941818de2b49cce2799112b707dd2fe695@ec2-34-225-82-212.compute-1.amazonaws.com:5432/df9eam8ii93hcd'
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

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    
    return app