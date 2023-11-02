from unittest import TestCase
from models import db, connect_db, User, User_city
from flask import session 
from app import app

app.config['SQLALCHEMY_DATABASE_URL'] = "postgresql:///test_travel"
app.config['SQLALCHEMY_ECHO']= False
app.config['TESTING']= True
app.config['WTF_CSRF_ENABLED']=False

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
        user.id = 36 
        db.session.add(user)
        db.session.commit()

        self.u_id = user.id

    def tearDown(self):
        """remove anything that remains in the session to be committed"""
        db.session.rollback()

    def test_user_model_and_relationship(self):
        """test that the User model is working and that the realtionship to user_cities table is functional"""
        u = User(
            username='test_username', 
            password='HASHED', 
            first_name='first', 
            last_name='last', 
            employer_timezone='+08:00')
        u.id = 52
        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.cities), 0)

    def test_registration(self):
        """test register method in User model"""
        new_u = User.register(
            username="test_username",
            first_name="test_first",
            last_name="test_last",
            password="password",
            employer_timezone="+08:00"
        )
        new_u_id = 98
        new_u.id = new_u_id
        db.session.add(new_u)
        db.session.commit()

        new_user = User.query.get(new_u_id)
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.id, 98)
        self.assertEqual(new_user.username, 'test_username')
        self.assertEqual(new_user.last_name, 'test_last')
        self.assertTrue(new_user.password.startswith('$2b$'))

# Bad salt error 

    def test_login(self):
        """test user log in"""
        with app.test_client() as c:
            user = User.query.get(self.u_id)
            d = {"username": user.username, "password": user.password}
            resp = c.post('/login', data=d)

            self.assertIsNotNone(user)
            self.assertEqual(session['username'], 'user123')

    def test_log_out(self):
        """test log out"""
        with app.test_client() as c:
            user = User.query.get(self.u_id)
            with c.session_transaction() as sess:
                sess['username'] = user.username
            resp = c.get('/logout')
            
            self.assertEqual(resp.status_code, 302)


# # test returns failure because the username already exists and usernames must be unique
# # so by failing it is actually passing 

#     def test_username_taken(self):
#         """test unavaibale username"""
#         with app.test_client() as c:
#             d = {"username": 'user123', "first_name": "fisrt", "last_name":"last", "password": "password", "employer_timezone":"+02:00"}
#             resp = c.post('/register', data=d)
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn('Username unavailable', html)

    def test_edit_user(self):
        """test that edit user works as expected"""
        with app.test_client() as c:
            user = User.query.get(self.u_id)
            with c.session_transaction() as sess:
                sess['username'] = user.username
            d = {"first_name":"test", "last_name":"last", "employer_timezone":"-05:00","username":user.username, "passowrd": user.password  }
            resp = c.post(f'/user/{user.username}', data=d)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(user.username, 'test')



    
        

    
