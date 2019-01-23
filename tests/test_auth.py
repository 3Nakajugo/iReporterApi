import unittest
import json
from app.views import app
from app.Database.db import Database

database = Database()


class TestApi(unittest.TestCase):
    def setUp(self):
        """
        test for index page
        """
        self.test_client = app.test_client()
        self.user = {
            "first_name": "maria",
            "last_name": "nakajugo",
            "other_names": "abenaky",
            "email": "ed@gmail.com",
            "telephone": "0781370907",
            "user_name": "nakimari",
            "password": "maria123"
        }

    def tearDown(self):
        pass
        database.drop_tables()

    def test_index(self):
        """
        test for welcome page
        """
        response = self.test_client.get('/api/v2/welcome')
        data = json.loads(response.data)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIs(type(response_data), dict)
        self.assertEqual(data['message'], "Welcome to iReporter application")

    def test_signup_user(self):
        """
        test for create user
        """
        response = self.test_client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user))
        response_data = json.loads(response.data.decode())
        self.assertIs(type(response_data), dict)
        self.assertEqual(response.status_code, 201)

    def test_signup_with_invalid_firstname(self):
        """
        test register with invalid firstname
        """
        user = {
            "first_name": "",
            "last_name": "nakajugo",
            "other_names": "abenaky",
            "email": "ed@gmail.com",
            "telephone": "0781370907",
            "user_name": "nakimari",
            "password": "maria123"
        }
        response = self.test_client.post(
            '/api/v2/auth/signup', data=json.dumps(user))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "first_name is missing")

    def test_register_invalid_email(self):
        """
        test register with invalid email
        """
        invalid_email_user = {
            "first_name": "edna",
            "last_name": "nakajugo",
            "other_names": "abenaky",
            "email": "ed@gmail. com",
            "telephone": "0781370907",
            "user_name": "nakimari",
            "password": "maria123"
        }
        response = self.test_client.post(
            '/api/v2/auth/signup', data=json.dumps(invalid_email_user))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "please input valid email")

    def test_register_invalid_password(self):
        """
        test register with invalid password
        """
        invalid_password_user = {
            "first_name": "edna",
            "last_name": "nakajugo",
            "other_names": "abenaky",
            "email": "ed@gmail.com",
            "telephone": "0781370907",
            "user_name": "nakimari",
            "password": "m"
        }
        response = self.test_client.post(
            '/api/v2/auth/signup', data=json.dumps(invalid_password_user))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"],
                         "password must be longer than 8 characters")

    def test_login(self):
        """
        test login
        """
        user = {
            "first_name": "maria",
            "last_name": "nakajugo",
            "other_names": "abenaky",
            "email": "ed@gmail.com",
            "telephone": "0781370907",
            "user_name": "nakimari",
            "password": "maria123"
        }
        credentials = {"user_name": "nakimari",
                       "password": "maria123"}
        response = self.test_client.post(
            '/api/v2/auth/signup', data=json.dumps(user))
        response = self.test_client.post(
            '/api/v2/auth/login', data=json.dumps(credentials))
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_username(self):
        invalid_credentials = {"user_name": "",
                       "password": "maria123"}
        response = self.test_client.post(
            '/api/v2/auth/login', data=json.dumps(invalid_credentials))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"],
                         "username Cannot be empty")

    def test_login_invalid_password(self):
            invalid_credentials = {"user_name":"ednaer",
                        "password": ""}
            response = self.test_client.post(
                '/api/v2/auth/login', data=json.dumps(invalid_credentials))
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response_data["message"],
                            "password cannot be empty")
  
