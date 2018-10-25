"""Tests for Health Tracking Flask app."""

import os, hashlib, base64, json
import AirNOW_mock
import server

from unittest import TestCase
from server import app
from seed import example_data
from flask import session
from sqlalchemy import func

from model import connect_to_db, db
from model import User, UserLog, UserCondition, Condition
from model import Symptom, UserSymptom, SymptomItem
from model import ValueType, UserValueType, ValueItem
from model import CountType, UserCountType, CountItem


class FlaskTestsLogInRegister(TestCase):  
    """Test log in and registration."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # Drop all tables first
        db.drop_all()

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_login_redirect(self):
        """Test log in form with redirects."""

        with self.client as c:
            result = c.post('/process-login',
                            data={"email": "hello@gmail.com", 
                                  "password": "123456"},
                            follow_redirects=True
                            )
            user = User.query.filter(User.email=="hello@gmail.com").one()
            self.assertEqual(session['userid'], user.user_id_pk)
            self.assertIn(b'Log in successful', result.data)
            self.assertIn(b"Welcome Patty", result.data)

    def test_login(self):
        """Test log in form."""

        with self.client as c:
            result = c.post('/process-login',
                            data={"email": "hello@gmail.com", 
                                  "password": "123456"},
                            follow_redirects=False
                            )
            self.assertEqual(result.status_code, 302)

    def test_bad_login_redirect(self):
        """Test log in form with bad user data with redirects."""

        with self.client as c:
            result = c.post('/process-login',
                            data={"email": "hello@gmail.com", 
                                  "password": "1234"},
                            follow_redirects=True
                            )
            self.assertIn(b'Login Failed', result.data)
            self.assertIn(b'Please Login', result.data)

    def test_bad_login(self):
        """Test log in form with bad user data."""

        with self.client as c:
            result = c.post('/process-login',
                            data={"email": "hello@gmail.com", 
                                  "password": "1234"},
                            follow_redirects=False
                            )
            self.assertEqual(result.status_code, 302)

    def test_register_redirect(self):
        """Test registration form with redirects."""

        with self.client as c:
            result = c.post('/process-register',
                            data={"email": "me@gmail.com", 
                                  "password": "123456"},
                            follow_redirects=True
                            )
            user = User.query.filter(User.email=="me@gmail.com").one()
            self.assertEqual(session['userid'], user.user_id_pk)
            self.assertIn(b'New user successfully created', result.data)
            self.assertIn(b"Update your settings", result.data)

    def test_register(self):
        """Test registration form."""

        with self.client as c:
            result = c.post('/process-register',
                            data={"email": "me@gmail.com", 
                                  "password": "123456"},
                            follow_redirects=False
                            )
            self.assertEqual(result.status_code, 302)

    def test_bad_register_redirect(self):
        """Test registration form with bad user data with redirects."""

        with self.client as c:
            result = c.post('/process-register',
                            data={"email": "hello@gmail.com", 
                                  "password": "1234"},
                            follow_redirects=True
                            )
            self.assertIn(b'Account already exists', result.data)
            self.assertIn(b'Please Login', result.data)

    def test_bad_register(self):
        """Test log in form with bad user data."""

        with self.client as c:
            result = c.post('/process-register',
                            data={"email": "hello@gmail.com", 
                                  "password": "1234"},
                            follow_redirects=False
                            )
            self.assertEqual(result.status_code, 302)


class LoggedOutTests(TestCase):
    """Tests for when no one is logged in."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index(self):
        """Test homepage page."""

        result = self.client.get('/')
        self.assertIn(b'About this project', result.data) 

    def test_login_page(self):
        """Test login page."""

        result = self.client.get('/login')
        self.assertIn(b'Please Login', result.data)
        self.assertIn(b'Please Register', result.data)

    def test_settings_redirect(self):
        """Test settings page."""

        result = self.client.get('/settings', follow_redirects=True)
        self.assertIn(b'Not logged in', result.data)        
        self.assertIn(b'Please Login', result.data)

    def test_settings(self):
        """Test settings page."""

        result = self.client.get('/settings', follow_redirects=False)
        self.assertEqual(result.status_code, 302)

    def test_user_page_redirect(self):
        """Test user main page."""

        result = self.client.get('/user/1', follow_redirects=True)
        self.assertIn(b'You do not have permission to view this page', 
                      result.data)
        self.assertIn(b'Please Login', result.data)

    def test_user_page(self):
        """Test user main page."""

        result = self.client.get('/user/1', follow_redirects=False)
        self.assertEqual(result.status_code, 302)

    def test_add_tracking_redirect(self):
        """Test add tracking page."""

        result = self.client.get('/add-tracking', follow_redirects=True)
        self.assertIn(b'You do not have permission to view this page', 
                      result.data)
        self.assertIn(b'Please Login', result.data)

    def test_add_tracking(self):
        """Test add tracking page."""

        result = self.client.get('/add-tracking', follow_redirects=False)
        self.assertEqual(result.status_code, 302)


    def test_stop_tracking_redirect(self):
        """Test stop tracking page."""

        result = self.client.get('/stop-tracking', follow_redirects=True)
        self.assertIn(b'You do not have permission to view this page', 
                      result.data)
        self.assertIn(b'Please Login', result.data)

    def test_stop_tracking_page(self):
        """Test stop tracking page."""

        result = self.client.get('/stop-tracking', follow_redirects=False)
        self.assertEqual(result.status_code, 302)


    def test_query_redirect(self):
        """Test query page."""

        result = self.client.get('/query', follow_redirects=True)
        self.assertIn(b'You do not have permission to view this page', 
                      result.data)
        self.assertIn(b'Please Login', result.data)

    def test_query_page(self):
        """Test query page."""

        result = self.client.get('/query', follow_redirects=False)
        self.assertEqual(result.status_code, 302)


