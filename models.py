from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    print('************************')
    print('************************')
    print('def connect function called')
    print('************************')
    print('************************')
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    first_name = db.Column(
        db.Text,
        nullable = False
    )
 
    last_name = db.Column(
        db.Text,
        nullable = False
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    fave_team = db.Column(
        db.Text
    )

    password = db.Column(
        db.Text,
        nullable=False
    )

    created_on = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow()
    )



    @classmethod
    def signup(cls, username, first_name, last_name, email, password, fave_team):
        """Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            first_name = first_name,
            last_name = last_name,
            email=email,
            password=hashed_pwd,
            fave_team=fave_team
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Bio(db.Model):
    """Biographical data added by user"""

    __tablename__ = 'user_bio'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    bio = db.Column(
        db.Text,
        nullable = False
    )

    user_id = db.Column(
    db.Integer,
    db.ForeignKey('users.id', ondelete='CASCADE'),
    nullable=False
    )

    user = db.relationship('User')


class Prediction_top(db.Model):
    """Predictions for the top four teams at season end """

    __tablename__ = 'predictions_top'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    season = db.Column(
        db.Integer,
        nullable = True
    )

    first = db.Column(
        db.Text,
        nullable = False
    )

    second = db.Column(
        db.Text,
        nullable = False
    )
    third = db.Column(
        db.Text,
        nullable = False
    )
    fourth = db.Column(
        db.Text,
        nullable = False
    )

    user_id = db.Column(
    db.Integer,
    db.ForeignKey('users.id', ondelete='CASCADE'),
    nullable=False
    )

    user = db.relationship('User')


class Prediction_bottom(db.Model):
    """Predictions for the bottom three teams at season end """

    __tablename__ = 'predictions_bottom'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    season = db.Column(
        db.Integer,
        nullable = True
    )

    last = db.Column(
        db.Text,
        nullable = False
    )

    last_less_one = db.Column(
        db.Text,
        nullable = False
    )
    last_less_two = db.Column(
        db.Text,
        nullable = False
    )

    user_id = db.Column(
    db.Integer,
    db.ForeignKey('users.id', ondelete='CASCADE'),
    nullable=False
    )

    user = db.relationship('User')


class Prediction_manager(db.Model):
    """Predictions for managerial dismissals during the season """

    __tablename__ = 'predictions_manager'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    season = db.Column(
        db.Integer,
        nullable = True
    )

    first = db.Column(
        db.Text,
        nullable = False
    )

    second = db.Column(
        db.Text
    )

    user_id = db.Column(
    db.Integer,
    db.ForeignKey('users.id', ondelete='CASCADE'),
    nullable=False
    )

    user = db.relationship('User')


# Tables to store data from the API

class Team(db.Model):
    """Team reference and name"""

    __tablename__ = 'teams'

    team_id = db.Column(
        db.Integer,
        primary_key=True,
    )

    team_name = db.Column(
        db.Text,
        nullable = False
    )


class Season_league(db.Model):
    """League id for each season and country"""

    __tablename__ = 'season_league'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    season = db.Column(
        db.Integer,
        nullable = False
    )

    league_id = db.Column(
        db.Integer,
        nullable = False
    )

    league_name = db.Column(
        db.Text,
        nullable = False
    )
    
    country = db.Column(
        db.Text,
        nullable = False
    )


class Team_info(db.Model):
    """General info on each team"""

    __tablename__ = 'team_data'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    team_name = db.Column(
        db.Text,
        nullable = False
    )

    founded = db.Column(
        db.Integer,
        nullable = True
    )

    venue_name = db.Column(
    db.Text,
    nullable = True
    )

    venue_address = db.Column(
    db.Text,
    nullable = True
    )

    venue_city = db.Column(
    db.Text,
    nullable = True
    )

    venue_capacity = db.Column(
    db.Integer,
    nullable = True
    )
    
    logo = db.Column(
    db.Text,
    nullable = True
    )

    team_id = db.Column(
    db.Integer,
    db.ForeignKey('teams.team_id', ondelete='CASCADE'),
    nullable = False
    )

    team = db.relationship('Team')


class Results_all(db.Model):
    """Team results in both home and away games"""

    __tablename__ = 'results_all'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    matches_played = db.Column(
    db.Integer,
    nullable = False
    )

    win = db.Column(
    db.Integer,
    nullable = False
    )

    draw = db.Column(
    db.Integer,
    nullable = False
    )

    lose = db.Column(
    db.Integer,
    nullable = False
    )

    goals_for = db.Column(
    db.Integer,
    nullable = False
    )

    goals_against = db.Column(
    db.Integer,
    nullable = False
    )

    team_id = db.Column(
    db.Integer,
    db.ForeignKey('teams.team_id', ondelete='CASCADE'),
    nullable = False
    )

    team = db.relationship('Team')



class Results_home(db.Model):
    """Team results in home games"""

    __tablename__ = 'results_home'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    matches_played = db.Column(
    db.Integer,
    nullable = False
    )

    win = db.Column(
    db.Integer,
    nullable = False
    )

    draw = db.Column(
    db.Integer,
    nullable = False
    )

    lose = db.Column(
    db.Integer,
    nullable = False
    )

    goals_for = db.Column(
    db.Integer,
    nullable = False
    )

    goals_against = db.Column(
    db.Integer,
    nullable = False
    )

    team_id = db.Column(
    db.Integer,
    db.ForeignKey('teams.team_id', ondelete='CASCADE'),
    nullable = False
    )

    team = db.relationship('Team')
   

class Results_away(db.Model):
    """Team results in away games"""

    __tablename__ = 'results_away'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    matches_played = db.Column(
    db.Integer,
    nullable = False
    )

    win = db.Column(
    db.Integer,
    nullable = False
    )

    draw = db.Column(
    db.Integer,
    nullable = False
    )

    lose = db.Column(
    db.Integer,
    nullable = False
    )

    goals_for = db.Column(
    db.Integer,
    nullable = False
    )

    goals_against = db.Column(
    db.Integer,
    nullable = False
    )

    team_id = db.Column(
    db.Integer,
    db.ForeignKey('teams.team_id', ondelete='CASCADE'),
    nullable = False
    )

    team = db.relationship('Team')

    
class League_standing(db.Model):
    """General info on each team"""

    __tablename__ = 'league_standing'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    logo = db.Column(
        db.Text
    )

    rank = db.Column(
        db.Integer,
        nullable = False
    )

    form = db.Column(
        db.Text,
        nullable = False
    )

    goalsDiff = db.Column(
        db.Integer
    )

    points = db.Column(
        db.Integer
    )

    lastUpdate = db.Column(
        db.Integer
    )

    team_id = db.Column(
    db.Integer,
    db.ForeignKey('teams.team_id', ondelete='CASCADE'),
    nullable = False
    )

    team = db.relationship('Team')



class Fixture(db.Model):
    """details of forthcoming fixtures"""

    __tablename__ = 'fixtures'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    event_date = db.Column(
        db.Text
    )

    event_time = db.Column(
        db.Integer,
        nullable = True
    )

    venue = db.Column(
        db.Text
    )

    referee = db.Column(
        db.Text
    )

    homeTeam = db.Column(
        db.Text
    )

    homeTeam_id = db.Column(
        db.Integer
    )

    homeTeam_logo = db.Column(
        db.Text
    )

    awayTeam = db.Column(
        db.Text
    )

    awayTeam_id = db.Column(
        db.Integer
    )

    awayTeam_logo = db.Column(
        db.Text
    )



class Result(db.Model):
    """details of forthcoming fixtures"""

    __tablename__ = 'results'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    fixture_id = db.Column(
        db.Integer
    )

    league = db.Column(
        db.Text
    )

    event_date = db.Column(
        db.Text
    )

    home_team = db.Column(
        db.Text
    )

    home_team_id = db.Column(
        db.Integer
    )

    home_team_logo = db.Column(
        db.Text
    )

    away_team = db.Column(
        db.Text
    )

    away_team_id = db.Column(
        db.Integer
    )

    away_team_logo = db.Column(
        db.Text
    )

    goals_home_team = db.Column(
        db.Integer
    )

    goals_away_team = db.Column(
        db.Integer
    )




