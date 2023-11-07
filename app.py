from flask import Flask, request, render_template, redirect, session, flash
from models import db, connect_db, User, User_city
from forms import LoginForm, RegisterUserForm, CommentForm, EditUserForm, SearchForm
import sqlalchemy
import requests
import datetime
import random
from sqlalchemy.exc import IntegrityError
import os 




app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///travel'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True
# app.config['SECRET_KEY'] = 'secret'
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

app.app_context().push()


connect_db(app)

db.create_all()

@app.route('/', methods=["GET", "POST"])
def homepage():
    """Show homepage:
    - if no user is logged in:
        - Navbar shows option to log in/ register 
        - list of citiies to check out
    - if a user is logged in:
        - Navbar shows option to see user page/information
        - list of cities to check out
        - form to search for cities"""

    all_cities = User_city.query.all()
    all_user_cities = []
    user_cities = []
    for city in all_cities:
        if city.city_name not in all_user_cities:
            all_user_cities.append(city.city_name)
            user_cities.insert(0, city)
    all_user_cities = user_cities[:9:]
    form = SearchForm()
    if form.validate_on_submit():
        city = request.form['city'].capitalize()
        res = requests.get('https://api.teleport.org/api/cities/', params={'search': city, 'limit':5})
        city_data = res.json()
        city_results = []
        for city in city_data['_embedded']['city:search-results']:
            city_results.append((city['matching_full_name'], city['_links']['city:item']['href']))
        return render_template('home.html', form=form, cities=city_results, all_user_cities=all_user_cities)
    return render_template('home.html', form=form, all_user_cities=all_user_cities)


@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Handle user registration.
    Create a new user and add to db. Redirect to homepage with new user logged in.
    If form not valid, redirect back to form.
    If username is unavailable flash message and redirect back to form"""
    form = RegisterUserForm()
    if form.validate_on_submit():
        print('validated')
        try:
            user = User.register(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=form.password.data,
            employer_timezone=form.employer_timezone.data
            )
            db.session.add(user)
            db.session.commit() 
            session['username']= user.username
            return redirect('/')
        except IntegrityError:
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
            session['username']= user.username
            return redirect('/')
        flash('Incorrect Username or Password!')
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """handle user logout"""
    session.pop('username')
    return redirect('/')

@app.route('/user/<username>', methods=["GET", "POST"])
def show_user(username):
    """show user page"""
    if 'username' not in session:
        flash("Access Denied")
        return redirect('/')
    user = User.query.filter_by(username = session['username']).first()
    user_cities = User_city.query.filter_by(user_id = user.id).all()
    visited = []
    to_visit = []
    for city in user_cities:
        if city.visited == 0:
            to_visit.append(city)
        else:
            visited.append(city)
    return render_template('user.html', user=user, visited=visited, to_visit=to_visit)

@app.route('/user/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    """edit user details"""
    if 'username' not in session:
        flash("Access Denied")
        return redirect('/')
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.employer_timezone = form.employer_timezone.data
        if User.authenticate(session['username'], form.password.data):
            db.session.commit()
            return redirect(f'/user/{user.username}')
        else: 
            flash("Incorrect Password!")
            return redirect(f'/user/{user.username}')
    return render_template('edit.html', form=form, user=user)

@app.route('/city/<city>', methods=["GET", "POST"])
def show_city(city):
    """Get all relevant information about a city"""

    # Get City data from Teleport API
    try: 
        res = requests.get('https://api.teleport.org/api/cities/', params={'search': city, 'limit':1})
        city_data = res.json()
        city_name = city_data['_embedded']['city:search-results'][0]['matching_full_name']
        # get the link the the cities data stored in other links 
        city_link = city_data['_embedded']['city:search-results'][0]['_links']['city:item']['href'] 
        city_scores_data =  requests.get(city_link)
        city_information = city_scores_data.json()
        city_short_name = city_information['name']
        population = city_information['population']
        # get the link to city scores data
        city_urban_area = requests.get(city_information['_links']['city:urban_area']['href'])
        city = city_urban_area.json()
        # get actual data from city scores link 
        city_scores = requests.get(city['_links']['ua:scores']['href'])
        # get city images
        city_images = requests.get(city['_links']['ua:images']['href'])
        city_img = city_images.json()
        city_image = city_img['photos'][0]['image']['web']

        # get categories to display
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
        city_lat = city_information['location']['latlon']['latitude']
        city_lon = city_information['location']['latlon']['longitude']
        data = requests.get(f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city_lat},{city_lon}?key=9Z9PX7J5C7ZRC76D38PL4WFL8')
        json_data = data.json()
        timezone = json_data['timezone']
        tzoffset = json_data['tzoffset']
        description = json_data['days'][0]['description']
        temp = int(json_data['days'][0]['temp'])
        c_temp = int((temp-32)*5/9)
        user = User.query.filter_by(username = session['username']).first()
        user_tz = user.employer_timezone.replace(':', '').replace('00', '')
        time_dif = int(user_tz) - int(tzoffset)

        #Get Country data using the country the city is in from teleport api 
        country = city_information['_links']['city:country']['name']
        country_link = requests.get(f'https://countryinfoapi.com/api/countries/name/{country}')
        country_data = country_link.json()
        language = country_data['languages']
        languages = language.values()
        driving = country_data['car']['side'].capitalize()
        currencies = country_data['currencies']
        currency = str(currencies.keys()).replace("dict_keys(['", "").replace("'])", "")
        final_currency = currencies[currency]['name']
        curr = final_currency
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
    city_link = city_data['_embedded']['city:search-results'][0]['_links']['city:item']['href'] 
    city_scores_link =  requests.get(city_link)
    city_information = city_scores_link.json()
    # get city data from urban area link
    city_urban_area = requests.get(city_information['_links']['city:urban_area']['href'])
    city = city_urban_area.json()
    city_images = requests.get(city['_links']['ua:images']['href'])
    city_img = city_images.json()
    city_image = city_img['photos'][0]['image']['web']
    for c in user_cities:
        if c.city_name == city_short_name:
            flash("You've already saved this city!")
            return redirect(f'/user/{user.username}')
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
    """remove city from user cities list and save the city as visited"""
    city = User_city.query.filter_by(id=city_id).first()
    user = session['username']
    city.visited = 1
    db.session.add(city)
    db.session.commit()
    return redirect(f'/user/{user}')   

@app.route('/city/<int:city_id>/notvisited', methods=["GET", "POST"])
def mark_city_as_not_visited(city_id):
    """remove city from user cities list and save the city as visited"""
    city = User_city.query.filter_by(id=city_id).first()
    user = session['username']
    city.visited = 0
    db.session.add(city)
    db.session.commit()
    return redirect(f'/user/{user}') 
