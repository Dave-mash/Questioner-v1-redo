"""
This module sets up tests for the user model 
"""

import unittest
from werkzeug.security import check_password_hash

from app.api.v1.models.user import User

class TestUser(unittest.TestCase):

    def setUp(self):

        self.user_item = {
            "id": 1,
            "first_name": "David",
            "last_name": "mash",
            "othername": "Dave",
            "email": "dave@demo.com",
            "phoneNumber": "0729710290",
            "username": "mwas",
            "password": "abc123@1A",
        }

        self.user = User(self.user_item)

    def test_save_user(self):
        self.user.save_user()
        self.assertEqual(self.user.fetch_users()[1]['email'], self.user_item['email'])
        self.assertTrue(check_password_hash(self.user.fetch_users()[1]['password'], self.user_item['password']))

    def test_fetch_users(self):
        self.assertTrue(self.user.fetch_users())

    def test_specific_user(self):

        self.assertEqual(self.user.fetch_specific_user(1)['email'], self.user_item['email'])
        self.assertTrue(check_password_hash(self.user.fetch_specific_user(1)['password'], self.user_item['password']))

    def test_existing_user(self):
        user_item = { **self.user_item }
        user = User(user_item)
        user.save_user()
        self.assertEqual(user.save_user(), {
                            "error": "This email is already taken!",
                            "status": 409
                        })
        user_item['email'] = "josh@demo.com"
        user = User(user_item)
        user.save_user()
        self.assertEqual(user.save_user(), {
                            "error": "This username is already taken!",
                            "status": 409
                        })

    def test_log_in_user(self):

        # non-existing user
        user = {
            "email": "pete@demo.com",
            "password": "bca123@1A"
        }

        self.assertEqual(self.user.log_in_user(user), False)

        # existing user
        user2 = {
            "email": self.user_item['email'],
            "password": self.user_item['password']
        }
        self.assertTrue(self.user.log_in_user(user2))

    def test_edit_user(self):
        updates = {"first_name": "Travis"}

        self.user.save_user()
        self.user.edit_user(1, updates)
        user = self.user.fetch_specific_user(1)
        self.assertEqual(user['first_name'], 'Travis')

    def test_delete_user(self):

        self.user.save_user()
        self.user.delete_user(1)

        user = self.user.fetch_specific_user(1)
        self.assertFalse(user)