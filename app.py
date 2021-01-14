import os

from flask import Flask, render_template, request, flash, redirect, session, jsonify, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from secrets import API_KEY
import requests
from datetime import date
# from populate import populate_standings_table

from forms import UserAddForm, UserEditForm, LoginForm, PredictionsForm
from models import db, connect_db, User, Bio, Prediction_top, Prediction_bottom, Prediction_manager, Team, Season_league, Team_info, Results_all, Results_home, Results_away, League_standing, Fixture


today = date.today()
d1 = today.strftime("%Y-%m-%d")




CURR_USER_KEY = "curr_user"

app = Flask(__name__)

API_BASE_URL = "https://api-football-v1.p.rapidapi.com/v2"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///matchday'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

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


@app.route("/")
def homepage():
    """Show homepage."""

    # user = User.query.get_or_404(user_id)
    return render_template("home.html")




@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        user = User.signup(
                username=form.username.data,
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                password=form.password.data,
                email=form.email.data,
            )
        # db.session(user)
        db.session.commit()

        # except IntegrityError:
        #     flash("Username already taken", 'danger')
        #     return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)


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
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Logout user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        # return render_template('users/login.html')
        return redirect('/')



@app.route('/user/<int:user_id>/predictions', methods=['GET', 'POST'])
def predictions(user_id):
    """Record season predictions from user
    """
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
    """Show season predictions from user
    """
    prediction_top = Prediction_top.query.get_or_404(user_id)
    prediction_bottom = Prediction_bottom.query.get_or_404(user_id)
    prediction_manager = Prediction_manager.query.get_or_404(user_id)

    return render_template('predictions_show.html', prediction_top = prediction_top, prediction_bottom = prediction_bottom, prediction_manager = prediction_manager)




@app.route('/leaguetable')
def show_league_table():
    populate_standings_table()
    league = League_standing.query.all()
    return render_template('league_table.html', league = league)



# def show_league_table():
#     fixture = Fixture.query.all()
#     return render_template('league_fixtures.html', fixture = fixture)

# @app.route('/fixtures')
# def show_upcoming_fixtures():
#     # get next 5 fixtures from league id = 2790 (prem league 2020)
#     url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/league/2790/next/5"
#     headers = {
#         'x-rapidapi-key': API_KEY,
#         'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
#         }
#     response = requests.request("GET", url, headers=headers)
        
#     data = response.json()
#     fixtures = data['api']['fixtures']
#     return render_template("league_fixtures.html", fixtures = fixtures)


#Get data from backend database
@app.route('/fixtures')
def show_upcoming_fixtures():
    # get next 5 fixtures from league id = 2790 (prem league 2020)
    games = Fixture.query.all()
    return render_template("league_fixtures2.html", games = games)


@app.route('/live')
def show_live_games():
    # get next 5 fixtures from league id = 2790 (prem league 2020)
    d4 = today.strftime("%d-%b-%Y")
    url = f"https://api-football-v1.p.rapidapi.com/v2/fixtures/league/2790/{d1}"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    fixtures = data['api']['fixtures']
    return render_template("live.html", fixtures = fixtures, d4 = d4)