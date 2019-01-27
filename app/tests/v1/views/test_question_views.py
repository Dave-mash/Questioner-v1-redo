"""
This module sets up tests for the question views 
"""

import unittest
import datetime
import json

from app import create_app

class TestQuestion(unittest.TestCase):

    db = []

    def setUp(self):
        """ Initializes app"""

        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.question = {
            "title": "Python",
            "body": "What are Python Data structures?",
            "id": 0,
            "createdOn": "10/10/2019",
            "meetupId": 0,
            "votes": 0
        }
        self.meetup = {
            "id": 0,
            "createdOn": "05/10/2019",
            "topic": "a meetup",
            "description": "this is a meetup",
            "location": "Nairobi",
            "happeningOn": "12-12-2019",
            "tags": "['Django', 'Flask']"
        }

    def post_req(self, path='api/v1/0/questions', data={}):
        """ This function utilizes the test client to send POST requests """
        data = data if data else self.question
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

    def test_meetup_questions(self):
        """ Test that user can fetch all a meetup's questions """

        payload = self.post_req()
        self.assertEqual(payload.json['error'], "Meetup not found or does not exist")
        self.assertEqual(payload.status_code, 404)

        # meetup_res = self.post_req(path='api/v1/meetups', data=self.meetup)
        # self.assertEqual(meetup_res.json['status'], 201)