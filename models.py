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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))




# class Comment(db.Model):
#     """Comment model"""
#     __tablename__ = 'comments'
#     def __repr__(self):
#         return f'<User ID: {self.user_id}, Comment {self.id}, {self.comment}>'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     comment = db.Column(db.String(100), nullable=False)

    # city_comment = db.relationship('City', backref="commentcity")

# class City(db.Model):
#     """City model"""
#     __tablename__ = 'cities'
#     def __repr__(self):
#         return f'<City: {self.id}, name: {self.city_name}>'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     city_name = db.Column(db.Text, nullable=False)
#     population = db.Column(db.Integer, nullable=False)
#     country_name = db.Column(db.Text, nullable=False)
#     saftey_score = db.Column(db.Integer, nullable=False)
#     cost_of_living = db.Column(db.Integer, nullable=False)
#     housing_score = db.Column(db.Integer, nullable=False)
#     healthcare_score = db.Column(db.Integer, nullable=False)
#     economy_score = db.Column(db.Integer, nullable=False)
#     tax_score = db.Column(db.Integer, nullable=False)
#     longitude = db.Column(db.Float, nullable=False)
#     latitude = db.Column(db.Float, nullable=False)
#     summary = db.Column(db.Text, nullable=False)

#     country = db.relationship('Country', backref="countrycity")
#     timezone = db.relationship('Timezone', backref='timezonecity')

# class Country(db.Model):
#     """Country model"""
#     __tablename__ = 'countries'
#     def __repr__(self):
#         return f'<Country: {self.id}, name: {self.country_name}>'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     country_name = db.Column(db.Text, db.ForeignKey('cities.country_name'), nullable=False)
#     continent = db.Column(db.Text, nullable=False)
#     currency = db.Column(db.Text, nullable=False)
#     languages = db.Column(db.Text, nullable=False)
#     drving_side = db.Column(db.Text, nullable=False)
#     flag = db.Column(db.Text, nullable=False, default='https://njq-ip.com/wp-content/uploads/2015/12/Benelux-No-Flag-Available.png')
    
#     country_timezone = db.relationship('Timezone', backref="timezonecountry")

# class Timezone(db.Model):
#     """Timezone model"""
#     __tablename__ = 'timezones'
#     def __repr__(self):
#         return f'<City ID: {self.city_id}, offset: {self.offset}>'
    
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
#     country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
#     offset = db.Column(db.Integer, nullable=False)











