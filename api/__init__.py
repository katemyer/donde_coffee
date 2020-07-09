from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #don't pass anything bc initialize later

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app) #initialize app here
    from .views import main
    app.register_blueprint(main)
    return app