from . import db #import db object to inherent from class in __init__ file

class Movie(db.Model):
  #table columns
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50))
  rating = db.Column(db.Integer)