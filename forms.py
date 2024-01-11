from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    """search city form"""
    city = StringField('City', validators=[DataRequired()])

class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6, max=50)])
    submit = SubmitField('Submit')

choices=[
    ((''), 'Select Timezone'),
    (('-11:00', 'International Date Line West'), 'International Date Line West'),
    (('-10:00', 'Hawaii'), 'Hawaii'),
    (('-09:00', 'Alaska'), 'Alaska'),
    (('-08:00', 'Pacific Time'), 'Pacific Time'),
    (('-08:00', 'Tijuana'), 'Tijuana'),
    (('-07:00', 'Arizona'), 'Arizona'),
    (('-07:00', 'Chihuahua'), 'Chihuahua'),
    (('-07:00', 'Mazatlan'), 'Mazatlan'),
    (('-07:00', 'Mountain Time (US & Canada)'), 'Mountain Time (US & Canada)'),
    (('-06:00', 'Central America'), 'Central America'),
    (('-06:00', 'Central Time (US & Canada)'), 'Central Time (US & Canada)'),
    (('-06:00', 'Guadalajara'), 'Guadalajara'),
    (('-06:00', 'Mexico City'), 'Mexico City'),
    (('-06:00', 'Monterrey'), 'Monterrey'),
    (('-06:00', 'Saskatchewan'), 'Saskatchewan'),
    (('-05:00', 'Bogota'), 'Bogota'),
    (('-05:00', 'Eastern Time (US & Canada)'), 'Eastern Time (US & Canada)'),
    (('-05:00', 'Indiana (East)'), 'Indiana (East)'),
    (('-05:00', 'Lima'), 'Lima'),
    (('-05:00', 'Quito'), 'Quito'),
    (('-04:00', 'Atlantic Time (Canada)'), 'Atlantic Time (Canada)'),
    (('-04:00', 'Georgetown'), 'Georgetown'),
    (('-04:00', 'La Paz'), 'La Paz'),
    (('-04:00', 'Santiago'), 'Santiago'),
    (('-03:00', 'Brasilia'), 'Brasilia'),
    (('-03:00', 'Buenos Aires'), 'Buenos Aires'),
    (('-03:00', 'Greenland'), 'Greenland'),
    (('-02:00', 'Mid-Atlantic'), 'Mid-Atlantic'),
    (('-01:00', 'Azores'), 'Azores'),
    (('-01:00', 'Cape Verde Is.'), 'Cape Verde Is.'),
    (('+00:00', 'Casablanca'), 'Casablanca'),
    (('+00:00', 'Dublin'), 'Dublin'),
    (('+00:00', 'Edinburgh'), 'Edinburgh'),
    (('+00:00', 'Lisbon'), 'Lisbon'),
    (('+00:00', 'London'), 'London'),
    (('+00:00', 'Monrovia'), 'Monrovia'),
    (('+00:00', 'UTC'), 'UTC'),
    (('+01:00', 'Amsterdam'), 'Amsterdam'),
    (('+01:00', 'Belgrade'), 'Belgrade'),
    (('+01:00', 'Berlin'), 'Berlin'),
    (('+01:00', 'Bern'), 'Bern'),
    (('+01:00', 'Bratislava'), 'Bratislava'),
    (('+01:00', 'Brussels'), 'Brussels'),
    (('+01:00', 'Budapest'), 'Budapest'),
    (('+01:00', 'Copenhagen'), 'Copenhagen'),
    (('+01:00', 'Ljubljana'), 'Ljubljana'),
    (('+01:00', 'Madrid'), 'Madrid'),
    (('+01:00', 'Paris'), 'Paris'),
    (('+01:00', 'Prague'), 'Prague'),
    (('+01:00', 'Rome'), 'Rome'),
    (('+01:00', 'Sarajevo'), 'Sarajevo'),
    (('+01:00', 'Skopje'), 'Skopje'),
    (('+01:00', 'Stockholm'), 'Stockholm'),
    (('+01:00', 'Vienna'), 'Vienna'),
    (('+01:00', 'Warsaw'), 'Warsaw'),
    (('+01:00', 'West Central Africa'), 'West Central Africa'),
    (('+01:00', 'Zagreb'), 'Zagreb'),
    (('+01:00', 'Zurich'), 'Zurich'),
    (('+02:00', 'Athens'), 'Athens'),
    (('+02:00', 'Bucharest'), 'Bucharest'),
    (('+02:00', 'Cairo'), 'Cairo'),
    (('+02:00', 'Harare'), 'Harare'),
    (('+02:00', 'Helsinki'), 'Helsinki'),
    (('+02:00', 'Istanbul'), 'Istanbul'),
    (('+02:00', 'Jerusalem'), 'Jerusalem'),
    (('+02:00', 'Kyiv'), 'Kyiv'),
    (('+02:00', 'Pretoria'), 'Pretoria'),
    (('+02:00', 'Riga'), 'Riga'),
    (('+02:00', 'Sofia'), 'Sofia'),
    (('+02:00', 'Tallinn'), 'Tallinn'),
    (('+02:00', 'Vilnius'), 'Vilnius'),
    (('+03:00', 'Baghdad'), 'Baghdad'),
    (('+03:00', 'Kuwait'), 'Kuwait'),
    (('+03:00', 'Minsk'), 'Minsk'),
    (('+03:00', 'Moscow'), 'Moscow'),
    (('+03:00', 'Nairobi'), 'Nairobi'),
    (('+03:00', 'Riyadh'), 'Riyadh'),
    (('+03:00', 'St. Petersburg'), 'St. Petersburg'),
    (('+03:00', 'Volgograd'), 'Volgograd'),
    (('+04:00', 'Abu Dhabi'), 'Abu Dhabi'),
    (('+04:00', 'Baku'), 'Baku'),
    (('+04:00', 'Muscat'), 'Muscat'),
    (('+04:00', 'Tbilisi'), 'Tbilisi'),
    (('+04:00', 'Yerevan'), 'Yerevan'),
    (('+05:00', 'Ekaterinburg'), 'Ekaterinburg'),
    (('+05:00', 'Islamabad'), 'Islamabad'),
    (('+05:00', 'Karachi'), 'Karachi'),
    (('+05:00', 'Tashkent'), 'Tashkent'),
    (('+06:00', 'Almaty'), 'Almaty'),
    (('+06:00', 'Astana'), 'Astana'),
    (('+06:00', 'Dhaka'), 'Dhaka'),
    (('+06:00', 'Novosibirsk'), 'Novosibirsk'),
    (('+06:00', 'Urumqi'), 'Urumqi'),
    (('+07:00', 'Bangkok'), 'Bangkok'),
    (('+07:00', 'Hanoi'), 'Hanoi'),
    (('+07:00', 'Jakarta'), 'Jakarta'),
    (('+07:00', 'Krasnoyarsk'), 'Krasnoyarsk'),
    (('+08:00', 'Beijing'), 'Beijing'),
    (('+08:00', 'Chongqing'), 'Chongqing'),
    (('+08:00', 'Hong Kong'), 'Hong Kong'),
    (('+08:00', 'Irkutsk'), 'Irkutsk'),
    (('+08:00', 'Kuala Lumpur'), 'Kuala Lumpur'),
    (('+08:00', 'Perth'), 'Perth'),
    (('+08:00', 'Singapore'), 'Singapore'),
    (('+08:00', 'Taipei'), 'Taipei'),
    (('+08:00', 'Ulaanbataar'), 'Ulaanbataar'),
    (('+09:00', 'Osaka'), 'Osaka'),
    (('+09:00', 'Sapporo'), 'Sapporo'),
    (('+09:00', 'Seoul'), 'Seoul'),
    (('+09:00', 'Tokyo'), 'Tokyo'),
    (('+09:00', 'Yakutsk'), 'Yakutsk'),
    (('+10:00', 'Brisbane'), 'Brisbane'),
    (('+10:00', 'Canberra'), 'Canberra'),
    (('+10:00', 'Guam'), 'Guam'),
    (('+10:00', 'Hobart'), 'Hobart'),
    (('+10:00', 'Magadan'), 'Magadan'),
    (('+10:00', 'Melbourne'), 'Melbourne'),
    (('+10:00', 'Port Moresby'), 'Port Moresby'),
    (('+10:00', 'Solomon Is.'), 'Solomon Is.'),
    (('+10:00', 'Sydney'), 'Sydney'),
    (('+10:00', 'Vladivostok'), 'Vladivostok'),
    (('+11:00', 'New Caledonia'), 'New Caledonia'),
    (('+12:00', 'Auckland'), 'Auckland'),
    (('+12:00', 'Fiji'), 'Fiji'),
    (('+12:00', 'Kamchatka'), 'Kamchatka'),
    (('+12:00', 'Marshall Is.'), 'Marshall Is.'),
    (('+12:00', 'Wellington'), 'Wellington'),
    (('+12:00', 'Nukualofa'), 'Nukualofa'),
    (('+12:00', 'Samoa'), 'Samoa'),
    (('+13:00', 'Tokelau Is.'), 'Tokelau Is.')]

class EditUserForm(FlaskForm):
    """Edit user details form"""
    employer_timezone = SelectField('Employer Timezone', validators=[DataRequired()], choices=timezones.choices)
    password = PasswordField('Password', validators=[Length(min=6)])
    submit = SubmitField('Submit')
    

class RegisterUserForm(FlaskForm):
    """Register a new user"""
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6, max=50)])
    employer_timezone = SelectField('Employer Timezone', validators=[DataRequired()], choices=timezones.choices)
    submit = SubmitField('Submit')
    
    
