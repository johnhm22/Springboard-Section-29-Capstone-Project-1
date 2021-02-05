"""Seed file to make sample data for db"""

from models import db
from app import app
from populate_scripts import populate_team_table, populate_season_league_table, populate_team_info_table, populate_standings_table, populate_results_all_table, populate_fixtures

#Create all tables
db.drop_all()
db.create_all()

#Update long term data in db
populate_team_table()
populate_season_league_table()
populate_team_info_table()
populate_standings_table()
populate_results_all_table()
populate_fixtures()

