"""User model tests."""

# run these tests with following command:
#
#    python -m unittest test_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Prediction_top, Team, Season_league, Team_info


# connect to test database
os.environ['DATABASE_URL'] = "postgresql:///matchday_test"


from app import app


class UserModelTestCase(TestCase):
    """Test model for users"""

    def setUp(self):
        """Drop database, removing test data and recreate for new tests"""
        db.drop_all()
        db.create_all()

        u1 = User.signup("User_john", "John", "Smith", "john@gmail.com", "password", "Chelsea", )
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

    
    def test_add_predictions(self):
        """Test addition of user predictions"""
        p = Prediction_top(first = "team1", second="team2", third = "team3", fourth = "team4", user_id = self.id1)
        db.session.commit()
        self.assertEqual(p.first, "team1")
        self.assertEqual(p.second, "team2")
        self.assertEqual(p.third, "team3")
        self.assertEqual(p.fourth, "team4")
        self.assertEqual(p.user_id, 1111)


    def test_team(self):
        """Test addition of team name and team id"""
        team = Team(team_id = 1, team_name = "Arsenal")
        db.session.commit()
        self.assertEqual(team.team_id, 1)
        self.assertEqual(team.team_name, "Arsenal")


    def test_season_league(self):
        """Test the insertion of season and league details"""
        season_league = Season_league(season = 2020, league_id = 20, league_name = "test name", country = "test_country")
        db.session.commit()
        
        self.assertEqual(season_league.season, 2020)
        self.assertEqual(season_league.league_id, 20)
        self.assertEqual(season_league.league_name, "test name")
        self.assertEqual(season_league.country, "test_country")

    
    def test_team_info(self):
        """Test insertion of team info"""
        team = Team_info(team_name = "test name", founded = 1900, venue_name = "test venue", venue_address = "test address", venue_city = "test city", venue_capacity = 60000, logo = "https//test_logo.com", team_id = 12345)
        db.session.commit()

        self.assertEqual(team.team_name, "test name")
        self.assertEqual(team.founded, 1900)
        self.assertEqual(team.venue_name, "test venue")
        self.assertEqual(team.venue_address, "test address")
        self.assertEqual(team.venue_city, "test city")
        self.assertEqual(team.venue_capacity, 60000)
        self.assertEqual(team.logo, "https//test_logo.com")
        self.assertEqual(team.team_id, 12345)





    

  

    






