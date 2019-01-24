import unittest
import json
from app.views import app
from app.Database.db import Database

database = Database()

class TestRedflag(unittest.TestCase):
    def setUp(self):
        """
        test for index page
        """
        database.create_tables()
        self.test_client = app.test_client()
        self.redflag = {
            "location": 902093392,
            "file": "ed.jpg",
            "comment": "all is well"
        }
        self.user = {
            "first_name": "edna",
            "last_name": "nakajugo",
            "other_names": "abenakyo",
            "email": "ed@gmail.com",
            "telephone": "0781370907",
            "user_name": "eddiena",
            "password": "ednanakaju",
            "isadmin":"False"
        }
        self.user_credentials = {
            "user_name": "eddiena",
            "password": "ednanakaju"
        }
        self.response = self.test_client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user))
        self.login_response = self.test_client.post(
            '/api/v2/auth/login', data=json.dumps(self.user_credentials), content_type="application/json")
        jwt_token = json.loads(self.login_response.data)["token"]
        print(jwt_token)
        self.test_client.post(
            '/api/v2/redlags', headers=dict(Authorization="Bearer " + jwt_token), data=json.dumps(self.redflag))

    def tearDown(self):
        database.drop_tables()

    def test_posting_redflag(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.post(
            '/api/v2/redflags', headers=dict(Authorization="Bearer " + jwt_token), data=json.dumps(self.redflag))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response_data["message"],
                         "Redflag has been created")
        self.assertEqual(response.status_code, 201)
        self.assertIs(type(response_data), dict)
    
    def test_get_all_redflags(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.post(
            '/api/v2/redflags', headers=dict(Authorization="Bearer " + jwt_token), data=json.dumps(self.redflag))
        response = self.test_client.get('/api/v2/redflags', headers=dict(Authorization="Bearer " + jwt_token))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIs(type(response_data), dict)

    def test_get_single_redflag_record(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.post(
            '/api/v2/redflags', headers=dict(Authorization="Bearer " + jwt_token), data=json.dumps(self.redflag))
        response = self.test_client.get('/api/v2/redflags/1', headers=dict(Authorization="Bearer " + jwt_token))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIs(type(response_data), dict)
    
    def test_get_single_redflag_that_doesnot_exists(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.get('/api/v2/redflags/1', headers=dict(Authorization="Bearer " + jwt_token))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertIs(type(response_data), dict)
    
    def test_delete_single_redflag(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.post(
            '/api/v2/redflags', headers=dict(Authorization="Bearer " + jwt_token), data=json.dumps(self.redflag))
        response = self.test_client.delete('/api/v2/redflags/1', headers=dict(Authorization="Bearer " + jwt_token))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIs(type(response_data), dict)
    
    # def test_delete_redflag_that_doenot_exist(self):



