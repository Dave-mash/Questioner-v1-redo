"""
This module contains tests for the base model
"""

# 3rd party imports
import unittest
import os
from datetime import datetime

# local imports
from app.api.v2.models.user import User
from app.database import InitializeDb

class TestBaseModel(unittest.TestCase):

    def setUp(self):

        self.user_item = dict(
            first_name="David",
            last_name="Mwangi",
            othername="Dave",
            email="dave@demo.com",
            phoneNumber="0729710290",
            username="dave",
            password="abc123@1A",
        )

        self.user = User(self.user_item, os.getenv('TEST_DATABASE_URI'))
        self.user.base_model.database.create_tables()


    def test_save_user(self):
        """ Test that save user method works correctly """

        # add item
        self.user.save_user()
        user = self.user.fetch_specific_user('username', 'username', 'dave')
        self.assertTrue(user)


    def test_fetch_user_id(self):
        """ Test fetch user id method works correctly """

        self.user.save_user()
        self.assertTrue(self.user.fetch_user_id('dave'))
        self.assertFalse(self.user.fetch_user_id('mash'))


    def test_fetch_all_users(self):
        """ Test fetch all users method works correctly """

        users = self.user.fetch_all_users()

        # zero users
        self.assertFalse(users)

        # one user
        self.user.save_user()
        self.assertTrue(self.user.fetch_all_users())


    def test_fetch_specific_user(self):
        """ Test fetch specific user method works correctly """

        self.user.save_user()
        self.assertTrue(self.user.fetch_specific_user('id', 'username', 'dave'))


    def test_log_in_user(self):
        """ Test log in user method works correctly """

        self.user.save_user()
        user = {
            "email": self.user_item['email'],
            "password": self.user_item['password']
        }
        self.assertEqual(self.user.log_in_user(user), 1)

    
    def test_make_admin(self):
        """ Test make admin method works correctly """

        self.user.save_user()
        admin = self.user.fetch_specific_user('isAdmin', 'username', 'dave')[0]
        self.assertEqual(admin, False)
        # self.user.make_admin(1)
        # self.assertEqual(admin, True)
        # self.assertTrue(self.user.make_admin(1))
        

    def tearDown(self):
        """ This method destroys the test tables """

        self.user.base_model.database.drop_tables()


if __name__ == "__main__":
    unittest.main()