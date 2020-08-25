from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL

app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewTestCase(TestCase):
    """Tests for views for users"""

    def setUp(self):

        User.query.delete()

        user = User(first_name="Maria", last_name="Aldapa", image_url='https://pbs.twimg.com/ profile_images/2880657358/7076189976277c6be2d745cead4bd3fb.jpeg')

        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

    def tearDown(self):
        db.session.rollback()

    def test_redirect(self):
        with app.test_client()as client:
            resp = client.get('/')
            self.assertEqual(resp.status_code, 302)


    def test_user_list(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Maria', html)

    def test_user_details(self):
        with app.test_client() as client:
            resp = client.get(f'users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Maria Aldapa', html)

    def test_add_user(self):
        with app.test_client() as client:
            resp = client.post('/users', data = {'first_name': 'James', 'last_name': 'Reid', 'image_url': 'https://i.pinimg.com/originals/9e/9f/21/9e9f21f31b2b612c517ac86340d05a32.jpg'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('James', html)

    def test_edit_user(self):
        with app.test_client() as client:
            resp = client.post(f'/{self.user_id}', data={'first_name': 'Mary', 'last_name': 'Alda', 'image_url': 'https://pbs.twimg.com/profile_images/2880657358/7076189976277c6be2d745cead4bd3fb.jpeg'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Alda, Mary', html)
