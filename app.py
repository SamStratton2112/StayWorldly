from flask import Flask, request, jsonify, render_template, redirect, session, g, flash
from models import db, connect_db, User, User_city
from forms import LoginForm, RegisterUserForm, CommentForm, EditUserForm, SearchForm
from sqlalchemy.exc import IntegrityError
import requests
import datetime
# from requestfuncs import get_city_info




app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///travel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config['SECRET_KEY'] = "secret"
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
    form = SearchForm()
    if form.validate_on_submit():
        city = request.form['city'].capitalize()
        res = requests.get('https://api.teleport.org/api/cities/', params={'search': city, 'limit':10})
        city_data = res.json()
        city_results = []
        for city in city_data['_embedded']['city:search-results']:
            city_results.append((city['matching_full_name'], city['_links']['city:item']['href']))
        return render_template('home.html', form=form, cities=city_results)
    return render_template('home.html', form=form)

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Handle user registration.
    Create a new user and add to db. Redirect to homepage with new user logged in.
    If form not valid, redirect back to form.
    If username is unavailable flash message and show form"""
    form = RegisterUserForm()
    if form.validate_on_submit():
        user = User.register(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=form.password.data,
            employer_timezone=form.employer_timezone.data
        )
        db.session.add(user)
        if user:
            db.session.commit() 
            session['username']= user.username
        else:
            flash("Username unavailable")
            return render_template('register.html', form=form)
        return redirect('/')
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
    user = User.query.filter_by(username=username).first()
    user_cities = User_city.query.filter(User.id == user.id).all()
    return render_template('user.html', user=user, user_cities=user_cities)

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
        if User.authenticate(form.username.data, form.password.data):
            db.session.commit()
            return redirect(f'/user/{user.username}')
        else: 
            flash("Incorrect Password!")
            return redirect('/')
    return render_template('edit.html', form=form, user=user)

@app.route('/city/<city>', methods=["GET", "POST"])
def show_city(city):
    """Get all relevant information about a city"""
    # Get City data from Teleport API
    res = requests.get('https://api.teleport.org/api/cities/', params={'search': city, 'limit':1})
    city_data = res.json()
    city_link = city_data['_embedded']['city:search-results'][0]['_links']['city:item']['href'] 
    city_name = city_data['_embedded']['city:search-results'][0]['matching_full_name']
    city_scores_link =  requests.get(city_link)
    city_information = city_scores_link.json()
    city_urban_area = requests.get(city_information['_links']['city:urban_area']['href'])
    city_short_name = city_information['name']
    population = city_information['population']
    city = city_urban_area.json()
    city_scores = requests.get(city['_links']['ua:scores']['href'])
    city_images = requests.get(city['_links']['ua:images']['href'])
    city_img = city_images.json()
    city_image = city_img['photos'][0]['image']['web']
    city_final = city_scores.json()
    city_cats = city_final['categories']
    summ = city_final['summary']
    summ1 = summ.replace('<p>', '')
    summ2 = summ1.replace('<b>', '')
    summ3 = summ2.replace('</b>', '')
    summ4 = summ3.replace('</p>', '')
    summary = summ4.replace('Teleport', '')

    # Get timezone and weather data
    city_lat = city_information['location']['latlon']['latitude']
    city_lon = city_information['location']['latlon']['longitude']
    data = requests.get(f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city_lat},{city_lon}?key=9Z9PX7J5C7ZRC76D38PL4WFL8')
    json_data = data.json()
    timezone = json_data['timezone']
    tzoffset = json_data['tzoffset']
    description = json_data['days'][0]['description']
    temp = json_data['days'][0]['temp']
    user = User.query.filter_by(username = session['username']).first()
    user_tz = user.employer_timezone.replace(':', '').replace('00', '')
    time_dif = int(user_tz) - int(tzoffset)
    # if time_dif< 0:
    #     time_difference = time_dif * -1
    # else:
    #     time_difference=time_dif

    #Get Country info

    country = city_information['_links']['city:country']['name']
    country_link = requests.get(f'https://countryinfoapi.com/api/countries/name/{country}')
    country_data = country_link.json()
    language = country_data['languages']
    languages = language.values()
    print(languages)
    driving = country_data['car']['side']
    currencies = country_data['currencies']
    currency = str(currencies.keys())
    curr = currency.replace("dict_keys(['", "").replace("'])", "")
    return render_template('city.html', city_short_name=city_short_name, population=population, user=user, currency=curr, driving=driving, languages=languages, time_dif=time_dif, timezone=timezone, city_image=city_image, city_cats=city_cats, summary=summary, city_name=city_name, temp=temp, description=description)

@app.route('/save/<city_short_name>', methods=["GET", "POST"])
def save_city(city_short_name):
    user = User.query.filter_by(username = session['username']).first()
    user_cities = User_city.query.filter_by(user_id = user.id).all()
    for city in user_cities:
        if city.city_name == city_short_name:
            flash("You've already saved this city!")
            return redirect(f'/user/{user.username}')
    add_city = User_city(city_name=city_short_name, user_id =user.id)
    db.session.add(add_city)
    db.session.commit()
    return redirect(f'/user/{user.username}')


@app.route('/remove/<city_id>', methods=["GET", "POST"])
def remove_u_city(city_id):
    city = User_city.query.filter_by(id=city_id).first()
    user = session['username']
    db.session.delete(city)
    db.session.commit()
    return redirect(f'/user/{user}')

    #  for city in user.cities:
    #         if city_short_name == city:
    #             flash('You have already saved this city')
    #             return redirect('/')
    #         add_city = User_city(city_name=city_short_name, user_id =user.id)
    #         db.session.add(add_city)
    #         db.session.commit()
    #         return redirect(f'/user/{user.username}')