"""
This module sets up the question model and all it's functionality
"""

import uuid
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from app.api.v2.models.base_model import BaseModel, AuthenticationRequired, database

class User(BaseModel):
    
    base_model = BaseModel('users')

    def __init__(self, user={}):
        if user:
            self.createdOn = datetime.timestamp(datetime.now())
            self.Fname = user['first_name']
            self.Lname = user['last_name']
            self.othername = user['othername']
            self.email = user['email']
            self.phoneNumber = user['phoneNumber']
            self.username = user['username']
            self.password = generate_password_hash(user['password'])
            self.isAdmin = False
            self.rsvps = []


    def save_user(self):
        """ This method saves a non-existing user """

        user = dict(
            first_name=self.Fname,
            last_name=self.Lname,
            other_name=self.othername,
            email=self.email,
            phone_number=self.phoneNumber,
            username=self.username,
            password=self.password,
            isAdmin=self.isAdmin,
            date_registered=self.createdOn
        )

        keys = ", ".join(user.keys())
        values = tuple(user.values())
        if self.fetch_specific_user('email', 'email', self.email):
            return {
                "error": "This email is already taken!",
                "status": 409
            }           
        elif self.fetch_specific_user('username', 'username', self.username):
            return {
                "error": "This username is already taken!",
                "status": 409
            }
        else:
            return self.base_model.add_item(keys, values)


    def fetch_user_id(self, username):
        """ This method fetches a user id """
    
        try:
            return self.fetch_specific_user('id', 'username', username)
        except:
            return False


    def fetch_specific_user(self, cols, condition, item):
        """ This method fetches a single user """

        return self.base_model.grab_items_by_name(cols, condition, item)
        

    # Log in user
    def log_in_user(self, details):

        try:
            # Check if user details exists
            users = []
            
            email = [email for email in users if email['email'] == details['email']]
            password = [p_word for p_word in users if check_password_hash(p_word['password'], details['password'])]

            if email and password:
                return str(uuid.uuid1())
            else:
                return False
        except:
            return None


    def delete_user(self, id):
        """ This method defines the delete query """

        if self.fetch_specific_user('id', 'id', id):
            return self.base_model.delete_item('id', id)
        else:
            return {
                "error": "User not found or does not exist!"
            }


    def update_user(self, id, updates):
        """ This method defines the update query """

        pairs_dict = {
            "first_name": f"first_name = '{updates['first_name']}'",
            "last_name": f"last_name = '{updates['last_name']}'",
            "other_name": f"other_name = '{updates['othername']}'",
            "email": f"email = '{updates['email']}'",
            "phoneNumber": f"phone_number = '{updates['phoneNumber']}'",
            "username": f"username = '{updates['username']}'",
            "password": f"password = '{generate_password_hash(updates['password'])}'"
        }
        
        pairs = ", ".join(pairs_dict.values())
        print(pairs)

        if self.fetch_specific_user('id', 'id', id):
            return self.base_model.update_item(pairs, id)
        else:
            return {
                "error": "User not found or does not exist!"
            }