class LoggedInTests(TestCase):
    """Tests for when a user is logged in."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['userid'] = 2

    def test_logout_redirect(self):
        """Test logout route with redirects."""

        with self.client as c:        
            result = c.get('/logout', follow_redirects=True)

            self.assertNotIn(b'userid', session)
            self.assertIn(b'Logged out', result.data)
            self.assertIn(b'Please Login', result.data)

    def test_logout(self):
        """Test logout route."""

        result = self.client.get('/logout', follow_redirects=False)
        self.assertEqual(result.status_code, 302)

    def test_index(self):
        """Test homepage page."""

        result = self.client.get('/')
        self.assertIn(b'About this project', result.data) 

    def test_login_page(self):
        """Test login page."""

        result = self.client.get('/login', follow_redirects=False)
        self.assertEqual(result.status_code, 302)


    def test_wrong_user_page(self):
        """Test user main page for wrong user."""

        result = self.client.get('/user/1', follow_redirects=False)
        self.assertEqual(result.status_code, 302)


class LoggedInTestsDatabase(TestCase):
    """Tests for when a user is logged in."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['userid'] = 2

        # Connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # Drop all tables first
        db.drop_all()

        # Create tables and add sample data
        db.create_all()
        example_data()            

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_login_page_redirect(self):
        """Test login page."""

        result = self.client.get('/login', follow_redirects=True)
        self.assertIn(b'Welcome Patty', result.data)

    def test_settings(self):
        """Test settings page."""

        result = self.client.get('/settings')
        self.assertIn(b'Update your settings', result.data)        
        self.assertIn(b'Patty', result.data)

    def test_user_page(self):
        """Test user main page without date."""

        result = self.client.get('/user/2')
        self.assertIn(b'Welcome Patty', result.data)

    def test_user_page_date(self):
        """Test user main page with date."""

        result = self.client.get('/user/2/2018-10-17')
        self.assertIn(b'Welcome Patty', result.data)

    def test_wrong_user_page_redirect(self):
        """Test user main page for wrong user."""

        result = self.client.get('/user/1', follow_redirects=True)
        self.assertIn(b'You do not have permission to view this page', 
                      result.data)
        self.assertIn(b'Welcome Patty', result.data)

    def test_add_tracking(self):
        """Test add tracking page."""

        result = self.client.get('/add-tracking')
        self.assertIn(b'Choose a new condition', result.data)
        self.assertIn(b'Asthma', result.data)

    def test_stop_tracking(self):
        """Test stop tracking page."""

        result = self.client.get('/stop-tracking')
        self.assertIn(b'Choose a condition to stop tracking', result.data)
        self.assertIn(b'Asthma', result.data)

    def test_query(self):
        """Test query page."""

        result = self.client.get('/query')
        self.assertIn(b'Choose a symptom to query on', result.data)
        self.assertIn(b'AQI', result.data)

    def test_process_settings_same_email(self):
        """Test update user settings (other than password), keep email"""

        with self.client as c:
            c.post('/process-settings', 
                   data={"email": "hello@gmail.com",
                         "fname": "Patricia",
                         "lname": "Pint",
                         "zipcode": 94105})

            user = User.query.get(2)
            self.assertEqual("hello@gmail.com", user.email)
            self.assertEqual("Patricia", user.fname) 
            self.assertEqual("Pint", user.lname) 
            self.assertEqual("94105", user.zipcode)                         

    def test_process_settings_new_email(self):
        """Test update user settings (other than password), change email"""

        with self.client as c:
            c.post('/process-settings', 
                   data={"email": "me@gmail.com",
                         "fname": "Patricia",
                         "lname": "Pint",
                         "zipcode": 94105})

            user = User.query.get(2)
            self.assertEqual("me@gmail.com", user.email)
            self.assertEqual("Patricia", user.fname) 
            self.assertEqual("Pint", user.lname) 
            self.assertEqual("94105", user.zipcode)

    def test_process_settings_bad_email(self):
        """Test update user settings (other than password), bad email"""

        with self.client as c:
            c.post('/process-settings', 
                   data={"email": "hi@gmail.com",
                         "fname": "Patricia",
                         "lname": "Pint",
                         "zipcode": 94105})

            user = User.query.get(2)
            self.assertNotEqual("hi@gmail.com", user.email)
            self.assertNotEqual("Patricia", user.fname) 
            self.assertNotEqual("Pint", user.lname) 
            self.assertNotEqual("94105", user.zipcode)

    def test_update_password(self):
        """Test update password route with correct current password"""

        with self.client as c:
            c.post('/update-password',
                   data={"currentPassword": "123456", 
                         "newPassword": "12322",
                         "newPassword2": "12322"})

            user = User.query.get(2)
            hashed = hashlib.sha512("12322".encode() + user.salt.encode())
            hashed_str = base64.urlsafe_b64encode(hashed.digest()).decode()

            self.assertEqual(hashed_str, user.passhash)

    def test_update_wrong_password(self):
        """Test update password route given wrong current password"""

        with self.client as c:
            c.post('/update-password',
                   data={"currentPassword": "1234", 
                         "newPassword": "12322",
                         "newPassword2": "12322"})

            user = User.query.get(2)
            hashed = hashlib.sha512("12322".encode() + user.salt.encode())
            hashed_str = base64.urlsafe_b64encode(hashed.digest()).decode()

            self.assertNotEqual(hashed_str, user.passhash)

    def test_update_password_newwrong(self):
        """Test update password route given new passwords that don't match"""

        with self.client as c:
            c.post('/update-password',
                   data={"currentPassword": "123456", 
                         "newPassword": "1232",
                         "newPassword2": "12322"})

            user = User.query.get(2)
            hashed = hashlib.sha512("1232".encode() + user.salt.encode())
            hashed_str = base64.urlsafe_b64encode(hashed.digest()).decode()
            hashed2 = hashlib.sha512("12322".encode() + user.salt.encode())
            hashed_str2 = base64.urlsafe_b64encode(hashed2.digest()).decode()

            self.assertNotEqual(hashed_str, user.passhash)
            self.assertNotEqual(hashed_str2, user.passhash)

    def test_get_user_symptom(self):
        """Test get user symptom from database"""

        result = self.client.get('/get-user-symptom',
                                 query_string={"user_symptom_id": 9,
                                               "date": "2018-10-07"})

        self.assertEqual(b"True", result.data)


    def test_get_user_no_symptom(self):
        """Test get user symptom that doesn't exist in database"""

        result = self.client.get('/get-user-symptom',
                                 query_string={"user_symptom_id": 9,
                                               "date": "2018-09-07"})

        self.assertEqual(b"False", result.data)

    def test_get_user_value_item(self):
        """Test get user value item from database"""

        result = self.client.get('/get-user-value-item',
                                 query_string={"user_value_id": 2,
                                               "date": "2018-10-07"})

        self.assertEqual(b"80", result.data)

    def test_get_user_no_value_item(self):
        """Test get user value item that doesn't exist in database"""

        result = self.client.get('/get-user-value-item',
                                 query_string={"user_value_id": 2,
                                               "date": "2018-09-07"})

        self.assertEqual(b"False", result.data)

    def test_get_user_count_item(self):
        """Test get user count item from database"""

        result = self.client.get('/get-user-count-item',
                                 query_string={"user_count_id": 3,
                                               "date": "2018-10-07"})

        self.assertEqual(b"1", result.data)

    def test_get_user_no_count_item(self):
        """Test get user count item that doesn't exist in database"""

        result = self.client.get('/get-user-count-item',
                                 query_string={"user_count_id": 3,
                                               "date": "2018-09-07"})

        self.assertEqual(b"False", result.data)

    def test_get_user_log(self):
        """Test get user log item from database"""

        result = self.client.get('/get-user-log',
                                 query_string={"date": "2018-10-07"})

        self.assertEqual(b"Coming down with a cold", result.data)

    def test_get_user_no_log(self):
        """Test get user log item that doesn't exist in database"""

        result = self.client.get('/get-user-log',
                                 query_string={"date": "2018-09-07"})

        self.assertEqual(b"False", result.data)

    def test_get_cond_desc(self):
        """Test get user condition description from database"""

        result = self.client.get('/get-condition-desc',
                                 query_string={"cond_id": 2})

        self.assertEqual(b"Severe headaches", result.data)

    def test_get_cond_desc_none(self):
        """Test get user condition description from database"""

        result = self.client.get('/get-condition-desc',
                                 query_string={"cond_id": 4})

        self.assertEqual(b"n/a", result.data)

    def test_get_tracked_cond_desc(self):
        """Test get tracked user condition description from database"""

        result = self.client.get('/get-tracked-condition-desc',
                                 query_string={"usercond_id": 3})

        self.assertEqual(b"Condition with swollen and narrowed airways", result.data)

    def test_get_tracked_cond_desc_none(self):
        """Test get tracked user condition description from database"""

        result = self.client.get('/get-tracked-condition-desc',
                                 query_string={"usercond_id": 4})

        self.assertEqual(b"n/a", result.data)        

    def test_update_user_symptom_true(self):
        """Test update user symptom for existing record in database"""

        user_symptom_id = 9
        date = "2018-10-07"
        TF = "true"

        with self.client as c:
            result = c.post('/update-user-symptom',
                   data={"user_symptom_id": user_symptom_id, 
                         "date": date,
                         "TF": TF})

            datarecord = (SymptomItem.query
                          .filter(SymptomItem.user_symptom_id==user_symptom_id,
                                  func.date(SymptomItem.symptom_date)==date)
                          .one())

            self.assertEqual(b"Record Updated", result.data)
            self.assertEqual(True, datarecord.symptom_present)

    def test_update_user_symptom_false(self):
        """Test update user symptom for existing record in database"""

        user_symptom_id = 9
        date = "2018-10-07"
        TF = "false"

        with self.client as c:
            result = c.post('/update-user-symptom',
                   data={"user_symptom_id": user_symptom_id, 
                         "date": date,
                         "TF": TF})

            datarecord = (SymptomItem.query
                          .filter(SymptomItem.user_symptom_id==user_symptom_id,
                                  func.date(SymptomItem.symptom_date)==date)
                          .one())

            self.assertEqual(b"Record Updated", result.data)
            self.assertEqual(False, datarecord.symptom_present)

    def test_update_user_symptom_add(self):
        """Test update user symptom for new record in database"""

        user_symptom_id = 9
        date = "2018-09-07"
        TF = "true"

        with self.client as c:
            result = c.post('/update-user-symptom',
                   data={"user_symptom_id": user_symptom_id, 
                         "date": date,
                         "TF": TF})

            datarecord = (SymptomItem.query
                          .filter(SymptomItem.user_symptom_id==user_symptom_id,
                                  func.date(SymptomItem.symptom_date)==date)
                          .one())

            self.assertEqual(b"Record Added", result.data)
            self.assertEqual(True, datarecord.symptom_present)

    def test_update_user_value_item(self):
        """Test update user value item in database"""

        user_value_id = 2
        date = "2018-10-07"
        value = 100.

        with self.client as c:
            result = c.post('/update-user-value-item',
                   data={"user_value_id": user_value_id, 
                         "date": date,
                         "value": value})

            datarecord = (ValueItem.query
                          .filter(ValueItem.user_value_id==user_value_id,
                                  func.date(ValueItem.value_date)==date)
                          .one())

            self.assertEqual(b"Record Updated", result.data)
            self.assertEqual(value, datarecord.value)

    def test_update_user_value_item_add(self):
        """Test add user value item in database"""

        user_value_id = 2
        date = "2018-09-07"
        value = ""

        with self.client as c:
            result = c.post('/update-user-value-item',
                   data={"user_value_id": user_value_id, 
                         "date": date,
                         "value": value})

            datarecord = (ValueItem.query
                          .filter(ValueItem.user_value_id==user_value_id,
                                  func.date(ValueItem.value_date)==date)
                          .one())

            self.assertEqual(b"Record Added", result.data)
            self.assertEqual(None, datarecord.value)

    def test_update_user_count_item(self):
        """Test update user count item in database"""

        user_count_id = 3
        date = "2018-10-07"
        count = 3

        with self.client as c:
            result = c.post('/update-user-count-item',
                   data={"user_count_id": user_count_id, 
                         "date": date,
                         "count": count})

            datarecord = (CountItem.query
                          .filter(CountItem.user_count_id==user_count_id,
                                  func.date(CountItem.count_date)==date)
                          .one())

            self.assertEqual(b"Record Updated", result.data)
            self.assertEqual(count, datarecord.count)

    def test_update_user_count_item_add(self):
        """Test add user count item in database"""

        user_count_id = 3
        date = "2018-09-07"
        count = 5

        with self.client as c:
            result = c.post('/update-user-count-item',
                   data={"user_count_id": user_count_id, 
                         "date": date,
                         "count": count})

            datarecord = (CountItem.query
                          .filter(CountItem.user_count_id==user_count_id,
                                  func.date(CountItem.count_date)==date)
                          .one())

            self.assertEqual(b"Record Added", result.data)
            self.assertEqual(count, datarecord.count)

    def test_update_user_log(self):
        """Test update user log item in database"""

        date = "2018-10-07"
        text = "So tired"

        with self.client as c:
            result = c.post('/update-user-log',
                   data={"date": date,
                         "text": text})

            datarecord = (UserLog.query
                          .filter(func.date(UserLog.log_date)==date,
                                  UserLog.user_id==2)
                          .one())

            self.assertEqual(b"Record Updated", result.data)
            self.assertEqual(text, datarecord.log_text)

    def test_update_user_log_add(self):
        """Test add user log item in database"""

        date = "2018-09-07"
        text = "So tired"

        with self.client as c:
            result = c.post('/update-user-log',
                   data={"date": date,
                         "text": text})

            datarecord = (UserLog.query
                          .filter(func.date(UserLog.log_date)==date,
                                  UserLog.user_id==2)
                          .one())

            self.assertEqual(b"Record Added", result.data)
            self.assertEqual(text, datarecord.log_text)


