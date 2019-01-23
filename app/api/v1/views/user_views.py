"""
This module defines all the user endpoints
"""

from flask import request, jsonify, make_response, Blueprint
from app.api.v1.models.user import User
from app.api.v1.utils.user_validators import UserValidator
import uuid

v1 = Blueprint('userv1', __name__, url_prefix='/api/v1/')


def errorParser(duplicate, name):

    def error(error):
        return make_response(jsonify({
            "status": 409,
            "error": "This {} is already taken!".format(error)
        }), 409)

    if duplicate:
        return error(name)


def missing_fields(name):
    return jsonify({
        "error": "You missed the {} field".format(name)
    }, 400)

""" This route fetches all users """
@v1.route("/users", methods=['GET'])
def get():
    users = User().fetch_users()

    return make_response(jsonify({
        "status": 200,
        "users": users
    }), 200)

""" This route allows unregistered users to sign up """
@v1.route("/auth/signup", methods=['POST'])
def registration():
    data = request.get_json()

    fields = ['first_name', 'last_name', 'othername', 'email', 'phoneNumber', 'username', 'password', 'confirm_password']

    for key in fields:
        try:
            data[key]
        except:
            return jsonify({
                "error": 'You missed the {} key, value pair'.format(key)
            })

    users = User().fetch_users()
    dup_email = [user for user in users if user['email'] == data['email']]
    dup_username = [user for user in users if user['username'] == data['username']]

    if dup_username:
        return errorParser(dup_username[0]['username'], 'username')
    elif dup_email:
        return errorParser(dup_email[0]['email'], 'email')
    else:
        # Validate user
        validate_user = UserValidator(
            data['first_name'],
            data['last_name'],
            data['username'],
            data['email'],
            data['password'],
            data['confirm_password']
        )
        validate_user.data_exists()
        validate_user.valid_email()
        validate_user.valid_name()
        validate_user.valid_phoneNumber(data['phoneNumber'])
        validate_user.validate_password()
        validate_user.matching_password()

        # Register user
        user_data = {
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "othername": data['othername'],
            "email": data['email'],
            "phoneNumber": data['phoneNumber'],
            "username": data['username'],
            "password": data['password']
        }

        reg_user = User(user_data)
        reg_user.save_user()

        return make_response(jsonify({
            "status": "ok",
            "message": "{} registered successfully".format(data['email']),
            "username": data['username']
        }), 201)

""" This route allows registered users to log in """
@v1.route("/auth/login", methods=['POST'])
def login():
    data = request.get_json()

    credentials = {
        "email": data['email'],
        "password": data['password']
    }

    if User().log_in_user(credentials):
        return jsonify({
            "status": 201,
            "message": "{} has been successfully logged in".format(data['email'])
        }), 201
    else:
        return make_response(jsonify({
            "status": 401,
            "error": "You entered wrong information. Please check your credentials!"
        }), 401) # unauthorised
