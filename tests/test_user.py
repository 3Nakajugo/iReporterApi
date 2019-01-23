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
            "first_name": "nakajugo",
            "last_name": "mag",
            "other_names": "eddiee",
            "email": "ed@gmail",
            "telephone": "9",
            "user_name": "nakajugo",
            "password": "edna1234"
        }
        self.user_invalid_username = {
            "first_name": "edna",
            "last_name": "mag",
            "other_names": "eddiee",
            "email": "ed@gmail",
            "telephone": "9",
            "user_name": "edl",
            "password": "edna1234"
        }
        self.user_invalid_password = {
            "first_name": "edna",
            "last_name": "mag",
            "other_names": "eddiee",
            "email": "ed@gmail",
            "telephone": "9",
            "user_name": "nakajugo",
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
        self.missing_login_credentials = {
            "user_name": "",
            "password": "edna12"
        }
        self.credentials = {
            "user_name": "ednamar",
            "password": "edna1234"
        }
        self.test_client.post(
            '/api/v1/auth/signup', data=json.dumps(self.user))
        self.login_response = self.test_client.post(
            '/api/v1/auth/login', data=json.dumps(self.credentials), content_type="application/json")
        jwt_token = json.loads(self.login_response.data)["token"]
        self.test_client.post(
            '/api/v1/redflags', headers=dict(Authorization="Bearer " + jwt_token), data=json.dumps(self.incident))

    # def test_failed_login(self):
    #     response = self.test_client.post(
    #         '/api/v1/auth/login', data=json.dumps(self.wrong_credentials), content_type="application/json")
    #     self.assertEqual(response.status_code, 401)

    # def test_login_empty_credentilas(self):
    #     response = self.test_client.post(
    #         '/api/v1/auth/login', data=json.dumps(self.missing_login_credentials), content_type="application/json")
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response_data["message"], "username Cannot be empty")

    # def test_get_all_users_when_not_admin(self):
    #     jwt_token = json.loads(self.login_response.data)["token"]
    #     response = self.test_client.get('/api/v1/users', headers=dict(
    #         Authorization="Bearer " + jwt_token), content_type="application/json")
    #     self.assertEqual(response.status_code, 401)


    # def test_register_with_invalid_password(self):
    #     response = self.test_client.post(
    #         '/api/v1/auth/signup', data=json.dumps(self.user_invalid_password))
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response_data["message"],
    #                      "password must be longer than 8 characters")
    #     self.assertIs(type(response_data), dict)

    # def test_register_with_invalid_username(self):
    #     response = self.test_client.post(
    #         '/api/v1/auth/signup', data=json.dumps(self.user_invalid_username))
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response_data["message"],
    #                      "username must be longer than 5 characters")
    #     self.assertIs(type(response_data), dict)
