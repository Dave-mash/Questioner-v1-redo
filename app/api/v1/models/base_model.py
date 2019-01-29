"""
This module serves as a database mock-up for the project
"""

import os
import jwt
import datetime
from functools import wraps, update_wrapper
from flask import jsonify, request

meetups_list = []
questions_list = []
users_list = []
comments_list = []

class BaseModel:

    def __init__(self, db_name=''):
        self.db_name = db_name

        self.db = None
        self.meetups_list = meetups_list
        self.questions_list = questions_list
        self.users_list = users_list
        self.comments_list = comments_list

    @staticmethod
    def encode_auth_token(user_id):
        """ This method generates authentication token """
        from app import create_app

        app = create_app('development')

        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def blacklisted(self):
        pass

    @staticmethod
    def decode_auth_token(auth_token):
        """ This method takes in token and decodes it """
        from app import create_app
        app = create_app('development')

        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def check_db(self):
        if self.db_name == 'meetup_db':
            self.db = self.meetups_list
        elif self.db_name == 'question_db':
            self.db = self.questions_list
        elif self.db_name == 'user_db':
            self.db = self.users_list
        elif self.db_name == 'comment_db':
            self.db = self.comments_list
        else:
            self.db = None
            return'Invalid db_name'

    def add_item(self, item):
        self.check_db()
        self.db.append(item)

    def delete_item(self, item_id):
        self.check_db()
        del_item = [item for item in self.db if item['id'] == item_id]

        if del_item:
            self.db.remove(del_item[0])
        else:
            return "No item"

    def edit_item(self, item_id, updates):
        self.check_db()
        edit_item = [item for item in self.db if item['id'] == item_id]

        if edit_item:
            edit_item[0].update(updates)
        else: 
            return "No item"

class AuthenticationRequired:
    """ This decorator class defines the token authentication """

    def __init__(self, f):
        self.f = f
        update_wrapper(self, f)

    def __call__(self, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or len(auth_header) < 8 or " " not in auth_header:
            return jsonify({ "error": "Please log in first!" }), 403

        auth_token = auth_header.split(" ")[1]
        BaseModel().decode_auth_token(auth_token)

        return self.f(*args, **kwargs)
