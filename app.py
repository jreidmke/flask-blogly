"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Rebel4ceradio@localhost/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


app.config['SECRET_KEY'] = "james"
app.config['DEBUG_TB_INTERCEPT_DREIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def show_home():
    users = User.query.all()
    return render_template('home.html', users = users)

@app.route('/<int:user_id>')
def show_user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user = user)
