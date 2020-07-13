from . import db  # import db object to inherent from class in __init__ file
from datetime import datetime

# UserMixin, 
class User(db.Model):
  # __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  posts = db.relationship('Post', backref='author', lazy='dynamic')

  def __repr__(self):
      return '<User {}>'.format(self.username)

class Shop(db.Model):
  __tablename__ = 'shops'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120))
  description = db.Column(db.String(250))
  hours = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  website = db.Column(db.String(120))
  price_level = db.Column(db.String(120))
  # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  # def __repr__(self):
  #     return f"Shop('{self.name}', '{self.address}', '{self.address}'), '{self.hours}'"
  
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)