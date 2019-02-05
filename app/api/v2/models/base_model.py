"""
This module serves as a database mock-up for the project
"""

import os
import jwt
import datetime
from functools import wraps, update_wrapper
from flask import jsonify, request

from app import create_app
from app.database import InitializeDb
database = InitializeDb(os.getenv('FLASK_DATABASE_URI'))

meetups_list = []
questions_list = []
users_list = []
comments_list = []

class BaseModel:
    """ This class defines all the methods reusable in all the models """

    def __init__(self, table_name=''):

        self.table_name = table_name
        self.db = None
        self.meetups_list = meetups_list
        self.questions_list = questions_list
        self.users_list = users_list
        self.comments_list = comments_list


    @staticmethod
    def encode_auth_token(user_id):
        """ This method generates authentication token """

        app, database = create_app()

        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
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

        app, database = create_app()

        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


    def grab_all_items(self, cols, condition, value):
        """ This method fetches all items """

        return database.fetch_all(
            "SELECT {} FROM {} WHERE {} = {};".format(self.table_name, cols, condition, value)
        )


    def grab_items_by_name(self, column, col_name, item_name):
        """ This method fetches an item by name """

        return database.fetch_one(
            "SELECT {} FROM {} WHERE {} = '{}'".format(column, self.table_name, col_name, item_name)
        )


    def add_item(self, keys, values):
        """ This method adds an item """

        return database.execute(
            "INSERT INTO {} ({}) VALUES {};".format(self.table_name, keys, values)
        )


    def delete_item(self, col, id):
        """ This method defines the delete item query """
        
        return database.update(
            "DELETE FROM {} WHERE {} = {}".format(self.table_name, col, id)
        )

       
    def update_item(self, col, id):
        """ This method defines the update item query """

        return database.update(
            "UPDATE {} SET {} WHERE id = {}".format(self.table_name, col, id)
        )


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
