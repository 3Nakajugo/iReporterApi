import unittest
import json
from project.views import app


class TestApi(unittest.TestCase):

    def setUp(self):
        self.test_client = app.test_client()

    def test_index(self):
        response = self.test_client.get('/welcome')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'],"Welcome to iReporter")
