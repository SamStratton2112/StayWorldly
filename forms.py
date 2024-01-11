from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from timezones import choices

class SearchForm(FlaskForm):
    """search city form"""
    city = StringField('City', validators=[DataRequired()])

class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6, max=50)])
    submit = SubmitField('Submit')

class EditUserForm(FlaskForm):
    """Edit user details form"""
    employer_timezone = SelectField('Employer Timezone', validators=[DataRequired()], choices=choices)
    password = PasswordField('Password', validators=[Length(min=6)])
    submit = SubmitField('Submit')
    

class RegisterUserForm(FlaskForm):
    """Register a new user"""
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6, max=50)])
    employer_timezone = SelectField('Employer Timezone', validators=[DataRequired()], choices=choices)
    submit = SubmitField('Submit')
    
    
