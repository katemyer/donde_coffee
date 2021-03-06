
from api import create_app
app = create_app()
app.app_context().push()

from api import db
from api.models import User, Post
u = User(username='john', email='john@example.com')
db.session.add(u)
db.session.commit()

#Query User Table
users = User.query.all()
users

for u in users:
  print(u.id, u.username)

Now let's add a blog post:(adding a shop review)

>>> u = User.query.get(1)
>>> p = Post(body='my first post!', author=u)
>>> db.session.add(p)
>>> db.session.commit()

Query Post Table
>>> posts = Post.query.all()
>>> posts

To get Post Object
>>> p = posts[0]
>>> p
>>> p.id
>>> p.author

To get list of user's posts>>> for p in u.posts:
...     p
... 
<Post my first coffee review!>
<Post my second post!>

# get all users in reverse alphabetical order
>>> User.query.order_by(User.username.desc()).all()
[<User susan>, <User john>]