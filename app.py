from flask import Flask, request, render_template, redirect, session, flash
from models import db, connect_db, User, User_city
from forms import LoginForm, RegisterUserForm, EditUserForm, SearchForm
import sqlalchemy
import requests
import random
from sqlalchemy.exc import IntegrityError
import os 
import logging
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
# database for localhost
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///travel'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True
# SECRET_KEY for localhost
# app.config['SECRET_KEY'] = 'secret'
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.logger.setLevel(logging.DEBUG)

# when this is active then I get Bad Request The CSRF token is missing whenn logging out. Otherwise, no errors
# csrf = CSRFProtect(app)

# app behaves the same if this is active or not 
# app.app_context().push()

# use imported function to connect app to database
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

    # initial cities list with duplication 
    all_cities = User_city.query.all()
    # initialize list used to render cities without duplication
    all_user_cities = []
    user_cities = []
    # initialize list of cities to return
    city_results = []
    app.logger.debug(f'Session Data: {session}')
    for city in all_cities:
        if city.city_name not in all_user_cities:
            all_user_cities.append(city.city_name)
            user_cities.insert(0, city)
    all_user_cities = random.sample(user_cities, 9)
    form = SearchForm()
    if form.validate_on_submit():
        # Ensure capitalized for API request
        city = request.form['city'].capitalize()
        # Get list of first 5 matching cities 
        res = requests.get('https://api.teleport.org/api/cities/', params={'search': city, 'limit':5})
        city_data = res.json()
        app.logger.debug(f'Form CSRF Token: {form.csrf_token.data}')
        # likely different because the CSRF token stored in the session is being regenerated on each request
        app.logger.debug(f'Session CSRF Token: {session["csrf_token"]}')
        app.logger.debug(f'Session Data: {session}')
        for city in city_data['_embedded']['city:search-results']:
            # add city name and image url to results list
            city_results.append((
                city['matching_full_name'], 
                city['_links']['city:item']['href']))
        return render_template('home.html', form=form, cities=city_results, all_user_cities=all_user_cities)
