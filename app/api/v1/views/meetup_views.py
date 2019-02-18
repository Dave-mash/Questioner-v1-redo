from flask import Blueprint
from flask import request, jsonify, make_response, Blueprint
from functools import wraps

from app.api.v1.models.meetup import Meetup
from app.api.v1.models.user import User
from app.api.v1.utils.meetup_validators import MeetupValidator
from app.api.v1.models.base_model import AuthenticationRequired

v1 = Blueprint('meetupv1', __name__, url_prefix='/api/v1/')

""" This route performs a get request to fetch all upcoming meetups """
@v1.route("/meetups/upcoming", methods=['GET'])
def get_all_meetups():
    meetups = Meetup().fetch_meetups()

    return make_response(jsonify({
        "status": 200,
        "meetups": meetups
    }), 200)

""" This route posts a meetup """
@v1.route("/meetups", methods=['POST'])
@AuthenticationRequired
def post_a_meetup():
    data = request.get_json()
    auth_header = request.headers
    print(auth_header)

    if MeetupValidator().meetup_fields(data):
        return make_response(jsonify(MeetupValidator().meetup_fields(data)), 400)
    else:
        # Validate user
        validate_question = MeetupValidator(data)
        validation_methods = [
            validate_question.valid_date,
            validate_question.data_exists,
            validate_question.valid_description,
            validate_question.valid_location,
            validate_question.valid_tags,
            validate_question.valid_title
        ]

        for error in validation_methods:
            if error():
                return make_response(jsonify({
                    "error": error(),
                    "status": 422
                }), 422)
         
    meetup = {
        "title": data['title'],
        "description": data['description'],
        "location": data['location'],
        "images": data['images'],
        "happeningOn": data['happeningOn'],
        "tags": data['tags'],
    }
    
    meetup_model = Meetup(meetup)

    meetup_model.save_meetup()
    
    return make_response(jsonify({
        "status": 201,
        "message": "You have successfully posted a meetup",
        "data": [{
            "title": data['title'],
            "location": data['location'],
            "images": ["img1", "img2"],
            "happeningOn": data['happeningOn'],
            "tags": data['tags'],
        }],
    }), 201)


""" This route fetches a specific meetup """
@v1.route("/meetups/<int:meetupId>", methods=['GET'])
def get_meetup(meetupId):
    meetup = Meetup().fetch_specific_meetup(meetupId)

    if meetup:
        return jsonify({
            "status": 200,
            "data": meetup
        }), 200
    else:
        return jsonify({
            "status": 404,
            "error": "No meetup found!"
        }), 404


""" This route edits a meetup """
@v1.route("meetups/<int:meetupId>", methods=['PATCH'])
@AuthenticationRequired
def edit_meetup(meetupId):
    data = request.get_json()

    meetup = Meetup().fetch_specific_meetup(meetupId)

    if meetup:

        updates = {
            "title": data['title'],
            "description": data['description'],
            "location": data['location'],
            "images": ["img1", "img2"],
            "happeningOn": data['happeningOn'],
            "tags": data['tags']
        }

        Meetup().edit_meetup(meetupId, updates)
        return jsonify({
            "status": 200,
            "message": "{} was updated".format(meetup['title'].upper())
        }), 200
    else:
        return make_response(jsonify({
            "error": 'meetup not found!',
            "status": 404
        }), 404)


""" This route deletes a specific meetup """
@v1.route("admin/meetups/<int:meetupId>", methods=['DELETE'])
@AuthenticationRequired
def delete_meetup(meetupId):

    get_meetup = Meetup().fetch_specific_meetup(meetupId)

    if get_meetup:
        Meetup().delete_meetup(meetupId)
        return jsonify({
            "status": 200,
            "message": "{} was deleted".format(get_meetup['title'].upper())
        }), 200
    else:
        return make_response(jsonify({
            "error": 'Meetup not found!',
            "status": 404
        }), 404)

""" This route posts RSVPS on meetups """
@v1.route("/meetups/<int:meetupId>/rsvp", methods=['POST'])
@AuthenticationRequired
def post_RSVP(meetupId):
    data = request.get_json()
    meetups = Meetup().fetch_meetups()
    meetup = [meetup for meetup in meetups if meetup['id'] == meetupId]

    if meetup:
        
        title = meetup[0]['title'].upper()
        rsvp = {
            "meetup": meetupId,
            "title": title,
            "status": data['status']
        }

        def confirm():
            if rsvp['status'] == "yes":
                return "You have successfully RSVP'd on {} meetup".format(title)
            elif rsvp['status'] == "no":
                return "You have confirmed you're not attending the {} meetup".format(title)
            elif rsvp['status'] == "maybe":
                return "You have confirmed you might attend the {} meetup".format(title)

        return jsonify({
            "status": 200,
            "message": confirm(),
            "data": rsvp
        }), 201
    else:
        return jsonify({
            "error": 'Meetup not found or doesn\'nt exist',
            "status": 404
        }), 404
