from . import db #import db object to inherent from class in __init__ file

class User(db.Model):
  #table columns
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  email = db.Column(db.String(50))