# IF DATABASE IS EMPTY
#  COMMENT OUT LINES 41-46 AND SUB 
# (all_user_cities=all_user_cities) FOR (all_user_cities=all_cities) 
# ON RETURN IN LINES 62 AND 66
    return render_template('home.html', form=form, all_user_cities=all_user_cities)

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Handle user registration.
    - Create a new user and add to db. Redirect to homepage with new user logged in.
    - If form not valid, redirect back to form.
    - If username is unavailable flash message and redirect back to form"""
    form = RegisterUserForm()
    if form.validate_on_submit():
        try:
            # collect information from form
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
            # add user to datadae
            db.session.add(user)
            db.session.commit() 
            # set session['username'] indicating that a user is logged in
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
    app.logger.debug(f'Session Data: {session}')
    form=LoginForm()
    if form.validate_on_submit():
        # validate_csrf(form.csrf_token.data, secret_key=app.secret_key)
        user = User.authenticate(form.username.data, form.password.data)
        app.logger.debug(f'Form CSRF Token: {form.csrf_token.data}')
        app.logger.debug(f'Session CSRF Token: {session["csrf_token"]}')
        app.logger.debug(f'Session Data: {session}')
        
        if user:
            # User.authenticate() will return the username of the authenticated user
            # if user is authenticated set session[username] indicating login 
            session['username']= user
            return redirect('/')
            # handle incorred credentials 
        flash('Incorrect Username or Password!')
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/logout', methods=["POST"])
def logout():
    """handle user logout"""
    # clear the session to indicate log out
    session.pop('username')
    app.logger.debug(f'Session Data: {session}')

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

@app.route('/city/<city>', methods=["GET", "POST"])
def show_city(city):
    """Get all relevant information about a city"""

    # Get City data from Teleport API
    try: 
        res = requests.get('https://api.teleport.org/api/cities/', params={'search': city, 'limit':1})
        city_urls = res.json()
        # get url for city information urls and make request
        city_details_urls =  requests.get(
            city_urls['_embedded']['city:search-results'][0]['_links']['city:item']['href'])
        city_detail_url = city_details_urls.json()
        # get url to city score urls and make request with it
        city_scores_url = requests.get(
            city_detail_url['_links']['city:urban_area']['href'])
        city_data = city_scores_url.json()
        # get actual data from city scores link 
        city_scores = requests.get(city_data['_links']['ua:scores']['href'])
        # get city image from images link 
        city_photos = requests.get(city_data['_links']['ua:images']['href'])
        city_img = city_photos.json()
        city_image = city_img['photos'][0]['image']['web']
        city_name = city_detail_url['full_name']
        city_short_name = city_detail_url['name']
        population = city_detail_url['population']
    

        # make category information accessible 
        city_final = city_scores.json()
        city_cats_data = city_final['categories']
        city_cats={}
        for cat in city_cats_data:
            city_cats.update({cat['name']: int(cat['score_out_of_10'])})
        housing = city_cats['Housing']
        cost = city_cats['Cost of Living']
        startups = city_cats['Startups']
        v_capital= city_cats['Venture Capital']
        travel = city_cats['Travel Connectivity']
        commute = city_cats['Commute']
        safety = city_cats['Safety']
        healthcare = city_cats['Healthcare']
        economy = city_cats['Economy']
        tax = city_cats['Taxation']
        internet = city_cats['Internet Access']
        culture= city_cats['Leisure & Culture']
        environment = city_cats['Environmental Quality']
        summ = city_final['summary']
        # remove written in tags 
        summary = summ.replace('<p>', '').replace('<b>', '').replace('</b>', '').replace('</p>', '').replace('Teleport', '').replace('<i>', '').replace('</i>', '').replace('<br>', '').replace('</br>', '')
    
        # Get timezone and weather data using lat/lon information from teleport api 
        city_lat = city_detail_url['location']['latlon']['latitude']
        city_lon = city_detail_url['location']['latlon']['longitude']
        tz_weather_data = requests.get(f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city_lat},{city_lon}?key=9Z9PX7J5C7ZRC76D38PL4WFL8')
        data = tz_weather_data.json()
        timezone = data['timezone']
        tzoffset = data['tzoffset']
        description = data['days'][0]['description']
        temp = int(data['days'][0]['temp'])
        c_temp = int((temp-32)*5/9)
        # get user timezone info
        user = User.query.filter_by(username = session['username']).first()
        # prep string to become int
        user_tz = user.employer_timezone.replace(':','').replace('00','')
        # calculate time difference 
        
        # added
        print(user_tz)
        time_dif = int(user_tz[:3]) - int(tzoffset)
        print(time_dif)

        #Get Country data using the country the city is in from teleport api 
        country = city_detail_url['_links']['city:country']['name']
        country_link = requests.get(f'https://countryinfoapi.com/api/countries/name/{country}')
        country_data = country_link.json()
        currencies = country_data['currencies']
        currency = str(currencies.keys()).replace("dict_keys(['","").replace("'])","")
        final_currency = currencies[currency]['name']
        curr = final_currency
        languages = country_data['languages'].values()
        driving = country_data['car']['side'].capitalize()
        return render_template('city.html', housing=housing, cost=cost, 
                startups=startups, v_capital=v_capital, travel=travel, 
                commute=commute, saftey=safety, healthcare=healthcare, 
                economy=economy, tax=tax, internet=internet, culture=culture,
                environment=environment, c_temp=c_temp, 
                city_short_name=city_short_name, population=population, 
                user=user, currency=curr, driving=driving, languages=languages, 
                time_dif=time_dif, timezone=timezone, city_image=city_image,
                summary=summary, city_name=city_name, temp=temp, 
                description=description)
    except KeyError:
        flash("We're still working on collecting data for this location!")
        return redirect('/')
    except IndexError:
        flash("We're still working on collecting data for this location!")
        return redirect('/')


@app.route('/save/<city_short_name>', methods=["GET", "POST"])
def save_city(city_short_name):
    """Save a city to user's page while avoiding duplication"""
    user = User.query.filter_by(username = session['username']).first()
    user_cities = User_city.query.filter_by(user_id = user.id).all()
    # get city data from teleport api using the city's short name 
    res = requests.get('https://api.teleport.org/api/cities/', params={'search': city_short_name, 'limit':1})
    city_data = res.json()
    city_scores_link =  requests.get(
        city_data['_embedded']['city:search-results'][0]['_links']['city:item']['href'])
    city_information_url = city_scores_link.json()
    # get city data from urban area link
    city_urban_area_url = requests.get(city_information_url['_links']['city:urban_area']['href'])
    city = city_urban_area_url.json()
    # get city url and image 
    city_images = requests.get(city['_links']['ua:images']['href'])
    city_img = city_images.json()
    city_image = city_img['photos'][0]['image']['web']
    # handle duplication 
    for c in user_cities:
        if c.city_name == city_short_name:
            flash("You've already saved this city!")
            return redirect(f'/user/{user.username}')
    # add city to user_cities 
    add_city = User_city(city_name=city_short_name, city_image=city_image, user_id =user.id)
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
