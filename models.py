from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import CSRFProtect

db = SQLAlchemy()
bcrypt = Bcrypt()
csrf = CSRFProtect()

def connect_db(app):
    """function to connect to db"""
    db.app=app
    db.init_app(app)
    csrf.init_app(app)

class User(db.Model):
    """"User model"""
    __tablename__ = 'users'
    def __repr__(self):
        return f'<User {self.id}, username: {self.username}>'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.Text, nullable = False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    employer_timezone = db.Column(db.Text, nullable=True)

    # access cities a user saved and users who have saved a city
    cities = db.relationship('User_city', backref='city_users')

    @classmethod
    def register(cls, username, first_name, last_name, password, employer_timezone):
        """register a user and hash password"""
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode('utf8')
    # return collected information with hashed password, then session.commit()
        return cls(
            username=username, 
            first_name=first_name, 
            last_name=last_name, 
            password=hashed_utf8, 
            employer_timezone=employer_timezone
            )
    
    @classmethod
    def authenticate(cls, username, password):
        # Get user from database
        u = User.query.filter_by(username=username).first()
        # check that the password is correct
        if bcrypt.check_password_hash(u.password, password):
            # set session[username] = u.username and load home page 
            return u
        else:
            # Throw Invalid credentials error 
            return False

class User_city(db.Model):
    # backrefd by Users
    """User city model"""
    __tablename__ = 'user_cities'
    def __repr__(self):
        return f'{self.city_name}'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_name = db.Column(db.Text, nullable=False)
    city_image = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    visited = db.Column(db.Boolean, nullable=False, default=0)