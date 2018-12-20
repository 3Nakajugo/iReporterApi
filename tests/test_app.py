import unittest
import json
from project.views import app
from project.models import Incident


class TestApi(unittest.TestCase):

    def setUp(self):
        self.test_client = app.test_client()

    def test_index(self):
        response = self.test_client.get('/api/v1/welcome')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], "Welcome to iReporter")

    # def test_create_incident(self):
    #     incident = Incident("edna", "redflag", "899 9i0",
    #                         "kdlk.jpg", "jncdsndfiowj")
    #     response = self.test_client.post('/api/v1/incidents', data=json.dumps(dict(created_by=incident.created_by,
    #                                                                               incident_type=incident.incident_type,
    #                                                                               location=incident.location,
    #                                                                               file=incident.file,
    #                                                                               comment=incident.comment)))
    #     self.assertEqual(response.status_code, 201)
