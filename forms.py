from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    fave_team = StringField('Fave team', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    

class UserEditForm(FlaskForm):
    """Form for editing users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')
    bio = StringField('Bio', validators=[Optional()])
    header_image_url = StringField('Header_image_url', validators=[Optional()])




class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class PredictionsForm(FlaskForm):
    """Form for adding users."""

    top_team = StringField('Top team', validators=[DataRequired()])
    second_place = StringField('Second', validators=[DataRequired()])
    third_place = StringField('Third', validators=[DataRequired()])
    fourth_place = StringField('Fourth', validators=[DataRequired()])

    bottom_team = StringField('Bottom team', validators=[DataRequired()])
    second_from_bottom = StringField('Second from bottom', validators=[DataRequired()])
    third_from_bottom = StringField('Third from bottom', validators=[DataRequired()])

    manager_one = StringField('First prediction', validators=[DataRequired()])
    manager_two = StringField('Second prediction', validators=[DataRequired()])