"""
This module defines all the user endpoints
"""
import json
from flask import request, jsonify, make_response, Blueprint

from app.api.v2.models.user import User
from app.api.v2.utils.user_validators import UserValidator

v2 = Blueprint('userv2', __name__, url_prefix='/api/v2/')


# """ This route fetches all users """
# @v2.route("/users", methods=['GET'])
# def get():
#     users = User().fetch_users()

#     return make_response(jsonify({
#         "status": 200,
#         "users": users
#     }), 200)

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

    if log_user:
        auth_token = User().encode_auth_token(log_user)
        return make_response(jsonify({
            "status": 201,
            "auth_token": auth_token.decode('utf-8'),
            "message": "{} has been successfully logged in".format(data['email'])
        }), 201)
    else:
        return make_response(jsonify({
            "status": 401,
            "error": "You entered wrong information. Please check your credentials or try creating an account first!"
        }), 401) # unauthorised

""" This route allows a users to delete their account """
@v2.route("/profile/<int:userId>", methods=['DELETE'])
def del_account(userId):

    remove_user = User().delete_user(userId)
    if isinstance(remove_user, dict):
        return make_response(jsonify({
            "error": remove_user
        }))
    else:
        return make_response(jsonify({
            "message": f"user {userId} deleted successfully"
        }))

