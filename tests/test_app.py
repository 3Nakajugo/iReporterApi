import unittest
import json
from project.views import app
from project.models import Incident


class TestApi(unittest.TestCase):

    def setUp(self):
        self.test_client = app.test_client()
        self.incident = {
            "created_by": "idlfowfk",
            "incident_type": "redflag",
            "location": "2123 13241",
            "file": "error.png",
            "comment": "jisckmsldkmspoll,ldjo"
        }

    def test_index(self):
        response = self.test_client.get('/api/v1/welcome')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], "Welcome to iReporter")

    # def test_create_incident(self):
    #     response = self.test_client.post(
    #         '/api/v1/incidents', data=json.dumps(self.incident))
    #     self.assertEqual(response.status_code, 201)
