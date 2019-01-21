import unittest
from app import create_app

class TestMeetup(unittest.TestCase):

    def setUp(self):
        """ Initializes app"""
        self.app = create_app('testing')
        self.client = self.app.test_client()

        self.user = {
            "first_name": "David",
            "last_name": "Mwangi",
            "username": "Dave",
            "email": "dave@gmail.com",
            "password": "abc123",
            "confirm_password": "abc123"
        }

    def test_create_meetup_with_valid_data(self):
        pass
