"""
This module sets up the question model and all it's functionality
"""

import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from app.api.v1.models.base_model import BaseModel

class User(BaseModel):
    
    base_model = BaseModel('user_db')

    def __init__(self, user={}):

        if user:
            self.id = len(self.fetch_users())
            self.createdOn = str(datetime.today())
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
        users = self.fetch_users()
        user_item = {
            "id": self.id,
            "dateRegistered": self.createdOn,
            "first_name": self.Fname,
            "last_name": self.Lname,
            "othername": self.othername,
            "email": self.email,
            "phoneNumber": self.phoneNumber,
            "username": self.username,
            "password": self.password,
            "isAdmin": self.isAdmin,
            "rsvps": self.rsvps
        }

        try:
            for user in users:
                email = user['email'] == self.email
                username = user['username'] == self.username
                if email:    
                    return {
                        "error": "This email is already taken!",
                        "status": 409
                    }
                elif username:
                    return {
                        "error": "This username is already taken!",
                        "status": 409
                    }
            self.base_model.add_item(user_item)
        except:
            self.base_model.add_item(user_item)

    def fetch_users(self):

        return self.base_model.users_list

    # Log in user
    def log_in_user(self, details):

        try:
            # Check if user details exists
            users = self.fetch_users()
            
            email = [email for email in users if email['email'] == details['email']]
            password = [p_word for p_word in users if check_password_hash(p_word['password'], details['password'])]

            if email and password:
                return str(uuid.uuid1())
            else:
                return False
        except:
            return None

    def fetch_specific_user(self, id):

        db = self.base_model.users_list
        user = [user for user in db if user['id'] == id]

        if user:
            return user[0]
        else:
            return False

    def edit_user(self, id, udpates):

        self.base_model.edit_item(id, udpates)

    def delete_user(self, id):

        self.base_model.delete_item(id)