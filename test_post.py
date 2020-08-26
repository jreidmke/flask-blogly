from unittest import TestCase

from app import app
from models import db, Post, User

# Use test database and don't clutter tests with SQL

app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class PostViewTestCase(TestCase):

    def setUp(self):
        Post.query.delete()
        User.query.delete()

        user = User(first_name="Maria", last_name="Aldapa", image_url='https://pbs.twimg.com/ profile_images/2880657358/7076189976277c6be2d745cead4bd3fb.jpeg')
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

        users = User.query.all()
        post = Post(user_id=self.user_id, title='Pizza', content='I like pizza.')
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id

    def tearDown(self):
        db.session.rollback()

    def test_new_post_on_user_detail(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Pizza', html)

    def test_make_new_post(self):
        data = {f'user_id': {self.user_id}, 'title': 'Movies', 'content': 'Movies are good'}
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/posts/new', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Movies', html)

    def test_show_post_details(self):
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('I like pizza', html)

    def test_edit_post(self):
        data = {'title': 'Candy', 'content': 'I like candy'}

        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/edit', data = data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Candy', html)
