from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    """search city form"""
    city = StringField('City', validators=[DataRequired()])

class CommentForm(FlaskForm):
    """comment Form"""

    username = StringField('Username', validators=[DataRequired()])
    city_name = StringField('City Name', validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[DataRequired()])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class EditUserForm(FlaskForm):
    """Edit user details form"""
    employer_timezone = SelectField('Employer Timezone(optional)', choices=[('-11:00', 'American Samoa'),
                                                            ('-11:00', 'International Date Line West'),
                                                            ('-11:00', 'Midway Island'),
                                                            ('-10:00', 'Hawaii'),
                                                            ('-09:00', 'Alaska'),	
                                                            ('-08:00', 'Pacific Time (US & Canada)'),	
                                                            ('-08:00', 'Tijuana'), 	
                                                            ('-07:00', 'Arizona'), 	
                                                            ('-07:00', 'Chihuahua'), 	
                                                            ('-07:00', 'Mazatlan'), 	
                                                            ('-07:00', 'Mountain Time (US & Canada)'), 	
                                                            ('-06:00', 'Central America'), 	
                                                            ('-06:00', 'Central Time (US & Canada)'), 	
                                                            ('-06:00', 'Guadalajara'),	
                                                            ('-06:00', 'Mexico City'), 	
                                                            ('-06:00', 'Monterrey'),
                                                            ('-06:00', 'Saskatchewan'),
                                                            ('-05:00', 'Bogota'),
                                                            ('-05:00', 'Eastern Time (US & Canada)'),
                                                            ('-05:00', 'Indiana (East)'),
                                                            ('-05:00', 'Lima'),
                                                            ('-05:00', 'Quito'), 	
                                                            ('-04:00', 'Atlantic Time (Canada)'), 	
                                                            ('-04:00', 'Georgetown'),
                                                            ('-04:00', 'La Paz'),
                                                            ('-04:00', 'Santiago'),
                                                            ('-03:00', 'Brasilia'),
                                                            ('-03:00', 'Buenos Aires'),
                                                            ('-03:00', 'Greenland'),
                                                            ('-02:00', 'Mid-Atlantic'),
                                                            ('-01:00', 'Azores'),	
                                                            ('-01:00', 'Cape Verde Is.'),	
                                                            ('+00:00', 'Casablanca'),	
                                                            ('+00:00', 'Dublin'),
                                                            ('+00:00', 'Edinburgh'),
                                                            ('+00:00', 'Lisbon'),
                                                            ('+00:00', 'London'),
                                                            ('+00:00', 'Monrovia'),
                                                            ('+00:00', 'UTC'),
                                                            ('+01:00', 'Amsterdam'),	
                                                            ('+01:00', 'Belgrade'),
                                                            ('+01:00', 'Berlin'),
                                                            ('+01:00', 'Bern'),
                                                            ('+01:00', 'Bratislava'),
                                                            ('+01:00', 'Brussels'),
                                                            ('+01:00', 'Budapest'),
                                                            ('+01:00', 'Copenhagen'),
                                                            ('+01:00', 'Ljubljana'),
                                                            ('+01:00', 'Madrid'),
                                                            ('+01:00', 'Paris'),
                                                            ('+01:00', 'Prague'),
                                                            ('+01:00', 'Rome'),
                                                            ('+01:00', 'Sarajevo'),
                                                            ('+01:00', 'Skopje'),
                                                            ('+01:00', 'Stockholm'),
                                                            ('+01:00', 'Vienna'),
                                                            ('+01:00', 'Warsaw'),
                                                            ('+01:00', 'West Central Africa'),
                                                            ('+01:00', 'Zagreb'),
                                                            ('+01:00', 'Zurich'),
                                                            ('+02:00', 'Athens'),
                                                            ('+02:00', 'Bucharest'),
                                                            ('+02:00', 'Cairo'),
                                                            ('+02:00', 'Harare'),
                                                            ('+02:00', 'Helsinki'),
                                                            ('+02:00', 'Istanbul'),
                                                            ('+02:00', 'Jerusalem'),
                                                            ('+02:00', 'Kyiv'),
                                                            ('+02:00', 'Pretoria'),
                                                            ('+02:00', 'Riga'),
                                                            ('+02:00', 'Sofia'),
                                                            ('+02:00', 'Tallinn'),
                                                            ('+02:00', 'Vilnius'),	
                                                            ('+03:00', 'Baghdad'),
                                                            ('+03:00', 'Kuwait'),
                                                            ('+03:00', 'Minsk'),
                                                            ('+03:00', 'Moscow'),
                                                            ('+03:00', 'Nairobi'),
                                                            ('+03:00', 'Riyadh'),
                                                            ('+03:00', 'St. Petersburg'),
                                                            ('+03:00', 'Volgograd'),	
                                                            ('+04:00', 'Abu Dhabi'),
                                                            ('+04:00', 'Baku'),
                                                            ('+04:00', 'Muscat'),
                                                            ('+04:00', 'Tbilisi'),
                                                            ('+04:00', 'Yerevan'),
                                                            ('+05:00', 'Ekaterinburg'),
                                                            ('+05:00', 'Islamabad'),
                                                            ('+05:00', 'Karachi'),	
                                                            ('+05:00', 'Tashkent'),
                                                            ('+06:00', 'Almaty'),
                                                            ('+06:00', 'Astana'),
                                                            ('+06:00', 'Dhaka'),
                                                            ('+06:00', 'Novosibirsk'),
                                                            ('+06:00', 'Urumqi'),		
                                                            ('+07:00', 'Bangkok'),
                                                            ('+07:00', 'Hanoi'),
                                                            ('+07:00', 'Jakarta'),
                                                            ('+07:00', 'Krasnoyarsk'),	
                                                            ('+08:00', 'Beijing'),
                                                            ('+08:00', 'Chongqing'),
                                                            ('+08:00', 'Hong Kong'),
                                                            ('+08:00', 'Irkutsk'),
                                                            ('+08:00', 'Kuala Lumpur'),
                                                            ('+08:00', 'Perth'),
                                                            ('+08:00', 'Singapore'),
                                                            ('+08:00', 'Taipei'),
                                                            ('+08:00', 'Ulaanbataar'),
                                                            ('+09:00', 'Osaka'),
                                                            ('+09:00', 'Sapporo'),
                                                            ('+09:00', 'Seoul'),
                                                            ('+09:00', 'Tokyo'),
                                                            ('+09:00', 'Yakutsk'),
                                                            ('+10:00', 'Brisbane'),
                                                            ('+10:00', 'Canberra'),
                                                            ('+10:00', 'Guam'),
                                                            ('+10:00', 'Hobart'),
                                                            ('+10:00', 'Magadan'),
                                                            ('+10:00', 'Melbourne'),
                                                            ('+10:00', 'Port Moresby'),
                                                            ('+10:00', 'Solomon Is.'),
                                                            ('+10:00', 'Sydney'),
                                                            ('+10:00', 'Vladivostok'),
                                                            ('+11:00', 'New Caledonia'),	
                                                            ('+12:00', 'Auckland'),
                                                            ('+12:00', 'Fiji'),
                                                            ('+12:00', 'Kamchatka'),
                                                            ('+12:00', 'Marshall Is.'),
                                                            ('+12:00', 'Wellington'),
                                                            ('+12:00', 'Nukualofa'),
                                                            ('+12:00', 'Samoa'),
                                                            ('+13:00', 'Tokelau Is.')])
    # username = StringField('Username', validators=[DataRequired(), ])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class RegisterUserForm(FlaskForm):
    """Register a new user"""
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    employer_timezone = SelectField('Employer Timezone(optional)', choices=[('-11:00', 'American Samoa'),
                                                            ('-11:00', 'International Date Line West'),
                                                            ('-11:00', 'Midway Island'),
                                                            ('-10:00', 'Hawaii'),
                                                            ('-09:00', 'Alaska'),	
                                                            ('-08:00', 'Pacific Time (US & Canada)'),	
                                                            ('-08:00', 'Tijuana'), 	
                                                            ('-07:00', 'Arizona'), 	
                                                            ('-07:00', 'Chihuahua'), 	
                                                            ('-07:00', 'Mazatlan'), 	
                                                            ('-07:00', 'Mountain Time (US & Canada)'), 	
                                                            ('-06:00', 'Central America'), 	
                                                            ('-06:00', 'Central Time (US & Canada)'), 	
                                                            ('-06:00', 'Guadalajara'),	
                                                            ('-06:00', 'Mexico City'), 	
                                                            ('-06:00', 'Monterrey'),
                                                            ('-06:00', 'Saskatchewan'),
                                                            ('-05:00', 'Bogota'),
                                                            ('-05:00', 'Eastern Time (US & Canada)'),
                                                            ('-05:00', 'Indiana (East)'),
                                                            ('-05:00', 'Lima'),
                                                            ('-05:00', 'Quito'),
                                                            ('-04:00', 'Atlantic Time (Canada)'), 	
                                                            ('-04:00', 'Georgetown'),
                                                            ('-04:00', 'La Paz'),
                                                            ('-04:00', 'Santiago'),
                                                            ('-03:00', 'Brasilia'),
                                                            ('-03:00', 'Buenos Aires'),
                                                            ('-03:00', 'Greenland'),
                                                            ('-02:00', 'Mid-Atlantic'),
                                                            ('-01:00', 'Azores'),	
                                                            ('-01:00', 'Cape Verde Is.'),	
                                                            ('+00:00', 'Casablanca'),	
                                                            ('+00:00', 'Dublin'),
                                                            ('+00:00', 'Edinburgh'),
                                                            ('+00:00', 'Lisbon'),
                                                            ('+00:00', 'London'),
                                                            ('+00:00', 'Monrovia'),
                                                            ('+00:00', 'UTC'),
                                                            ('+01:00', 'Amsterdam'),	
                                                            ('+01:00', 'Belgrade'),
                                                            ('+01:00', 'Berlin'),
                                                            ('+01:00', 'Bern'),
                                                            ('+01:00', 'Bratislava'),
                                                            ('+01:00', 'Brussels'),
                                                            ('+01:00', 'Budapest'),
                                                            ('+01:00', 'Copenhagen'),
                                                            ('+01:00', 'Ljubljana'),
                                                            ('+01:00', 'Madrid'),
                                                            ('+01:00', 'Paris'),
                                                            ('+01:00', 'Prague'),
                                                            ('+01:00', 'Rome'),
                                                            ('+01:00', 'Sarajevo'),
                                                            ('+01:00', 'Skopje'),
                                                            ('+01:00', 'Stockholm'),
                                                            ('+01:00', 'Vienna'),
                                                            ('+01:00', 'Warsaw'),
                                                            ('+01:00', 'West Central Africa'),
                                                            ('+01:00', 'Zagreb'),
                                                            ('+01:00', 'Zurich'),
                                                            ('+02:00', 'Athens'),
                                                            ('+02:00', 'Bucharest'),
                                                            ('+02:00', 'Cairo'),
                                                            ('+02:00', 'Harare'),
                                                            ('+02:00', 'Helsinki'),
                                                            ('+02:00', 'Istanbul'),
                                                            ('+02:00', 'Jerusalem'),
                                                            ('+02:00', 'Kyiv'),
                                                            ('+02:00', 'Pretoria'),
                                                            ('+02:00', 'Riga'),
                                                            ('+02:00', 'Sofia'),
                                                            ('+02:00', 'Tallinn'),
                                                            ('+02:00', 'Vilnius'),	
                                                            ('+03:00', 'Baghdad'),
                                                            ('+03:00', 'Kuwait'),
                                                            ('+03:00', 'Minsk'),
                                                            ('+03:00', 'Moscow'),
                                                            ('+03:00', 'Nairobi'),
                                                            ('+03:00', 'Riyadh'),
                                                            ('+03:00', 'St. Petersburg'),
                                                            ('+03:00', 'Volgograd'),	
                                                            ('+04:00', 'Abu Dhabi'),
                                                            ('+04:00', 'Baku'),
                                                            ('+04:00', 'Muscat'),
                                                            ('+04:00', 'Tbilisi'),
                                                            ('+04:00', 'Yerevan'),
                                                            ('+05:00', 'Ekaterinburg'),
                                                            ('+05:00', 'Islamabad'),
                                                            ('+05:00', 'Karachi'),	
                                                            ('+05:00', 'Tashkent'),	
                                                            ('+05:45', 'Kathmandu'),
                                                            ('+06:00', 'Almaty'),
                                                            ('+06:00', 'Astana'),
                                                            ('+06:00', 'Dhaka'),
                                                            ('+06:00', 'Novosibirsk'),
                                                            ('+06:00', 'Urumqi'),	
                                                            ('+07:00', 'Bangkok'),
                                                            ('+07:00', 'Hanoi'),
                                                            ('+07:00', 'Jakarta'),
                                                            ('+07:00', 'Krasnoyarsk'),	
                                                            ('+08:00', 'Beijing'),
                                                            ('+08:00', 'Chongqing'),
                                                            ('+08:00', 'Hong Kong'),
                                                            ('+08:00', 'Irkutsk'),
                                                            ('+08:00', 'Kuala Lumpur'),
                                                            ('+08:00', 'Perth'),
                                                            ('+08:00', 'Singapore'),
                                                            ('+08:00', 'Taipei'),
                                                            ('+08:00', 'Ulaanbataar'),
                                                            ('+09:00', 'Osaka'),
                                                            ('+09:00', 'Sapporo'),
                                                            ('+09:00', 'Seoul'),
                                                            ('+09:00', 'Tokyo'),
                                                            ('+09:00', 'Yakutsk'),
                                                            ('+10:00', 'Brisbane'),
                                                            ('+10:00', 'Canberra'),
                                                            ('+10:00', 'Guam'),
                                                            ('+10:00', 'Hobart'),
                                                            ('+10:00', 'Magadan'),
                                                            ('+10:00', 'Melbourne'),
                                                            ('+10:00', 'Port Moresby'),
                                                            ('+10:00', 'Solomon Is.'),
                                                            ('+10:00', 'Sydney'),
                                                            ('+10:00', 'Vladivostok'),
                                                            ('+11:00', 'New Caledonia'),	
                                                            ('+12:00', 'Auckland'),
                                                            ('+12:00', 'Fiji'),
                                                            ('+12:00', 'Kamchatka'),
                                                            ('+12:00', 'Marshall Is.'),
                                                            ('+12:00', 'Wellington'),
                                                            ('+12:00', 'Nukualofa'),
                                                            ('+12:00', 'Samoa'),
                                                            ('+13:00', 'Tokelau Is.')])