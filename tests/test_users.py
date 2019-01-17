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
            "user_name": "edljlkjkljk",
            "password": "edna123"
        }
        
    def test_get_all_users_when_list_empty(self):
        response = self.test_client.get(
            '/api/v1/users')
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        response = self.test_client.post(
            '/api/v1/users/signup', data=json.dumps(self.user))
        request_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(request_data["message"], "User has been created")
        self.assertIs(type(request_data), dict)

    def test_get_all_users(self):
        response = self.test_client.post(
            '/api/v1/users/signup', data=json.dumps(self.user))
        response = self.test_client.get(
            '/api/v1/users')
        request_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIs(type(request_data), dict)