class LoggedInTestsDatabaseAPI(TestCase):
    """Tests for when a user is logged in."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['userid'] = 2

        # Connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # Drop all tables first
        db.drop_all()

        # Create tables and add sample data
        db.create_all()
        example_data()

        def _mock_get_airnow_data(url, payload):
            if payload.get('date'):
                if payload['zipCode'] == "02738":
                    return AirNOW_mock.previous_02738
                elif payload['zipCode'] == "94030":
                    return AirNOW_mock.previous_94030
                else:
                    return AirNOW_mock.bad_zip
            else:
                if payload['zipCode'] == "02738":
                    return AirNOW_mock.current_02738
                elif payload['zipCode'] == "94030":
                    return AirNOW_mock.current_94030
                else:
                    return AirNOW_mock.bad_zip

        server.get_airnow_data = _mock_get_airnow_data            

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_airnow_api_add(self):
        """Test airnow api add value with input zip"""

        user_value_id = 2
        date = "2018-10-24"
        zipcode = "94030"

        with self.client as c:
            result = c.post('/update-airnow-item',
                       data={"user_value_id": user_value_id, 
                             "date": date,
                             "zipcode": zipcode})

            r = json.loads(result.data.decode())

            datarecord = (ValueItem.query
                          .filter(ValueItem.user_value_id==user_value_id,
                                  func.date(ValueItem.value_date)==date)
                          .one())

            self.assertEqual(datarecord.value, r[0])
            self.assertEqual("Record Added", r[1])

    def test_airnow_api_update(self):
        """Test airnow api update value with input zip"""

        user_value_id = 2
        date = "2018-10-01"
        zipcode = "94030"

        with self.client as c:
            result = c.post('/update-airnow-item',
                       data={"user_value_id": user_value_id, 
                             "date": date,
                             "zipcode": zipcode})

            r = json.loads(result.data.decode())

            datarecord = (ValueItem.query
                          .filter(ValueItem.user_value_id==user_value_id,
                                  func.date(ValueItem.value_date)==date)
                          .one())

            self.assertEqual(datarecord.value, r[0])
            self.assertEqual("Record Updated", r[1])

    def test_airnow_api_add_default(self):
        """Test airnow api add value with default zip"""

        user_value_id = 2
        date = "2018-10-24"

        with self.client as c:
            result = c.post('/update-airnow-item',
                       data={"user_value_id": user_value_id, 
                             "date": date})

            r = json.loads(result.data.decode())

            datarecord = (ValueItem.query
                          .filter(ValueItem.user_value_id==user_value_id,
                                  func.date(ValueItem.value_date)==date)
                          .one())

            self.assertEqual(datarecord.value, r[0])
            self.assertEqual("Record Added", r[1])

    def test_airnow_api_update_default(self):
        """Test airnow api update value with default zip"""

        user_value_id = 2
        date = "2018-10-01"

        with self.client as c:
            result = c.post('/update-airnow-item',
                       data={"user_value_id": user_value_id, 
                             "date": date})

            r = json.loads(result.data.decode())

            datarecord = (ValueItem.query
                          .filter(ValueItem.user_value_id==user_value_id,
                                  func.date(ValueItem.value_date)==date)
                          .one())

            self.assertEqual(datarecord.value, r[0])
            self.assertEqual("Record Updated", r[1])

    def test_airnow_api_badzip(self):
        """Test airnow api with bad zip"""

        user_value_id = 2
        date = "2018-10-24"
        zipcode = "as65aew"

        with self.client as c:
            result = c.post('/update-airnow-item',
                       data={"user_value_id": user_value_id, 
                             "date": date,
                             "zipcode": zipcode})

            r = json.loads(result.data.decode())

            self.assertEqual(None, r[0])
            self.assertEqual("Failed to create AQI record", r[1])


class LoggedInUser3TestsDatabaseAPI(TestCase):
    """Tests for when a user is logged in."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['userid'] = 3

        # Connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # Drop all tables first
        db.drop_all()

        # Create tables and add sample data
        db.create_all()
        example_data()

        def _mock_get_airnow_data(url, payload):
            if payload.get('date'):
                if payload['zipCode'] == "02738":
                    return AirNOW_mock.previous_02738
                elif payload['zipCode'] == "94030":
                    return AirNOW_mock.previous_94030
                else:
                    return AirNOW_mock.bad_zip
            else:
                if payload['zipCode'] == "02738":
                    return AirNOW_mock.current_02738
                elif payload['zipCode'] == "94030":
                    return AirNOW_mock.current_94030
                else:
                    return AirNOW_mock.bad_zip

        server.get_airnow_data = _mock_get_airnow_data            

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_airnow_api_nozip(self):
        """Test airnow api logic with no user zip and no input zip"""

        user_value_id = 2
        date = "2018-10-24"

        with self.client as c:
            result = c.post('/update-airnow-item',
                       data={"user_value_id": user_value_id, 
                             "date": date})

            r = json.loads(result.data.decode())

            self.assertEqual(None, r[0])
            self.assertEqual("Failed to create AQI record", r[1])



#######################################################

if __name__ == "__main__":
    
    import unittest
    unittest.main()