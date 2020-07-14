print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))
from . import db  # import db object to inherent from class in __init__ file
from datetime import datetime

# UserMixin, 
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), index=True, unique=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  reviews = db.relationship('Review', backref='user', lazy='dynamic')
  favorites = db.relationship('Favorite', backref='user', lazy='dynamic')

  def __repr__(self):
    return '<User {},{}>'.format(self.name,self.email)

class Shop(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120))
  description = db.Column(db.String(250))
  hours = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  website = db.Column(db.String(120))
  price_level = db.Column(db.String(120))
  reviews = db.relationship('Review', backref='shop', lazy='dynamic')
  favorites = db.relationship('Favorite', backref='shop', lazy='dynamic')

  def __repr__(self):
      return '<Shop {},{},{}>'.format(self.name,self.description,self.address)
  
class Review(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.String(140))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))

  def __repr__(self):
    return '<Review {},{},{}>'.format(self.body,self.user_id,self.shop_id)

class Favorite(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))

  def __repr__(self):
    return '<Favorite {},{},{}>'.format(self.user_id,self.shop_id)