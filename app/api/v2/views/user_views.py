"""
This module defines all the user endpoints
"""
import json
from flask import request, jsonify, make_response, Blueprint

from app.api.v2.models.user import User
from app.api.v2.utils.user_validators import UserValidator

v2 = Blueprint('userv2', __name__, url_prefix='/api/v2/')


""" This route fetches all users """
@v2.route("/users", methods=['GET'])
def get():
    users = User().fetch_all_users()
    users_list = []

    for user in users:
        users_list.append(user[0])

    return make_response(jsonify({
        "status": 200,
        "users": users_list
    }), 200)

""" This route allows unregistered users to sign up """
@v2.route("/auth/signup", methods=['POST'])
def registration():
    data = request.get_json()

    if UserValidator().signup_fields(data):
        return make_response(jsonify(UserValidator().signup_fields(data)), 400)
    else:
        # Validate user
        validate_user = UserValidator(data)
        validation_methods = [
            validate_user.valid_email,
            validate_user.valid_name,
            validate_user.valid_phoneNumber,
            validate_user.validate_password,
            validate_user.matching_password
        ]

        for error in validation_methods:
            if error():
                return make_response(jsonify({
                    "error": error()
                }), 422)
                
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
        if reg_user.save_user():
            return make_response(jsonify(reg_user.save_user()), 409)
        else:
            id = reg_user.fetch_user_id(user_data['username'])
            auth_token = reg_user.encode_auth_token(id[0])
            return make_response(jsonify({
                "status": 201,
                "message": "{} registered successfully".format(data['email']),
                "username": data['username'],
                "auth_token": auth_token.decode('utf-8')
            }), 201)        
            
""" This route allows registered users to log in """
@v2.route("/auth/login", methods=['POST'])
def login():
    data = request.get_json()
    missing_fields = UserValidator().login_fields(data)

    if missing_fields:
        return make_response(jsonify(missing_fields), 400)

    validate_user = UserValidator(data)

    if validate_user.valid_email():
        return make_response(jsonify({
            "error": validate_user.valid_email()
        }), 422)

    credentials = {
        "email": data['email'],
        "password": data['password']
    }

    # if auth:
    log_user = User().log_in_user(credentials)

    if isinstance(log_user, int):
        auth_token = User().encode_auth_token(log_user)
        return make_response(jsonify({
            "status": 201,
            "auth_token": auth_token.decode('utf-8'),
            "message": "{} has been successfully logged in".format(data['email'])
        }), 201)
    else:
        return make_response(log_user)


""" This route allows a user to delete their account """
@v2.route("/profile/<int:userId>", methods=['DELETE'])
def del_account(userId):

    remove_user = User().delete_user(userId)
    if isinstance(remove_user, dict):
        return make_response(jsonify(remove_user))
    else:
        return make_response(jsonify({
            "message": f"user with id '{userId}' deleted successfully"
        }))

""" This route allows a user to update their account """
@v2.route("/profile/<int:userId>", methods=['PUT'])
def update_account(userId):
    data = request.get_json()

    if UserValidator().signup_fields(data):
        return make_response(jsonify(UserValidator().signup_fields(data)), 400)
    else:
        # Validate user
        validate_user = UserValidator(data)
        validation_methods = [
            validate_user.valid_email,
            validate_user.valid_name,
            validate_user.valid_phoneNumber,
            validate_user.validate_password,
            validate_user.matching_password
        ]

        for error in validation_methods:
            if error():
                return make_response(jsonify({
                    "error": error()
                }), 422)
                
    user_data = {
        "first_name": data['first_name'],
        "last_name": data['last_name'],
        "othername": data['othername'],
        "email": data['email'],
        "phoneNumber": data['phoneNumber'],
        "username": data['username'],
        "password": data['password']
    }    

    update_user = User().update_user(userId, user_data)
    if isinstance(update_user, dict):
        return make_response(jsonify(update_user))
    else:
        return make_response(jsonify({
            "message": f"user {user_data['email']} updated successfully"
        }))