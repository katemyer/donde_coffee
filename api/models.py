from . import db  # import db object to inherent from class in __init__ file
from datetime import datetime


class User(db.Model):
    # table columns
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    # saved_shops = db.relationship('Post', backref='person', lazy=True)

    def __repr__(self):    
      return f"User('{self.name}', '{self.email}')"


# class Shop(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120))
#     address = db.Column(db.String(120))
#     hours = db.Column(db.String(120))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     def __repr__(self):
#         return f"Shop('{self.name}', '{self.address}', '{self.address}'), '{self.hours}'"
