"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_models.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Prediction_top

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///matchday_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data


class UserModelTestCase(TestCase):
    """Test model for users"""

    def setUp(self):
        """Drop database, removing test data and recreate for new tests"""
        db.drop_all()
        db.create_all()

        u1 = User.signup("User_john", "John", "Smith", "john@gmail.com", "password", "Chelsea")
        id1 = 1111
        u1.id = id1

        u2 = User.signup("User_sam", "Sam", "McClean", "sam@gmail.com", "password2", "Arsenal")
        id2 = 2222
        u2.id = id2

        db.session.commit()

        u1 = User.query.get(id1)
        u2 = User.query.get(id2)

        self.u1 = u1
        self.id1 = id1

        self.u2 = u2
        self.id2 = id2

        self.client = app.test_client()

    def tearDown(self):
        """Remove test data"""
        User.query.delete()
        db.session.rollback()

    
    def test_signup(self):
        """Test addition of new user"""

        u = User.signup(username = "User_nick", first_name="Nick", last_name="Johnson", password="password", fave_team="Southampton", email="nick@gmail.com")

        uid = 999
        u.id = uid
        db.session.commit()

        u = User.query.get(uid)
        self.assertIsNotNone(u)
        self.assertEqual(u.username, 'User_nick')
        self.assertEqual(u.first_name, 'Nick')
        self.assertEqual(u.last_name, 'Johnson')
        self.assertNotEqual(u.password, "password")
        self.assertEqual(u.fave_team, 'Southampton')
        self.assertEqual(u.email, 'nick@gmail.com')
        # Bcrypt strings should start with $2b$
        self.assertTrue(u.password.startswith("$2b$"))

    # OK
    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.id1)
        self.assertEqual(u.username, "User_john")

        
    # OK
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))


    # OK
    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))




    






