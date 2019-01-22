import unittest
import datetime
import json

from app import create_app

class TestMeetup(unittest.TestCase):

    db = []

    def setUp(self):
        """ Initializes app"""

        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.meetup = {
            "happeningOn" : "12-12-2018",
            "location" : "Nairobi",
            "tags": ["Machine learning", "Neural networks"],
            "images": ["img1", "img2"],
            "topic": "Python data structures",
            "description": "Deep dive into python",
        }

    def post_req(self, path='api/v1/meetups', data={}):
        """ This function utilizes the test client to send POST requests """
        data = data if data else self.meetup
        data['id'] = len(self.db)
        self.db.append(data)
        res = self.client.post(
            path,
            data=json.dumps(data),
            content_type='application/json'
        )
        return res

    def get_req(self, path):
        """ This function utilizes the test client to send GET requests """
        
        res = self.client.get(path)
        return res 

    def test_create_meetup_with_valid_data(self):
        """ Test that a user can create a meetup """
    
        payload = self.post_req(data=self.meetup)
        self.assertEqual(payload.status_code, 201)
        self.assertEqual(payload.json['message'], "You have successfully posted a meetup")
