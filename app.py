from flask import Flask, request, render_template, redirect, session, flash
from models import db, connect_db, User, User_city
from forms import LoginForm, RegisterUserForm, EditUserForm, SearchForm
import sqlalchemy
import requests
import random
from sqlalchemy.exc import IntegrityError
import os 
from helpers import country_codes, get_city_search_results, get_city_details, get_city_photo, get_country_details, get_weather_tz, get_country_basics

# pytz, pycountry

app = Flask(__name__)

# Needs too be broken up into a few files

# # database for localhost
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///travel'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True
# SECRET_KEY for localhost
app.config['SECRET_KEY'] = 'secret'
# app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


with app.app_context():
    connect_db(app)

@app.route('/', methods=["GET", "POST"]) 
def homepage():
    """Show homepage:
    - if no user is logged in:
        - Navbar shows option to log in/ register 
        - list of cities 
    - if a user is logged in:
        - Navbar shows option to see user page/information
        - list of cities 
        - form to search for cities"""
    all_cities = set(User_city.query.all()) 
    all_user_cities = all_cities if len(all_cities) <= 9 else random.sample(all_cities, 9)
    form = SearchForm()
    if form.validate_on_submit():
        # Ensure capitalized for API request
        city_input = request.form['city'].capitalize()
        # get city results 
        city_results = get_city_search_results(city_input)
        return render_template('home.html', form=form, cities=city_results, all_user_cities=all_user_cities)
    return render_template('home.html', form=form, all_user_cities=all_user_cities)

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Handle user registration.
    - Create a new user and add to db. Redirect to homepage with new user logged in.
    - If form not valid, redirect back to register form.
    - If username is unavailable flash message and redirect back to register form"""
    form = RegisterUserForm()
    if form.validate_on_submit():
        try:
            # collect information from form and use User class method to validate inputs 
            ## handel invalid timezones can mostlikely be ommited when pytz is incorperated 
            # handle invalid timezone 
            if form.employer_timezone.data == '' :
                flash("Invalid Timezone!")
                return redirect('/register')
            user = User.register(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=form.password.data,
            employer_timezone=form.employer_timezone.data
            )
            # handle invalid timezone
            if form.employer_timezone.data == '' :
                flash("Invalid Timezone!")
                return redirect('/register')
            # add user to database
            db.session.add(user)
            db.session.commit() 
            # store username in session to indicate logged in True
            session['username']= user.username
            return redirect('/')
        except IntegrityError:
            # handle database duplication error 
            flash("This Username is unavailable")
            return redirect('/register')
    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def do_login():
    """ handle user log in"""
    form=LoginForm()
    if form.validate_on_submit(): 
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            # User.authenticate() will return the username of the authenticated user
            # if user is authenticated set session[username] indicating logged in 
            session['username']= user
            return redirect('/')
            # handle incorrect credentials 
        flash('Incorrect Username or Password!')
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/logout', methods=["POST"])
def logout():
    """handle user logout"""
    # clear the session to indicate log out
    session.pop('username')

    return redirect('/')

@app.route('/user/<username>', methods=["GET", "POST"])
def show_user(username):
    """show user page"""
    # handle no logged in user
    if 'username' not in session:
        flash("Access Denied")
        return redirect('/')
    # select user from database
    user = User.query.filter_by(username = session['username']).first()
    # trim characters off user timezone
    user_tz = (user.employer_timezone.replace("'", '').replace('(','').replace(')',''))
    # if no timezone selected leave timezone as empty string
    if len(user_tz) > 2:
        user_tz = 'Employer Timezone: UTC '+(user.employer_timezone.replace("'", '').replace('(','').replace(')',''))
    # get all user cities
    user_cities = User_city.query.filter_by(user_id = user.id).all()
    # initialize cities visited
    visited = []
    # initialize cities not visited
    to_visit = []
    for city in user_cities:
        # appened each city accordingly
        if city.visited == 0:
            to_visit.append(city)
        else:
            visited.append(city)
    return render_template('user.html', user=user,user_tz=user_tz, visited=visited, to_visit=to_visit)

@app.route('/user/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    """edit user details"""
    if 'username' not in session:
        flash("Access Denied")
        return redirect('/')
    # get user from database
    user = User.query.get_or_404(user_id)
    # get edit form containing current user information
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        # update data timezone
        user.employer_timezone = form.employer_timezone.data.replace("'", '').replace('(','').replace(')','')
        # handle invalid timezone
        if user.employer_timezone == '' :
                flash("Invalid Timezone!")
                return redirect(f'/user/{user_id}/edit')
        if User.authenticate(session['username'], form.password.data):
            db.session.commit()
            return redirect(f'/user/{user.username}')
        else: 
            flash("Incorrect Password!")
            return redirect(f'/user/{user_id}/edit')
    return render_template('edit.html', form=form, user=user)

@app.route('/city/<city_name>', methods=["GET", "POST"])
def show_city(city_name):
    """Get all relevant information about a city"""

    # Get City data from APIs
    try: 
        # Returns a dictionary containing population, longitude, latitude, and country
        city_info = get_city_details(city_name)

        # get city image 
        image = get_city_photo(city_info)

        # get country details, no details for USA
        country_description, activities = get_country_details(city_info)
    
        # Get user timezone info/difference and weather data
        c_temp, temp, time_dif, user, timezone, description = get_weather_tz(city_info)

        # get country currency, languages, and driving side
        curr, languages, driving = get_country_basics(city_info)

        return render_template('city.html', c_temp=c_temp, user=user, currency=curr, driving=driving, languages=languages,time_dif=time_dif, timezone=timezone, city_country=city_info['country'],  city_name=city_info['name'], temp=temp, image=image, description=description, activities=activities, country_description=country_description, population=city_info['population'])
    except KeyError:
        flash("We're still working on collecting data for this location!")
        return redirect('/')
    except IndexError:
        flash("We're still working on collecting data for this location!")
        return redirect('/')


@app.route('/save/<city_name>', methods=["GET", "POST"])
def save_city(city_name):
    """Save a city to user's page while avoiding duplication"""
    user = User.query.filter_by(username = session['username']).first()
    user_cities = User_city.query.filter_by(user_id = user.id).all()
    # get city data from teleport api using the city's short name 
    res = requests.get('https://api.api-ninjas.com/v1/city?name=', 
    params={'name': city_name}, 
    headers={
        "X-Api-Key":"bq8QLL6Jp79EIBsYjBWTlA==K8KjTdI3vm5VyHRH"})
    city_data = res.json()
    city_info = city_data[0]
    city_name = city_info['name']
    country_code = city_info["country"]
    city_country = find_key_by_value(country_codes, country_code)

    # get  images 
    country_basics = requests.get(f'https://pixabay.com/api/?key=41953233-44daacb0d74b24b2c21cce044&q={city_country}+{city_name}&image_type=photo')
    photos = country_basics.json()
    image= photos['hits'][0]['webformatURL']
    
    # handle duplication 
    for c in user_cities:
        if c.city_name == city_name:
            flash("You've already saved this city!")
            return redirect(f'/user/{user.username}')
    # add city to user_cities 
    add_city = User_city(city_name=city_name, city_image=image, user_id =user.id)
    db.session.add(add_city)
    db.session.commit()
    return redirect(f'/user/{user.username}')


@app.route('/remove/<city_id>', methods=["GET", "POST"])
def remove_u_city(city_id):
    """Remove a city from a user's page"""
    city = User_city.query.filter_by(id=city_id).first()
    user = session['username']
    db.session.delete(city)
    db.session.commit()
    return redirect(f'/user/{user}')

@app.route('/city/<int:city_id>/visted', methods=["GET", "POST"])
def mark_city_as_visited(city_id):
    """remove city from user not visited list and save the city as visited"""
    city = User_city.query.filter_by(id=city_id).first()
    user = session['username']
    city.visited = 1
    db.session.add(city)
    db.session.commit()
    return redirect(f'/user/{user}')   

@app.route('/city/<int:city_id>/notvisited', methods=["GET", "POST"])
def mark_city_as_not_visited(city_id):
    """remove city from user visited list and save the city as not visited"""
    city = User_city.query.filter_by(id=city_id).first()
    user = session['username']
    city.visited = 0
    db.session.add(city)
    db.session.commit()
    return redirect(f'/user/{user}') 
