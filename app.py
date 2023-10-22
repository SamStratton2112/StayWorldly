from flask import Flask, request, jsonify, render_template, redirect, session, g, flash
from models import db, connect_db, User, City, Country, Timezone, User_city, Comment
from forms import LoginForm, RegistrUserForm, CommentForm
from sqlalchemy.exc import IntegrityError


CURR_USER_KEY = 'curr_user'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///travel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config['SECRET_KEY'] = "secret"
app.app_context().push()


connect_db(app)
db.create_all()

@app.before_request
def add_user_to_g():
    """If a user is logged in, add curr_user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/')
def homepage():
    """Show homepage:
    - if no user is logged in:
        - Navbar shows option to log in/ register 
        - list of citiies to check out
    - if a user is logged in:
        - Navbar shows option to see user page/information
        - list of cities to check out
        - form to search for cities""" 
    return render_template('home.html')

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Handle user registration.
    Create a new user and add to db. Redirect to homepage with new user logged in.
    If form not valid, redirect back to form.
    If username is unavailable flash message and show form"""
    form = RegistrUserForm()
    if form.validate_on_submit():
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
        except IntegrityError:
            flash("Username unavailable")
            return render_template('register.html', form=form)
        session[CURR_USER_KEY] = user.id
        g.user = User.query.get(session[CURR_USER_KEY])
        return redirect('/')
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def do_login():
    """ handle user log in"""
    form=LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            session[CURR_USER_KEY] = user.id
            g.user = User.query.get(session[CURR_USER_KEY])
            return redirect('/')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """handle user logout"""
    session.pop(CURR_USER_KEY)
    return redirect('/')
        
