from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Rebel4ceradio@localhost/blogly'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Test for models for User"""

    def setUp(self):
        User.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_repr(self):
        user = User(first_name='Maria', last_name='Aldapa')
        self.assertEqual(user.get_full_name(), 'Maria Aldapa')