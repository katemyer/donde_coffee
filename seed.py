print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))
from api import db
from api.models import User,Shop,Review,Favorite
from api import create_app

app = create_app()
app.app_context().push()

#Seeding User Data
#clear data in db
db.session.query(User).delete() 
db.session.commit()

users = []

u = User(name='charlie pie',username='charlie', email='charlie@example.com',password_hash='charlie123')
users.append(u)
u = User(name='steve stevey',username='hiitsmesteve', email='steve@example.com',password_hash='steve4562')
users.append(u)
u = User(name='surecan do',username='mochalatte', email='surecando@example.com',password_hash='surecandonothing56878')
users.append(u)

for user in users:
  #add to db
  db.session.add(user)
  #save
  db.session.commit()

#Seeding Shop Data
#clear data in db
db.session.query(Shop).delete() 
db.session.commit()

shops = []

s = Shop(name='Heart Coffee Roasters', description='A place where coffee meets the heart',hours='8am-3pm',address='1123 SW Washington St Portland OR 97205',phone='+15039543645',website='https://www.heartroasters.com/',price_level='$')
shops.append(s)
s = Shop(name='Olympia Coffee Roasters', description='Only the best coffee you will ever have',hours='7am-5pm',address='3840 California Ave SW Seattle WA 98116',phone='+12069354306',website='https://www.olympiacoffee.com/',price_level='$')
shops.append(s)
s = Shop(name='Anchorhead Coffee', description='Never sail away without a good up of coffee',hours='8am-3pm',address='1600 7th Ave Ste 105 Seattle WA 98101',phone= '+12062222222',website='https://anchorheadcoffee.com/',price_level='$$')
shops.append(s)
s = Shop(name='Matchstick Fraser Street', description='The only coffee you will need in BC ey!',hours='5am-5pm',address='639 E 15th Ave, Vancouver, BC V5T 2R6, Canada',phone= '+16045580639',website='https://matchstickyvr.com/',price_level='$$$')
shops.append(s)

for shop in shops:
  #add to db
  db.session.add(shop)
  #save
  db.session.commit()

#Seeding Review Data
#clear data in db
db.session.query(Review).delete() 
db.session.commit()

reviews = []

r = Review(body='Loved the coffee. It kept me awake for the drive home.', user_id='1',shop_id='1')
reviews.append(r)
r = Review(body='Went back twice because it was that good.', user_id='2',shop_id='2')
reviews.append(r)
r = Review(body='I live in Oregon and drive all the way to Seattle just for this coffee.', user_id='3',shop_id='3')
reviews.append(r)
r = Review(body='I am not sure if I should say that Canada has better coffee than Seattle.', user_id='3',shop_id='4')
reviews.append(r)

for review in reviews:
  #add to db
  db.session.add(review)
  #save
  db.session.commit()

#Seeding Favorite Data
#clear data in db
db.session.query(Favorite).delete() 
db.session.commit()

favorites = []

f = Favorite(user_id='1',shop_id='1')
favorites.append(f)
f = Favorite(user_id='2',shop_id='4')
favorites.append(f)
f = Favorite(user_id='3',shop_id='1')
favorites.append(f)
f = Favorite(user_id='3',shop_id='3')
favorites.append(f)
f = Favorite(user_id='3',shop_id='4')
favorites.append(f)

for favorite in favorites:
  #add to db
  db.session.add(favorite)
  #save
  db.session.commit()