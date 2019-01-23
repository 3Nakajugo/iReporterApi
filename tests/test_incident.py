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
        self.intervention = {
            "location": 902093392,
            "file": "ed.jpg",
            "comment": "all is well"
        }
        self.redflag = {
            "location": 902093392,
            "file": "ed.jpg",
            "comment": "all is well"
        }
        self.user = {
            "first_name": "nakajugo",
            "last_name": "nakajugo",
            "other_names": "abenaky",
            "email": "ed@gmail.com",
            "telephone": "0781370907",
            "user_name": "nakimari",
            "password": "maria123"
        }
        self.user_credentials = {
            "user_name": "nakimari",
            "password": "maria123"
        }
        self.response = self.test_client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user))
        self.login_response = self.test_client.post(
            '/api/v2/auth/login', data=json.dumps(self.user_credentials), content_type="application/json")
        jwt_token = json.loads(self.login_response.data)["token"]
        self.test_client.post(
            '/api/v2/redlags', headers=dict(Authorization="Bearer " + jwt_token), data=json.dumps(self.redflag))

    def tearDown(self):
        database.drop_tables()

    def test_create_intervention(self):
        """
        test for creating intervention
        """
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.post(
            '/api/v2/interventions', headers=dict(Authorization="Bearer " + jwt_token), data=json.dumps(self.intervention))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response_data["message"],
                         "intervention has been created")
        self.assertEqual(response.status_code, 201)
        self.assertIs(type(response_data), dict)

    def test_get_all_interventions(self):
        """
        test for geting all interventions
        """
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.post('/api/v2/interventions', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json", data=json.dumps(self.intervention))
        response = self.test_client.get('/api/v2/interventions', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_single_intervention_that_doesnot_exist(self):
        """
        test for geting single interventions that doesnot exist
        """
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.get('/api/v2/interventions/100', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_delete_intervention_that_doesnot_exist(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.delete('/api/v2/redflags/5', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json",)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data["status"], 404)
        self.assertEqual(response_data["message"],
                         "no incident with such an id")

    def test_posting_missing_location(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        missing_location = {
            "location": "",
            "file": "ed.jpg",
            "comment": "corruption"
        }
        response = self.test_client.post('/api/v2/interventions', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json", data=json.dumps(missing_location))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "location must be an integer of less then 9 integers")
    

    def test_posting_missing_comment(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        missing_comment = {
            "location": 56778,
            "file": "ed.jpg",
            "comment": ""
        }
        response = self.test_client.post('/api/v2/interventions', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json", data=json.dumps(missing_comment))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "comment is missing")


