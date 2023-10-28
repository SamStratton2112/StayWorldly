from unittest import TestCase
from models import db, connect_db, User, User_city
from flask import session 
from app import app

app.config['SQLALCHEMY_DATABASE_URL'] = "postgresql:///test_travel"
app.config['SQLALCHEMY_ECHO']= False
app.config['TESTING']= True

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    """ Test user page"""
    def setUp(self):
        """make a test user"""
        User.query.delete()
        db.session.commit()

        user = User(username='user123', password='password', first_name='first',
            last_name='last', employer_timezone='-08:00')
        user.id = 22 
        db.session.add(user)
        db.session.commit()

        self.u_id = user.id
        print(self.u_id)

    def tearDown(self):
        """remove anything that remains in the session to be committed"""

        db.session.rollback()

    def test_user_cities_model(self):
        """test user save city functionality"""
        u = User(username='testuser', password='password', first_name='first',
            last_name='last', employer_timezone='-11:00')
        u.id = 44
        db.session.add(u)
        db.session.commit()

        new_u_city = User_city(city_name='Paris', city_image="url", user_id=u.id, visited=0)
        db.session.add(new_u_city)
        db.session.commit()
        
        self.assertEqual(len(u.cities), 1)


    def test_remove_city_from_user(self):
        """test removing a city from a user's cities"""
        with app.test_client() as c:
            user = User.query.get(self.u_id)
            with c.session_transaction() as sess:
                sess['username'] = user.username
            new_city = User_city(city_name='Tokyo', city_image="url", user_id=user.id, visited=0)
            new_city.id =222
            db.session.add(new_city)
            db.session.commit()
            resp = c.get('/remove/222')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(len(user.cities), 0)

    def test_mark_city_visited(self):
        """test city marked as visited"""
        with app.test_client() as c:
            user = User.query.get(self.u_id)
            with c.session_transaction() as sess:
                sess['username'] = user.username
            new_city = User_city(city_name='Brooklyn', city_image="url", user_id=user.id, visited=0)
            new_city.id =333
            db.session.add(new_city)
            db.session.commit()
            city = User_city.query.get(333)

            resp = c.post('/city/333/visted')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(city.visited, 1)

    def test_mark_city_not_visited(self):
        """test that a city can be marked as not visited"""
        with app.test_client() as c:
            user = User.query.get(self.u_id)
            with c.session_transaction() as sess:
                sess['username'] = user.username
            new_city = User_city(city_name='Queens', city_image="url", user_id=user.id, visited=1)
            new_city.id =444
            db.session.add(new_city)
            db.session.commit()
            city = User_city.query.get(444)

            resp = c.get('/city/444/notvisted')
            html = resp.get_data(as_text=True)

            self.assertEqual(city.visited, 0)



   




