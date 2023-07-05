import os

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
# from secrets_1 import API_KEY_SECRETS_FILE, DATABASE_URL
import requests
from datetime import datetime
from models import db, connect_db, User, Bio, Prediction_top, Prediction_bottom, Prediction_manager, Team, Season_league, Team_info, Results_all, Results_home, Results_away, League_standing, Fixture


app = Flask(__name__)

API_BASE_URL = "https://api-football-v1.p.rapidapi.com/v2"

# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     os.environ.get('DATABASE_URL', 'postgres:///matchday'))

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(DATABASE_URL)

# app.config['API_KEY'] = (os.environ.get('API_KEY', API_KEY_SECRETS_FILE))
API_KEY = app.config['API_KEY']



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

LEAGUE2020 = 2790
LEAGUE2021 = 3456
LEAGUE_ID = LEAGUE2021


connect_db(app)




def populate_season_league_table():
    """Populate table for season, league_id, league name for England"""

    stored_data = Season_league.query.all()
    for data in stored_data:
        db.session.delete(data)
        db.session.commit()

    url = "https://api-football-v1.p.rapidapi.com/v2/leagues/search/england"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers)
        
    data = response.json()
    for info in data['api']['leagues']:
        season_table = Season_league(season = info['season'], league_id = info['league_id'], league_name = info['name'], country = info['country'])
        db.session.add(season_table)
        db.session.commit()


def populate_team_table():
    """Populate table for all teams of country England"""
    url = "https://api-football-v1.p.rapidapi.com/v2/teams/search/england"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers)

    data = response.json()
    for info in data['api']['teams']:
        team_table = Team(team_id = info['team_id'], team_name = info['name'])
        db.session.add(team_table)
        db.session.commit()



def populate_team_info_table():
    """ Populate table with data about each team in England
    """

    stored_data = Team_info.query.all()
    for data in stored_data:
        db.session.delete(data)
        db.session.commit()


    url = "https://api-football-v1.p.rapidapi.com/v2/teams/search/england"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers)

    data = response.json()
    for info in data['api']['teams']:
        team_info_table = Team_info(team_name = info['name'], team_id = info['team_id'], logo = info['logo'], venue_name = info['venue_name'], venue_address = info['venue_address'], venue_city = info['venue_city'], venue_capacity = info['venue_capacity'])
        db.session.add(team_info_table)
        db.session.commit()



def populate_standings_table():
    """populate prem league table. Prem league id for 2020 = 2790"""
    stored_data = League_standing.query.all()
    for data in stored_data:
        db.session.delete(data)
        db.session.commit()

    url = f"https://api-football-v1.p.rapidapi.com/v2/leagueTable/{LEAGUE_ID}"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers)

    data = response.json()

    for info in data['api']['standings'][0]:
        league_table = League_standing(team_id = info['team_id'], rank = info['rank'], logo=info['logo'], form = info['forme'], points = info['points'], goalsDiff = info['goalsDiff'])
        db.session.add(league_table)
        db.session.commit()



def populate_results_all_table():
    """populate results table for all games. Prem league id for 2020 = 2790"""
    
    stored_data = Results_all.query.all()
    for data in stored_data:
        db.session.delete(data)
        db.session.commit()

    url = f"https://api-football-v1.p.rapidapi.com/v2/leagueTable/{LEAGUE_ID}"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers)

    data = response.json()
    for info in data['api']['standings'][0]:
        results_all_table = Results_all(team_id = info['team_id'], matches_played = info['all']['matchsPlayed'], win = info['all']['win'], draw = info['all']['draw'], lose = info['all']['lose'], goals_for = info['all']['goalsFor'], goals_against = info['all']['goalsAgainst'])
        db.session.add(results_all_table)
        db.session.commit()



def populate_fixtures():
    """populate upcoming fixture table for all games. Prem league id for 2020 = 2790"""
    
    stored_data = Fixture.query.all()
    for data in stored_data:
        db.session.delete(data)
        db.session.commit()
  
    
    url = f"https://api-football-v1.p.rapidapi.com/v2/fixtures/league/{LEAGUE_ID}/next/5"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers)


    data = response.json()
    for info in data['api']['fixtures']:
        upcoming_games = Fixture(event_date = info['event_date'], venue = info['venue'], referee = info['referee'], homeTeam = info['homeTeam']['team_name'], homeTeam_id = info['homeTeam']['team_id'], homeTeam_logo = info['homeTeam']['logo'], awayTeam = info['awayTeam']['team_name'], awayTeam_id = info['awayTeam']['team_id'], awayTeam_logo = info['awayTeam']['logo'])
        db.session.add(upcoming_games)
        db.session.commit()


#scripts to run
# populate_season_league_table()
# populate_team_table()
# populate_team_info_table()
# populate_standings_table()
# populate_results_all_table()
# populate_fixtures()
