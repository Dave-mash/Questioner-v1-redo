"""
This module sets up the question model and all it's functionality
"""

import os
import uuid
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from app.api.v2.models.base_model import BaseModel, AuthenticationRequired

class User(BaseModel):
    
    def __init__(self, user={}, database=os.getenv('FLASK_DATABASE_URI')):

        self.base_model = BaseModel('users', database)

        if user:
            self.Fname = user['first_name']
            self.Lname = user['last_name']
            self.othername = user['othername']
            self.email = user['email']
            self.phoneNumber = user['phoneNumber']
            self.username = user['username']
            self.password = generate_password_hash(user['password'])
            self.isAdmin = False
      
      
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
            isAdmin=self.isAdmin
        )

        keys = ", ".join(user.keys())
        values = tuple(user.values())
        if self.fetch_specific_user('email', f"email = '{self.email}'"):
            return {
                "error": "This email already exists try logging in!",
                "status": 409
            }
        elif self.fetch_specific_user('username', f"username = '{self.username}'"):
            return {
                "error": "This username is already taken!",
                "status": 409
            }
        else:
            return self.base_model.add_item(keys, values)


    def fetch_user_id(self, username):
        """ This method fetches a user id """
    
        try:
            return self.fetch_specific_user('id', f"username = '{username}'")
        except:
            return False


    def fetch_all_users(self):
        """ This method fetches all users """

        return self.base_model.grab_all_items('(username, email)', f"isAdmin = False")


    def fetch_specific_user(self, cols, condition):
        """ This method fetches a single user """

        return self.base_model.grab_items_by_name(cols, condition)
        

    # Log in user
    def log_in_user(self, details):
        """ This method logs in a user """

        user = self.fetch_specific_user('email', f"email = '{details['email']}'")
        password = self.fetch_specific_user('password', f"email = '{details['email']}'")
        
        if not user:
            return jsonify({
                "error": "Details not found, please sign up!",
                "status": 401
            }), 401
        elif not check_password_hash(password[0], details['password']):
            return jsonify({
                "error": "Your email or password is incorrect!",
                "status": 403
            }), 403
        else:
            return self.fetch_specific_user('id', f"email = '{details['email']}'")[0]


    def make_admin(self, id):
        """ This method promotes a user to an admin """

        try:
            user_id = self.base_model.grab_items_by_name('id', f"id = {id}")[0]
            pair_dict = { "isAdmin": "isAdmin = True" }
            pair = ", ".join(pair_dict.values())
            return self.base_model.update_item(pair, f"id = {user_id}")
        except:
            return jsonify({ 'error': 'User Not found!', 'statu': 404 })


    def delete_user(self, id):
        """ This method defines the delete query """

        if self.fetch_specific_user('id', f"id = {id}"):
            return self.base_model.delete_item(f"id = {id}")
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

        if self.fetch_specific_user('id', f"id = {id}"):
            return self.base_model.update_item(pairs, f"id = {id}")
        else:
            return {
                "error": "User not found or does not exist!"
            }
