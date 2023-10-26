from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """connectr to db"""
    db.app=app
    db.init_app(app)

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

    cities = db.relationship('User_city', backref='city_users')

    @classmethod
    def register(cls, username, first_name, last_name, password, employer_timezone):
        """register a user and hash password"""
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode('utf8')
        return cls(username=username, first_name=first_name, last_name=last_name, 
                    password=hashed_utf8, employer_timezone=employer_timezone)
    
    @classmethod
    def authenticate(cls, username, password):
        u = User.query.filter_by(username=username).first()
        if u and bcrypt.check_password_hash(u.password,password):
            return u
        else:
            return False

class User_city(db.Model):
    """User city model"""
    __tablename__ = 'user_cities'
    def __repr__(self):
        return f'{self.city_name}'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_name = db.Column(db.Text, nullable=False)
    city_image = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    visited = db.Column(db.Boolean, nullable=False, default=0)



        












