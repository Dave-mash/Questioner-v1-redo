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

class BaseModel:
    """ This class defines all the methods reusable in all the models """

    def __init__(self, table_name='', database=os.getenv('FLASK_DATABASE_URI')):

        self.table_name = table_name
        self.database = InitializeDb(database)


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


    def grab_all_items(self, cols, condition):
        """ This method fetches all items """

        return self.database.fetch_all(
            "SELECT {} FROM {} WHERE {};".format(cols, self.table_name, condition)
        )


    def grab_items_by_name(self, column, condition):
        """ This method fetches an item by name """
        
        return self.database.fetch_one(
            "SELECT {} FROM {} WHERE {}".format(column, self.table_name, condition)
        )


    def grab_items(self, columns, name, condition):
        """ This method fetches items """

        return self.database.fetch_all(
            "SELECT {} FROM {} WHERE {}".format(columns, name, condition)
        )


    def add_item(self, keys, values):
        """ This method adds an item """

        return self.database.execute(
            "INSERT INTO {} ({}) VALUES {};".format(self.table_name, keys, values)
        )


    def add_item_two(self, name, keys, values):
        """ This method adds an item """

        return self.database.execute(
            "INSERT INTO {} ({}) VALUES {};".format(name, keys, values)
        )


    def delete_item(self, condition):
        """ This method defines the delete item query """
        
        return self.database.update(
            "DELETE FROM {} WHERE {}".format(self.table_name, condition)
        )

       
    def update_item(self, updates, condition):
        """ This method defines the update item query """

        return self.database.update(
            "UPDATE {} SET {} WHERE {}".format(self.table_name, updates, condition)
        )


class AuthenticationRequired:
    """ This decorator class validates the token """

    def __init__(self, f):
        self.f = f
        update_wrapper(self, f)

    def __call__(self, *args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or len(auth_header) < 8 or " " not in auth_header:
            return jsonify({ "error": "Please log in first!" }), 403

        auth_token = auth_header.split(" ")[1]

        if isinstance(BaseModel().decode_auth_token(auth_token), str):
            return jsonify({ "error": BaseModel().decode_auth_token(auth_token) })
        
        return self.f(*args, **kwargs)
