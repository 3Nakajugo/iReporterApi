import unittest
import json
from project.views import app
from project.models import Incident, incidents


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

    def test_index(self):
        """
        test for creating redflag
        """
        response = self.test_client.get('/api/v1/welcome')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], "Welcome to iReporter")

    def test_create_incident(self):
        response = self.test_client.post(
            '/api/v1/incidents', data=json.dumps(self.incident))
        response_data = json.loads(response.data)
        self.assertEqual(response_data["data"], [
            {
                "message": "incident redflag has been created"
            }
        ])
        self.assertEqual(response.status_code, 201)

    def test_get_all_redflags(self):
        response = self.test_client.post(
            '/api/v1/incidents', data=json.dumps(self.incident))
        response = self.test_client.get('/api/v1/incidents')
        self.assertEqual(response.status_code, 200)

    def test_get_all_when_list_is_empty(self):
        response = self.test_client.get('/api/v1/incidents')
        responce_data = json.loads(response.data)
        print(responce_data)
        self.assertEqual(response.status_code, 200)

    def test_get_single_redflag_that_doesnot_exist(self):
        response = self.test_client.get('/api/v1/incidents/908')
        self.assertEqual(response.status_code, 404)

    def test_get_single_redflag_that_exist(self):
        response = self.test_client.post(
            '/api/v1/incidents', data=json.dumps(self.incident))

        response = self.test_client.get('/api/v1/incidents/2')
        request_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(request_data, dict)

    def test_delete_redflag(self):
        response = self.test_client.post(
            '/api/v1/incidents', data=json.dumps(self.incident))
        response = self.test_client.delete('/api/v1/incidents/1')
        request_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request_data["status"], 200)
        self.assertEqual(request_data["data"], [
            {
                "id": 1,
                "message": "red-flag record has been deleted"
            }
        ])
        self.assertTrue(request_data, dict)

    def test_delete_redflag_that_doesnot_exist(self):
        response = self.test_client.post(
            '/api/v1/incidents', data=json.dumps(self.incident))
        response = self.test_client.delete('/api/v1/incidents/5')
        request_data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(request_data["status"], 404)
        self.assertEqual(request_data["message"],
                         "no incident with such an id")

    # def test_edit_location_of_redlag_that_doesnot_exist(self):
    #     response = self.test_client.post(
    #         '/api/v1/incidents', data=json.dumps(self.incident))
    #     self.edit_location = {"location": "ntinda"}
    #     response = self.test_client.patch('/api/v1/incidents/6/location', data=json.dumps(self.edit_location))
    #     self.assertEqual(response.status_code,404)
