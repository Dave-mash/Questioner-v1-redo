import unittest
import datetime
from random import choice, randint
import json
import string

from app import create_app

class TestMeetup(unittest.TestCase):

    def create_user(self):
        """ simulate a fake user """
        username = "".join(choice(
                           string.ascii_letters) for x in range(randint(7, 10)))
        params = {
            "first_name": "Dave",
            "last_name": "mwas",
            "othername" : "mash",
            "email": "{}@gmail.com".format(username),
            "username": username,
            "phoneNumber" : "+254729710290",
            "password": "abc123@1A",
            "confirm_password": "abc123@1A"
        }
        
        res = self.client.post("/api/v1/auth/signup",
                                data=json.dumps(params),
                                content_type="application/json")

        user_id = res.json['user_id']
        auth_token = res.json['auth_token']
        return user_id, auth_token

    def setUp(self):
        """ Initializes app"""

        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.meetup = {
            "happeningOn" : "12-12-2018",
            "location" : "Nairobi",
            "tags": ["Machine learning", "Neural networks"],
            "images": ["img1", "img2"],
            "title": "Python data structures",
            "description": "Deep dive into python",
        }

    def post_req(self, path='api/v1/meetups', auth_token=1, data={}, headers=None):
        """ This function utilizes the test client to send POST requests """
        data = data if data else self.meetup
        if auth_token is 1:
            user = self.create_user()
            auth_token = user[1]
        if not headers:
            headers = {"Authorization": "Bearer {}".format(auth_token)}

        res = self.client.post(
            path,
            data=json.dumps(data),
            headers=headers,
            content_type='application/json'
        )
        return res

    def get_req(self, path):
        """ This function utilizes the test client to send GET requests """
        
        res = self.client.get(path)
        return res

    def test_create_meetup_with_valid_data(self):
        """ Test that a user can create a meetup """
    
        payload = self.post_req()
        self.assertEqual(payload.status_code, 201)
        self.assertEqual(payload.json['message'], "You have successfully posted a meetup")
        self.assertEqual(payload.json['status'], 201)

    def test_fetch_upcoming_meetups(self):
        """ Test that a user can fetch all upcoming meetups """

        payload = self.get_req('api/v1/meetups/upcoming')
        self.assertEqual(payload.status_code, 200)
        self.assertTrue(isinstance(payload.json['meetups'], list))
        self.assertEqual(payload.json['status'], 200)

    def test_get_specific_meetups(self):
        """ Test that a user can fetch a specific meetup """

        # test for non-existing meetup
        payload = self.get_req('api/v1/meetups/6')
        self.assertEqual(payload.status_code, 404)
        self.assertEqual(payload.json['error'], 'No meetup found!')

        # test existing meetup
        self.post_req(data=self.meetup)
        payload2 = self.get_req('api/v1/meetups/1')
        self.assertEqual(payload2.status_code, 200)
        self.assertEqual(payload2.json['status'], 200)

    def test_edit_meetup(self):
        """ Test that a user can edit a meetup """
        
        user = self.create_user()
        auth_token = user[1]
        headers = {"Authorization": "Bearer {}".format(auth_token)}

        payload = self.client.patch('api/v1/meetups/6', headers=headers)
        self.assertEqual(payload.status_code, 404)
        self.assertEqual(payload.json['error'], 'meetup not found!')

    def test_delete_meetup(self):
        """ Test that a user can delete a meetup """

        user = self.create_user()
        auth_token = user[1]
        headers = {"Authorization": "Bearer {}".format(auth_token)}

        # test for non-existing meetup
        payload = self.client.delete('api/v1/admin/meetups/6', headers=headers)
        self.assertEqual(payload.status_code, 404)
        self.assertEqual(payload.json['error'], 'Meetup not found!')

        # test existing meetup
        self.post_req(data=self.meetup)
        payload2 = self.client.delete('api/v1/admin/meetups/2', headers=headers)
        msg = "Python".upper()
        self.assertEqual(payload2.json['status'], 200)
        self.assertEqual(payload2.json['message'], "{} was deleted".format(msg))

    def test_RSVP_on_a_meetup(self):
        """ Test that a user can fetch a specific meetup """

        # test for non-existing meetup
        payload = self.post_req('api/v1/meetups/6/rsvp')
        self.assertEqual(payload.status_code, 404)
        self.assertEqual(payload.json['error'], 'Meetup not found or doesn\'nt exist')

        # test existing meetup
        msg = "Python".upper()

        data = { "status": "yes" }
        payload2 = self.post_req('api/v1/meetups/1/rsvp', data=data)
        self.assertEqual(payload2.status_code, 201)
        self.assertEqual(payload2.json['message'], "You have successfully RSVP'd on {} meetup".format(msg))
        
        data = { "status": "maybe" }
        payload2 = self.post_req('api/v1/meetups/1/rsvp', data=data)
        self.assertEqual(payload2.status_code, 201)
        self.assertEqual(payload2.json['message'], "You have confirmed you might attend the {} meetup".format(msg))

        data = { "status": "no" }
        payload2 = self.post_req('api/v1/meetups/1/rsvp', data=data)
        self.assertEqual(payload2.status_code, 201)
        self.assertEqual(payload2.json['message'], "You have confirmed you're not attending the {} meetup".format(msg))
