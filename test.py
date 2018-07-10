from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', lazy='dynamic', back_populates='author')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User')

    def __repr__(self):
        return '<Post {}>'.format(self.body)

db.drop_all()
db.create_all()

# Susan will be both created and added to the session
u1 = User(username='susan', email='susan@example.com')
db.session.add(u1)

# John will be created, but not added
u2 = User(username='john', email='john@example.com')

# Create a post by Susan
p1 = Post(body='this is my post!', author=u1)

# Add susan's post to the session
db.session.add(p1)

# Create a post by john, since john does not yet exist as a user, he is created automatically
p2 = Post(body='this is my post!', author=u2)

# Add john's post to the session
db.session.add(p2)

# After the session has everything defined, commit it to the database
db.session.commit()

# Since these exist now, the next step is another post by the same user, the user object will now contain john
user = db.session.query(User).filter(User.username == 'john').first()

p3 = Post(body='My second Post!!', author=user)
db.session.add(p3)

db.session.commit()