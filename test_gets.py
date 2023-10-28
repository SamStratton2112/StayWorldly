from unittest import TestCase
from models import db, connect_db, User, User_city
from flask import session 
from app import app

app.config['SQLALCHEMY_DATABASE_URL'] = "postgresql:///test_travel"
app.config['SQLALCHEMY_ECHO']= False
app.config['TESTING']= True

db.drop_all()
db.create_all()

class GetTestCase(TestCase):
    """ Test user page"""
    def setUp(self):
        """make a test user"""
        User.query.delete()
        db.session.commit()

        user = User(username='user123', password='password', first_name='first',
            last_name='last', employer_timezone='-08:00')
        db.session.add(user)
        db.session.commit()

        self.u_id = user.id


    def tearDown(self):
        """remove anything that remains in the session to be committed"""
        db.session.rollback()

    def test_home_page(self):
        """test that the home page renders correctly"""
        with app.test_client() as a:
            resp = a.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>Log in or register to find your next adventure!</p>', html)

    def test_show_register_form(self):
        """test that the form renders correctly"""
        with app.test_client() as b:
            resp = b.get('/register')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button>Register</button>', html)

    def test_show_edit_user_form(self):
        """test that the edit form renders correctly"""
        with app.test_client() as c:
            user = User.query.get(self.u_id)
            with c.session_transaction() as sess:
                sess['username'] = user.username
            resp = c.get(f'/user/{user.id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<button><a href="/user/{user.id}">Cancel</a></button>', html)

    def test_show_user(self):
        """test that a user's page renders correctly"""
        with app.test_client() as d:
            u = User.query.get(self.u_id)
            with d.session_transaction() as sess:
                sess['username'] = u.username
            resp = d.get(f'/user/{u.username}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h1>Stay Worldly {u.username}</h1>', html)

    def test_show_city(self):
        """test that a city is added to a user_cities"""
        with app.test_client() as e:
            u = User.query.get(self.u_id)
            with e.session_transaction() as sess:
                sess['username'] = u.username

            resp = e.get('/city/Paris')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li>French</li>', html)

    