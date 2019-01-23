"""
This module takes care of validating input from the endpoints
"""

from datetime import datetime
import re
import string

from app.api.v1.models.base_model import BaseModel

base_model = BaseModel()

class UserValidator:
    
    def __init__(
        self,
        Fname="",
        Lname="",
        username="",
        email="",
        password="",
        confirm_password=""
    ):
        self.Fname = Fname
        self.Lname = Lname
        self.username = username
        self.email = email
        self.password = password
        self.confirm_password = confirm_password

    def errorHandler(self, error):
        return error

    def data_exists(self):

        data = {
            "Fname": self.Fname,
            "Lname": self.Lname,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "confirm_password": self.confirm_password
        }

        for key, value in data.items():
            if not value:
                return self.errorHandler('You missed a required field {}.'.format(key))

    def valid_name(self):
        if self.username:
            if len(self.username) < 3:
                return self.errorHandler('Your username is too short!')
            elif len(self.username) > 20:
                return self.errorHandler('Your username is too long!')

    def valid_email(self):
        reg_email = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")
        
        if not re.match(reg_email, self.email):
            return self.errorHandler('Invalid email address!')

    def validate_password(self):
        reg_password = re.compile(r'[a-zA-Z0-9@_+-.]{3,}$')

        if not re.match(reg_password, self.password):
            return self.errorHandler('Weak password!')

    def matching_password(self):
        if self.password != self.confirm_password:
            return self.errorHandler('Your passwords don\'t match')

    def valid_phoneNumber(self, number):
        if not int(number):
            return 'Use numbers only'
        