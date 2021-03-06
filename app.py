"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres4@localhost/blogly'
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
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('home.html', posts = posts)

@app.route('/users')
def show_users():
    users = User.query.order_by(User.last_name.asc()).all()
    posts = Post.query.all()
    return render_template('users.html', users = users, posts = posts)

# Show User Details

@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user-detail.html', user = user)

# Add New User

@app.route('/users/new')
def show_new_user_page():
    return render_template('new-user.html')

@app.route('/users', methods=["POST"])
def create_new_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    if image_url == '':
        image_url = 'https://merriam-webster.com/assets/mw/images/article/art-wap-article-main/egg-3442-e1f6463624338504cd021bf23aef8441@1x.jpg'
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
    tags = Tag.query.all()
    return render_template('add-post.html', user = user, tags = tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    user = User.query.get(user_id)
    title = request.form['title']
    content = request.form['content']
    post = Post(user_id=user_id, title=title, content=content)
    db.session.add(post)
    db.session.commit()
    tags = request.form.getlist('tags')
    for tag in tags:
        tag = PostTag(post_id=post.id, tag_id = tag)
        db.session.add(tag)
    db.session.commit()

    return redirect(f'/')

# Show post details

@app.route('/posts/<int:post_id>')
def show_post_details(post_id):
    post = Post.query.get(post_id)
    return render_template('post-detail.html', post=post)

# Edit Post Stuff

@app.route('/posts/<int:post_id>/edit')
def show_edit_page(post_id):
    post = Post.query.get(post_id)
    tags = Tag.query.all()
    tag_ids = []
    for tag_id in post.tags:
        tag_ids.append(tag_id.tag_id)
    return render_template('edit-post.html', post=post, tags = tags, tag_ids = tag_ids)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def make_post_edit(post_id):
    post = Post.query.get(post_id)
    title = request.form['title']
    content = request.form['content']
    post.title = title
    post.content = content
    db.session.add(post)
    db.session.commit()
    tags = request.form.getlist('tags')
    for tag in tags:
        tag = PostTag(post_id=post.id, tag_id = tag)
        db.session.add(tag)
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

# Show tags

@app.route('/tags/')
def show_tags_page():
    tags = Tag.query.all()
    return render_template('tags.html', tags = tags)

@app.route('/tags/<int:tag_id>')
def show_tag_detail(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('tag-detail.html', tag = tag)

#Make new Tags

@app.route('/tags/new')
def show_new_tags_page():
    return render_template ('new-tags.html')

@app.route('/tags/new', methods=["POST"])
def make_new_tag():
    name = request.form['name']
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

# Edit tag

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_page(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('edit-tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    tag.name = request.form['name']
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')