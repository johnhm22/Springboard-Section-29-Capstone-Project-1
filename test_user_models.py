"""
Test of user creation, login and authentication

Running test file: comment out populate_standings_table() in app.py prior to running tests

run these tests with following command:

    python -m unittest test_app.py

"""


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Prediction_top

# Before app is imported, set an environmental variable
# to use test database. This needs to be done
# before app is imported, otherwise it will use the live database

os.environ['DATABASE_URL'] = "postgresql:///matchday_test"


from app import app



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

    
    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.id1)
        self.assertEqual(u.username, "User_john")

        
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))


    
    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))




    






