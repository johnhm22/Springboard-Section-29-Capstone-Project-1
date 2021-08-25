import os

from flask import Flask, render_template, request, flash, redirect, session, jsonify, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

import requests
from datetime import datetime, date
from ratelimit import limits, sleep_and_retry
from forms import UserAddForm, UserEditForm, LoginForm, PredictionsForm
from models import db, connect_db, User, Bio, Prediction_top, Prediction_bottom, Prediction_manager, Team, Season_league, Team_info, Results_all, Results_home, Results_away, League_standing, Fixture
from populate_scripts import populate_standings_table


today = date.today()
d1 = today.strftime("%Y-%m-%d")

FIFTEEN_MINUTES = 900
FIVE_MINUTES = 300

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

API_BASE_URL = "https://api-football-v1.p.rapidapi.com/v2"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///matchday'))
    
# app.config['API_KEY'] = (os.environ.get('API_KEY', API_KEY_SECRETS_FILE))
app.config['API_KEY'] = (os.environ.get('API_KEY'))
API_KEY = app.config['API_KEY']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's |a secret")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# toolbar = DebugToolbarExtension(app)

# 3456 is the API-Football id for the 2021-22 English Premier League
# 2790 is the API-Football id for the 2020-21 English Premier League

LEAGUE2020 = 2790
LEAGUE2021 = 3456
LEAGUE_ID = LEAGUE2021

connect_db(app)


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route("/")
def homepage():
    """Show homepage."""    
    return render_template("index.html")


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form.
    """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    
    form = UserAddForm()
    # the two lines below are not working; should give a drop down list of team_ids in the form
    #(next step is show team_name)

    fave_team_list = []
    teams = db.session.query(League_standing.team_id, Team.team_name).join(Team).all()
    for (id, name) in teams:
        fave_team_list.append(name)
    
    team_choices = [(team, team) for team in fave_team_list]

    form.fave_team.choices = team_choices



    if form.validate_on_submit():
        user = User.signup(
                username = form.username.data,
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                password = form.password.data,
                fave_team = form.fave_team.data,
                email = form.email.data
            )
        db.session.commit()

        do_login(user)
   
        return redirect("/user/profile")

    else:
        return render_template('signup.html', form=form)


@app.route('/user/profile')
def profile_page():
    """Present details of user's profile"""
    if not g.user:
        flash("Sorry, you are not authorised to view this page", "danger")
        return redirect("/")
    
    return render_template('user_profile.html')



@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle login.
    Present login form
    Check validity of username and password
    If details not valid, flash info message and re-present form.
    """

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            return redirect('/home')

        flash("Sorry, you're details don't match", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Logout user."""
    do_logout()

    flash(f"Thanks for visiting Matchday. You are now logged out", "success")
    return redirect('/')


@app.route('/home')
def home_page():
    """user home page displaying league standing for fave team and the next 5 games for team"""
    if not g.user:
        flash("Sorry, you are not authorised to view this page", 'danger')
        return redirect("/")
   
    team = Team.query.filter_by(team_name = g.user.fave_team).all()
    results = Results_all.query.filter_by(team_id = team[0].team_id).all()
    results_data = results[0]
    league = League_standing.query.filter_by(team_id = team[0].team_id).all()
    league_data = league[0]

    record = League_standing.query.filter_by(team_id = team[0].team_id).all()


    users_team = Team.query.filter_by(team_name = g.user.fave_team).all()


    url = f"https://api-football-v1.p.rapidapi.com/v2/fixtures/team/{users_team[0].team_id}/next/5"
    headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    future_games = data['api']['fixtures']

    return render_template('home.html', results_data=results_data, league_data=league_data, future_games = future_games, record=record)


@limits(calls = 1, period = FIVE_MINUTES)
@app.route('/user/recent_results')
def show_recent_results():
    """Show last five results in league"""
    if not g.user:
        flash("Sorry, you are not authorised to view this page", "danger")
        return redirect("/")


    url = f"https://api-football-v1.p.rapidapi.com/v2/fixtures/league/{LEAGUE_ID}/last/5"

    headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    results = data['api']['fixtures']

    return render_template('recent_results.html', results = results)


@app.route('/user/<int:user_id>/predictions', methods=['GET', 'POST'])
def predictions(user_id):
    """Record season predictions from user"""
    if not g.user:
        flash("Sorry, you are not authorised to view this page", "danger")
        return redirect("/")

    form = PredictionsForm()
    user = User.query.get_or_404(user_id)

    if form.validate_on_submit():
        prediction_top = Prediction_top(first = form.top_team.data,
                                        second = form.second_place.data,
                                        third = form.third_place.data,
                                        fourth = form.fourth_place.data,
                                        user_id = user_id)
        
        prediction_bottom = Prediction_bottom(last = form.bottom_team.data,
                                        last_less_one = form.second_from_bottom.data,
                                        last_less_two = form.third_from_bottom.data,
                                        user_id = user_id)
        
        prediction_manager = Prediction_manager(first = form.manager_one.data,
                                        second = form.manager_two.data,
                                        user_id = user_id)

        db.session.add(prediction_top)
        db.session.add(prediction_bottom)
        db.session.add(prediction_manager)
        db.session.commit()
        return redirect('/')

    return render_template('predictions.html', form=form, user=user)


@app.route('/user/<int:user_id>/predictions/show')
def predictions_show(user_id):
    """Show user's predictions for the season"""
    if not g.user:
        flash("Sorry, you are not authorised to view this page", "danger")
        return redirect("/")

    if Prediction_top.query.filter_by(user_id = g.user.id).all() == [] or Prediction_bottom.query.filter_by(user_id = g.user.id).all() == [] or Prediction_manager.query.filter_by(user_id = g.user.id).all() == []:
        flash("Please enter your predictions", "info")
        return redirect(f"/user/{user_id}/predictions")

    predictions_top = Prediction_top.query.filter_by(user_id = user_id)
    predictions_bottom = Prediction_bottom.query.filter_by(user_id = user_id)
    predictions_manager = Prediction_manager.query.filter_by(user_id = user_id)

    return render_template('predictions_show.html', predictions_top = predictions_top, predictions_bottom = predictions_bottom, predictions_manager = predictions_manager)


@limits(calls = 1, period = FIVE_MINUTES)
@app.route('/leaguetable')
def show_league_table():

    """Show current league table"""

    url = f"https://api-football-v1.p.rapidapi.com/v2/leagueTable/{LEAGUE_ID}"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    league = data['api']['standings'][0]
    return render_template('league_table.html', league = league)




@limits(calls = 1, period = FIVE_MINUTES)
@app.route('/fixtures')
def show_upcoming_fixtures():
    if not g.user:
        flash("Sorry, you are not authorised to view this page", "danger")
        return redirect("/")

    url = f"https://api-football-v1.p.rapidapi.com/v2/fixtures/league/{LEAGUE_ID}/next/5"
    headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    fixtures = data['api']['fixtures']
    return render_template('league_fixtures.html', fixtures = fixtures)



@limits(calls = 3, period = FIVE_MINUTES)
@app.route('/user/live')
def show_live_games():
    """Show scheduled/live games for the day """
    if not g.user:
        flash("Sorry, you are not authorised to view this page", "danger")
        return redirect("/")

    d_today = today.strftime("%d-%b-%Y")
    url = f"https://api-football-v1.p.rapidapi.com/v2/fixtures/league/{LEAGUE_ID}/{d1}"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    if data['api']['results'] == 0:
        return render_template('live_no_games.html')

    fixtures = data['api']['fixtures']
    return render_template("live.html", fixtures = fixtures, d_today = d_today)


