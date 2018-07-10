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
    posts = db.relationship('Post', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Post {}>'.format(self.body)

db.drop_all()
db.create_all()

# Susan will be both created and added to the databases
u1 = User(username='susan', email='susan@example.com')
db.session.add(u1)

# John will be created, but not added
u2 = User(username='john', email='john@example.com')

# Create a post by Susan
p1 = Post(body='this is my post!', user_id=u1.id)

# Add susan's post to the databases
db.session.add(p1)

# Create a post by john, but do not save it
p2 = Post(body='this is my post!', user_id=u2.id)

# Add john's post to the databases
db.session.add(p2)

db.session.commit()