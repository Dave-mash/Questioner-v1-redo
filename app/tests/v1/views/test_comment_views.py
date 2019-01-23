import unittest
import datetime
import json

from app import create_app

class TestMeetup(unittest.TestCase):

    comments = []
    questions = [{
            "title": "Python",
            "body": "What are Python Data structures?",
            "id": 0,
            "createdOn": "10/10/2019",
            "meetupId": 1,
            "votes": -3
        },
        {
            "title": "Django",
            "body": "What is Django?",
            "id": 1,
            "createdOn": "15/10/2019",
            "meetupId": 2,
            "votes": 2
        }]

    def setUp(self):
        """ Initializes app"""

        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.comment = {
            "id": 1,
            "question": 0,
            "createdOn": "12/12/2019",
            "title": "Python",
            "body": "What are Python data structures?",
            "comment": "This is Python!"
        }
        self.meetup = {
            "id": 2,
            "createdOn": "05/10/2019",
            "topic": "a meetup",
            "description": "this is a meetup",
            "location": "Nairobi",
            "happeningOn": "12-12-2019",
            "tags": "['Django', 'Flask']"
        }

    def post_req(self, path='api/v1/0/comments', data={}):
        """ This function utilizes the test client to send POST requests """
        data = data if data else self.comment
        data['id'] = len(self.comments)
        self.comments.append(data)
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

    def test_post_a_comment(self):
        """ Test that a user can post a comment to a question """

        que = [que for que in self.questions if que['id'] == 0]

        # test non-existing question
        payload = self.post_req()
        self.assertEqual(payload.json['error'], "Question not found or does not exist")

        # test existing question
        # self.post_req(path="api/v1/meetups", data=self.meetup)
        self.post_req(path="api/v1/0/questions", data=self.questions[0])
        payload = self.post_req()
        # self.assertEqual(payload.json['error'], "No meetup found")