import unittest
import json
from app.views import app


class TestApi(unittest.TestCase):
    def setUp(self):
        """
        test for index page
        """
        self.test_client = app.test_client()
        self.incident = {
            "created_by": "edna",
            "incident_type": "redflag",
            "location": "2123 13241",
            "file": "error.png",
            "comment": "jisckmsldkmspoll,ldjo"
        }
        self.incident_missing = {
            "created_by": "edna",
            "incident_type": "redflag",
            "file": "error.png",
            "comment": "jisckmsldkmspoll,ldjo"
        }
        self.user = {
            "first_name": "edna",
            "last_name": "mag",
            "other_names": "eddiee",
            "email": "ed@gmail",
            "telephone": "9",
            "user_name": "ednamar",
            "password": "edna123"
        }
        self.credentials = {
            "user_name": "ednamar",
            "password": "edna123"
        }
        self.test_client.post(
            '/api/v1/users/signup', data=json.dumps(self.user))
        self.login_response = self.test_client.post(
            '/api/v1/auth/login', data=json.dumps(self.credentials), content_type="application/json")
        jwt_token = json.loads(self.login_response.data)["token"]
        self.test_client.post(
            '/api/v1/incidents', headers=dict(Authorization="Bearer " + jwt_token), data=json.dumps(self.incident))

    def tearDown(self):
        self.incident = None

    def test_index(self):
        """
        test for welcome page
        """
        response = self.test_client.get('/api/v1/welcome')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], "Welcome to iReporter")

    def test_create_incident(self):
        """ 
        test for creating incident
        """
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.post(
            '/api/v1/incidents', headers=dict(Authorization="Bearer " + jwt_token), data=json.dumps(self.incident))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response_data["data"], [
            {
                "message": "incident redflag has been created"
            }
        ])
        self.assertEqual(response.status_code, 201)

    def test_get_all_redflags(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.post('/api/v1/incidents', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json", data=json.dumps(self.incident))
        response = self.test_client.get('/api/v1/incidents', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_all_when_list_is_empty(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.get('/api/v1/incidents',  headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_single_redflag_that_doesnot_exist(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.get('/api/v1/incidents/100', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_get_single_redflag_that_exist(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.post('/api/v1/incidents', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json", data=json.dumps(self.incident))
        response = self.test_client.get('/api/v1/incidents/2', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json")
        request_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIs(type(request_data), dict)

    def test_delete_redflag(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.post('/api/v1/incidents', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json", data=json.dumps(self.incident))

        response = self.test_client.delete('/api/v1/incidents/1', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json",)
        request_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request_data["status"], 200)
        self.assertEqual(request_data["data"], [
            {
                "id": 1,
                "message": "red-flag record has been deleted"
            }
        ])
        self.assertIs(type(request_data), dict)

    def test_delete_redflag_that_doesnot_exist(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.delete('/api/v1/incidents/5', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json",)
        request_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(request_data["status"], 404)
        self.assertEqual(request_data["message"],
                         "no incident with such an id")

    def test_posting_missing_field(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.post('/api/v1/incidents', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json", data=json.dumps(self.incident_missing))
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "some fields are empty")

    def test_edit_location_of_redlag_that_doesnot_exist(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        edit_location = {"location": "ntinda"}
        response = self.test_client.patch('/api/v1/incidents/78/location', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json", data=json.dumps(edit_location))
        self.assertEqual(response.status_code, 404)

    def test_edit_location_of_redlag_that_exists(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.post('/api/v1/incidents', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json", data=json.dumps(self.incident))
        edit_location = {"location": "ntinda"}
        response = self.test_client.patch('/api/v1/incidents/2/location', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json", data=json.dumps(edit_location))
        self.assertEqual(response.status_code, 200)

    def test_edit_comment_that_exists(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.post('/api/v1/incidents', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json", data=json.dumps(self.incident))
        edit_comment = {"comment": "comment changed"}
        response = self.test_client.patch('/api/v1/incidents/2/comment', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json", data=json.dumps(edit_comment))
        self.assertEqual(response.status_code, 200)

    def test_edit_comment_that_doesnot_exists(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        edit_comment = {"comment": "comment changed"}
        response = self.test_client.patch('/api/v1/incidents/200/comment', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json", data=json.dumps(edit_comment))
        self.assertEqual(response.status_code, 404)
