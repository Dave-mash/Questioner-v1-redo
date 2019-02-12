import unittest
import datetime
import json

from app import create_app

class TestUser(unittest.TestCase):

    def setUp(self):
        """ Initializes app"""

        self.app = create_app('testing')[0]
        self.client = self.app.test_client()
        self.user_item = {
            "first_name" : "David",
            "last_name" : "Mwangi",
            "othername" : "Dave",
            "email" : "jjj@demo.com",
            "phoneNumber" : "+254729710290",
            "username" : "jjj",
            "password": "abc123@1A",
            "confirm_password": "abc123@1A"
        }

    def post_req(self, path='api/v1/auth/signup', data={}):
        """ This function utilizes the test client to send POST requests """
        data = data if data else self.user_item
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

    def test_fetch_all_user(self):
        """ This method tests that fetch all users works correctly """

        payload = self.get_req('api/v1/users')
        self.assertEqual(payload.status_code, 200)

    def test_sign_up_user(self):
        """ This method tests that sign up users route works correctly """

        # test successful registration
        user = {
            "first_name" : "Josh",
            "last_name" : "Anderson",
            "othername" : "Miguel",
            "email" : "josh@email.com",
            "phoneNumber" : "+254754734345",
            "username" : "josh",
            "password": "abc123@1A",
            "confirm_password": "abc123@1A"
        }
        payload = self.post_req(data=user)
        # self.assertEqual(payload.json['status'], 201)
        # self.assertTrue(payload.json['auth_token'])
        # self.assertEqual(payload.json['message'], "josh@email.com registered successfully")

        # test missing fields
        user = {
            "last_name" : "Mwangi",
            "othername" : "Dave",
            "email" : "jjj@demo.com",
            "phoneNumber" : "+254729710290",
            "username" : "jjj",
            "password": "abc123@1A",
            "confirm_password": "abc123@1A"
        }
        payload2 = self.post_req(data=user)
        self.assertEqual(payload2.status_code, 400)
        self.assertEqual(payload2.json['error'], 'You missed the first_name key, value pair')

        # test invalid data
        user2 = { **self.user_item }
        user2['phoneNumber'] = "0729abc"
        payload3 = self.post_req(data=user2)
        self.assertEqual(payload3.status_code, 422)
        self.assertEqual(payload3.json['error'], 'Use valid numbers for phone number')


    def test_log_in_user(self):
        """ This method tests that the log in user route works correctly """

        # test successful log in
        user = {
            "email": self.user_item['email'],
            "password": self.user_item['password']
        }

        payload4 = self.post_req(path='api/v1/auth/login', data=user)

        self.assertEqual(payload4.status_code, 201)
        self.assertTrue(payload4.json['auth_token'])
        self.assertEqual(payload4.json['message'], "jjj@demo.com has been successfully logged in")

        user4 = {
            "email": "abc@demo.com",
            "password": "abc4A#@"
        }
        payload2 = self.post_req(path='api/v1/auth/login', data=user4)
        self.assertEqual(payload2.status_code, 401)
        self.assertEqual(payload2.json['error'], "You entered wrong information. Please check your credentials or try creating an account first!")

        # test missing field
        user1 = {
            "password": self.user_item['password']
        }
        payload = self.post_req(path='api/v1/auth/login', data=user1)
        self.assertEqual(payload.status_code, 400)

        # test invalid email
        user2 = { **user }
        user2['email'] = "jjjdemo.com"
        payload3 = self.post_req(path='api/v1/auth/login', data=user2)
        self.assertEqual(payload3.status_code, 422)
        self.assertEqual(payload3.json['error'], "Invalid email address!")

        