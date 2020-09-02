"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()



class User(db.Model):

    def __repr__(self):
        return f"My name is {self.get_full_name()}."

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    image_url = db.Column(db.String(200), default = 'https://merriam-webster.com/assets/mw/images/article/art-wap-article-main/egg-3442-e1f6463624338504cd021bf23aef8441@1x.jpg')

    posts = db.relationship('Post', backref='users', cascade="all, delete")

class Post(db.Model):

    def __repr__(self):
        return f"{self.title} is title"

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
    default=datetime.utcnow)


    def date_time_print(self):
        return self.created_at.strftime("%a, %m/%d, %I:%M")

    tags = db.relationship('PostTag', cascade="all, delete", backref='post')

class Tag(db.Model):

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

    posts = db.relationship('PostTag', cascade="all, delete", backref='tag')

class PostTag(db.Model):

    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

def connect_db(app):
    db.app = app
    db.init_app(app)