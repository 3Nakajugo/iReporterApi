import unittest
import json
from app.views import app


class TestUser(unittest.TestCase):
    def setUp(self):
        """
        test for index page
        """
        self.test_client = app.test_client()
        self.user = {
            "first_name": "edna",
            "last_name": "mag",
            "other_names": "eddiee",
            "email": "ed@gmail",
            "telephone": "9",
            "user_name": "ednamar",
            "password": "edna123"
        }
        self.invalid_user = {
            "first_name": "edna",
            "last_name": "mag",
            "other_names": "eddiee",
            "email": "ed@gmail",
            "telephone": "9",
            "user_name": "edl",
            "password": "edna123"
        }
        self.incident = {
            "created_by": "edna",
            "incident_type": "redflag",
            "location": "2123 13241",
            "file": "error.png",
            "comment": "jisckmsldkmspoll,ldjo"
        }
        self.wrong_credentials = {
            "user_name": "maredna",
            "password": "edna12"
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

    def test_failed_login(self):
        response = self.test_client.post(
            '/api/v1/auth/login', data=json.dumps(self.wrong_credentials), content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_get_all_users_when_list_empty(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.get('/api/v1/users', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response_data["message"], "No Users to display")

    def test_register_user(self):
        response = self.test_client.post(
            '/api/v1/users/signup', data=json.dumps(self.user))
        request_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(request_data["message"], "User has been created")
        self.assertIs(type(request_data), dict)

    def test_get_all_users(self):
        jwt_token = json.loads(self.login_response.data)["token"]
        response = self.test_client.post('/api/v1/users/signup', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json", data=json.dumps(self.user))
        response = self.test_client.get('/api/v1/users', headers=dict(
            Authorization="Bearer " + jwt_token), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIs(type(response_data), dict)

    def test_invalid_user(self):
        response = self.test_client.post(
            '/api/v1/users/signup', data=json.dumps(self.invalid_user))
        request_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(request_data["message"], "some fields are missing")
        self.assertIs(type(request_data), dict)
