"""
Test of routes in app.py

Running test file: comment out populate_standings_table() in app.py prior to running tests

run these tests with following command:

    python -m unittest test_app.py

"""

import os
from unittest import TestCase
from models import db, connect_db, User, Prediction_top, Prediction_bottom, Prediction_manager
from flask import session
from datetime import datetime, date


os.environ['DATABASE_URL'] = "postgresql:///matchday_test"


from app import app, CURR_USER_KEY

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()
import test_populate_scripts


class ViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""


        self.client = app.test_client()

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



        p1 = Prediction_top(first = 'Team1', second = 'Team2', third = 'Team3', fourth = 'Team4', user_id = id1)
        p2 = Prediction_bottom(last = 'Team20', last_less_one = 'Team19', last_less_two = 'Team18', user_id = id1)
        p3 = Prediction_manager(first = 'Man1', second = 'Man2', user_id = id1)

        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.commit()


     
    def tearDown(self):
        """Remove test data"""
        Prediction_top.query.delete()
        Prediction_bottom.query.delete()
        Prediction_manager.query.delete()
        User.query.delete()
        db.session.commit()
        db.session.rollback()

    
    def test_login(self):
        with app.test_client() as client:
            res = client.get("/login")
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h5 class="card-title">Login</h5>', html)


    def test_users_home(self):
        with app.test_client() as client:
            res = client.post('/login',
                                data={'username': 'User_john', 'password': 'password'})
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)

    
    def test_users_home(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.id1

            res = client.get('/home', follow_redirects = True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<th>Rank</th>', html)
            self.assertIn('<h3 class="display-5 mb-3 text-center">User_john, how\'s your fave team Chelsea doing?</h3>', html)
    

    
    def test_fixtures(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.id1


            res = client.get("/fixtures", follow_redirects=True)
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2 class="display-5">Five day fixture list</h2>', html)


    
    def test_recent_results(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.id1

            res = client.get("/user/recent_results")
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2 class="display-5">Last 5 league results</h2>', html)
    

    
    def test_league_table(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.id1

            res = client.get("/leaguetable")
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2 class="display-5">Premier League Table</h2>', html)
            self.assertIn('<th>Rank</th>', html)

    
    def test_live(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.id1
  
            res = client.get("/user/live")
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
        

    
    def test_predictions_show(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.id1
        
        res = client.get('/user/1111/predictions/show')
        html = res.get_data(as_text = True)

        self.assertEqual(res.status_code, 200)
        self.assertIn('<h5 class="mt-0 d-inline mb-2">Top teams</h5>', html)
        self.assertIn('<li class="list-group-item" style="background-color: #e4f0edaa">Team1</li>', html)
        self.assertIn('<li class="list-group-item" style="background-color: #e4f0edaa">Team2</li>', html)
        self.assertIn('<li class="list-group-item" style="background-color: #e4f0edaa">Team3</li>', html)
        self.assertIn('<li class="list-group-item" style="background-color: #e4f0edaa">Team4</li>', html)
     

        self.assertIn('<h5 class="mt-0 d-inline mb-2">Bottom three teams</h5>', html)
        self.assertIn(' <li class="list-group-item" style="background-color: #e4f0edaa">Team18</li>', html)
        self.assertIn(' <li class="list-group-item" style="background-color: #e4f0edaa">Team19</li>', html)
        self.assertIn(' <li class="list-group-item" style="background-color: #e4f0edaa">Team20</li>', html)
        

        self.assertIn('<h5 class="mt-0 d-inline mb-2">Managerial departures</h5>', html)
        self.assertIn(' <li class="list-group-item" style="background-color: #e4f0edaa">Man1</li>', html)
        self.assertIn(' <li class="list-group-item" style="background-color: #e4f0edaa">Man2</li>', html)
    


    

