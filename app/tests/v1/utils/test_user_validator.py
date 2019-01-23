"""
This module tests the user_validator endpoint
"""

import unittest
from app.api.v1.utils.user_validators import UserValidator

class TestQuestionsValidator(unittest.TestCase):

    def setUp(self):
        """ Initializes app """
        self.user = {
            "Fname": "Dave",
            "Lname": "Mwangi",
            "username": "Mash",
            "email": "demo@email.com",
            "password": "password",
            "confirm_password": "password"
        }

    def test_user_data_exists(self):
        user = UserValidator('', '')
        self.assertEqual(user.data_exists(), 'You missed a required field Fname.')  

    def test_invalid_data(self):

        user = UserValidator('Dave', 'Mash', 'j')
        self.assertEqual(user.valid_name(), 'Your username is too short!')

        user = UserValidator('Dave', 'Mash', 'This is a very long name for this field')
        self.assertEqual(user.valid_name(), 'Your username is too long!')

        user = UserValidator('Dave', 'Mash', 'username', 'email.com')
        self.assertEqual(user.valid_email(), 'Invalid email address!')

        user = UserValidator('Dave', 'Mash', 'username', 'email@demo.com', 'q')
        self.assertEqual(user.validate_password(), 'Weak password!')

        user = UserValidator('Dave', 'Mash', 'username', 'email@demo.com', 'abc123', 'abc')
        self.assertEqual(user.matching_password(), 'Your passwords don\'t match')
