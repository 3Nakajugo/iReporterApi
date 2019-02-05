import unittest
import json
from app.views import app
from app.Database.db import Database

database = Database()


class TestIntervention(unittest.TestCase):
    def setUp(self):
        """
        test for index page
        """
        database.create_tables()
        self.test_client = app.test_client()
        self.intervention = {
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
            "isadmin": "False"
        }
        self.user_credentials = {
            "user_name": "eddiena",
            "password": "ednanakaju"
        }
        self.response = self.test_client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user))
        self.login_response = self.test_client.post(
            '/api/v2/auth/login', data=json.dumps(self.user_credentials), content_type="application/json")
        # jwt_token = json.loads(self.login_response.data)["token"]

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

    def test_get_single_intervention_that_exists(self):
        """
        tests get intervention that exists
        """
        jwt_token = json.loads(self.login_response.data)["token"]
        self.test_client.post('/api/v2/interventions', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json", data=json.dumps(self.intervention))
        response = self.test_client.get('/api/v2/interventions/1', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_intervention_that_doesnot_exist(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.delete('/api/v2/interventions/5', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json")

        self.assertEqual(response.status_code, 404)

    def test_delete_intervention_that_exists(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        print("token:", jwt_token)
        post_method = self.test_client.post('/api/v2/interventions', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json", data=json.dumps(self.intervention))
        print("data podted:", post_method.data)
        response = self.test_client.delete('/api/v2/interventions/1', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json")
        print("response", response.data)
        self.assertEqual(response.status_code, 200)

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
        self.assertEqual(
            response_data["message"], "location must be an integer of less then 9 integers")

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

    def test_posting_with_no_file(self):
        """ 
        tests posting empty file
        """
        jwt_token = json.loads(self.login_response.data)["token"]
        missing_file = {
            "location": 56778,
            "file": "",
            "comment": "land slides"
        }
        response = self.test_client.post('/api/v2/interventions', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json", data=json.dumps(missing_file))
        self.assertEqual(response.status_code, 400)

    def test_get_interventions_when_table_empty(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.get('/api/v2/interventions', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_edit_intervention_comment(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        comment = {"comment": "corruption"}
        response = self.test_client.post(
            '/api/v2/interventions', headers=dict(Authorization="Bearer " + jwt_token), data=json.dumps(self.intervention))
        response = self.test_client.patch(
            '/api/v2/interventions/1/comment', headers=dict(Authorization="Bearer " + jwt_token), data=json.dumps(comment))
        self.assertEqual(response.status_code, 200)

    def test_edit_intervention_location(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        location = {"location": 888888}
        response = self.test_client.post(
            '/api/v2/interventions', headers=dict(Authorization="Bearer " + jwt_token), data=json.dumps(self.intervention))
        response = self.test_client.patch(
            '/api/v2/interventions/1/location', headers=dict(Authorization="Bearer " + jwt_token), data=json.dumps(location))
        self.assertEqual(response.status_code, 200)

    def test_eidt_location_intervention_that_doesnot_exist(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        location = {"location": 888888}
        response = self.test_client.patch(
            '/api/v2/interventions/1/location', headers=dict(Authorization="Bearer " + jwt_token), data=json.dumps(location))
        self.assertEqual(response.status_code, 404)

    def test_eidt_comment_intervention_that_doesnot_exist(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        comment = {"comment": "corruption"}
        response = self.test_client.patch(
            '/api/v2/interventions/1/comment', headers=dict(Authorization="Bearer " + jwt_token), data=json.dumps(comment))
        self.assertEqual(response.status_code, 404)

    def test_edit_intervention_with_invalid_location(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        location = {"location": "888888"}
        response = self.test_client.post(
            '/api/v2/interventions', headers=dict(Authorization="Bearer " + jwt_token), data=json.dumps(self.intervention))
        response = self.test_client.patch(
            '/api/v2/interventions/1/location', headers=dict(Authorization="Bearer " + jwt_token), data=json.dumps(location))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_data["message"], "location must be an integer of less then 9 integers")

    def test_update_status(self):
        admin = {
            "first_name": "edna",
            "last_name": "nakajugo",
            "other_names": "abenakyo",
            "email": "ed@gmail.com",
            "telephone": "0781370907",
            "user_name": "admin",
            "password": "mukasajo"
        }
        admin_credentials = {
            "user_name": "admin",
            "password": "mukasajo"
        }
        new_status = {
            "status": "rejected"
        }

        response = self.test_client.post(
            '/api/v2/auth/signup', data=json.dumps(admin))
        login_response = self.test_client.post(
            '/api/v2/auth/login', data=json.dumps(admin_credentials), content_type="application/json")
        jwt_token = json.loads(login_response.data)["token"]
        response = self.test_client.post(
            '/api/v2/interventions', headers=dict(Authorization="Bearer " + jwt_token), data=json.dumps(self.intervention))
        response = self.test_client.patch('/api/v2/interventions/1/status', headers=dict(
            Authorization="Bearer " + jwt_token), data=json.dumps(new_status))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code,200)
        self.assertEqual(response_data["data"][0]["message"],"updated Interventions status")
