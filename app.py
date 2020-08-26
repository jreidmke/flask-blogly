"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Rebel4ceradio@localhost/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


app.config['SECRET_KEY'] = "james"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

# Show Users List

@app.route('/')
def show_home():
    return redirect('/users')

@app.route('/users')
def show_users():
    users = User.query.order_by(User.last_name.asc()).all()
    return render_template('home.html', users = users)

# Show User Details

@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user = user)

# Add New User

@app.route('/users/new')
def show_new_user_page():
    return render_template('new-user.html')

@app.route('/users', methods=["POST"])
def create_new_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

# Edit User Details

@app.route('/users/<int:user_id>/edit')
def show_edit_user_page(user_id):
    user = User.query.get(user_id)
    return render_template('edit-user.html', user = user)

@app.route('/<int:user_id>', methods=["POST"])
def show_updated_user_page(user_id):
    user = User.query.get(user_id)
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url
    db.session.add(user)
    db.session.commit()
    return redirect('/')

# Delete User

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def show_delete_page(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/')

# Add Post Page

@app.route('/users/<int:user_id>/posts/new')
def show_add_post_page(user_id):
    user = User.query.get(user_id)
    return render_template('add-post.html', user = user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    user = User.query.get(user_id)
    title = request.form['title']
    content = request.form['content']
    post = Post(user_id=user_id, title=title, content=content)
    db.session.add(post)
    db.session.commit()
    return redirect(f'/users/{user.id}')

# Show post details

@app.route('/posts/<int:post_id>')
def show_post_details(post_id):
    post = Post.query.get(post_id)
    return render_template('post-detail.html', post=post)

# Edit Post Stuff

@app.route('/posts/<int:post_id>/edit')
def show_edit_page(post_id):
    post = Post.query.get(post_id)
    return render_template('edit-post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def make_post_edit(post_id):
    post = Post.query.get(post_id)
    title = request.form['title']
    content = request.form['content']
    post.title = title
    post.content = content
    db.session.add(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')

# Delete Post

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    user_id = Post.query.get(post_id)
    user_id = user_id.user_id
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f'/users/{user_id}')
