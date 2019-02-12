from flask import Blueprint
from flask import request, jsonify, make_response, Blueprint
from functools import wraps

from app.api.v2.models.meetup import Meetup, AuthenticationRequired
from app.api.v2.models.user import User
from app.api.v2.utils.meetup_validators import MeetupValidator

v2 = Blueprint('meetupv2', __name__, url_prefix='/api/v2/')

""" This route performs a get request to fetch all upcoming meetups """
@v2.route("/meetups/upcoming", methods=['GET'])
def get_all_meetups():
    meetups = Meetup().fetch_meetups('(authorId, topic, description, location)')
    meetups_list = []

    for meetup in meetups:
        meetups_list.append(meetup[0])

    return make_response(jsonify({
        "status": 200,
        "meetups": meetups_list
    }), 200)


""" This route posts a meetup """
@v2.route("/<int:adminId>/meetups", methods=['POST'])
@AuthenticationRequired
def post_a_meetup(adminId):
    data = request.get_json()

    if MeetupValidator().meetup_fields(data):
        return make_response(jsonify(MeetupValidator().meetup_fields(data)), 400)
    else:
        # Validate user
        validate_question = MeetupValidator(data)
        validation_methods = [
            validate_question.data_exists,
            # validate_question.valid_description,
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
            "topic": data['title'],
            "description": data['description'],
            "location": data['location'],
            "images": data['images'],
            "happeningOn": data['happeningOn'],
            "tags": data['tags'],
            "id": adminId
        }
        
        meetup_model = Meetup(meetup=meetup)
        meetup_model.save_meetup()

        User().make_admin(adminId)

        return make_response(jsonify({
            "status": 201,
            "message": "You have successfully posted a meetup",
            "data": [{
                "topic": data['title'],
                "location": data['location'],
                "images": data['images'],
                "happeningOn": data['happeningOn'],
                "tags": data['tags'],
            }],
        }), 201)

 
""" This route fetches a specific meetup """
@v2.route("/meetups/<int:meetupId>", methods=['GET'])
def get_meetup(meetupId):
    meetup = Meetup().fetch_specific_meetup('(authorId, topic, description, location)', f"id = {meetupId}")

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
@v2.route("<int:adminId>/meetups/<int:meetupId>", methods=['PUT'])
@AuthenticationRequired
def edit_meetup(adminId, meetupId):
    data = request.get_json()

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

        updates = {
            "topic": data['title'],
            "description": data['description'],
            "location": data['location'],
            "images": data['images'],
            "happeningOn": data['happeningOn'],
            "tags": data['tags']
        }
                
        try:
            userId = Meetup().fetch_specific_meetup('authorId', f"id = {meetupId}")[0]
            user = User().fetch_specific_user('id', f"id = {userId}")[0]

            if adminId == user:
                
                if isinstance(Meetup().update_meetup(meetupId, updates), dict):

                    return make_response(Meetup().update_meetup(meetupId, updates), 404)
                else:
                    return make_response(jsonify({
                        "status": 200,
                        "message": f"Meetup with id {meetupId} was updated"
                    }), 200)
            else:
                return make_response(jsonify({
                    "error": "Sorry! Only admins are authorized to access this resource.",
                    "status": 403
                }), 403)
        except:

            return make_response(Meetup().update_meetup(meetupId, updates), 404)


""" This route deletes a specific meetup """
@v2.route("admin/meetups/<int:meetupId>", methods=['DELETE'])
@AuthenticationRequired
def delete_meetup(meetupId):

    try:
        User().fetch_specific_user('isAdmin', "isAdmin = True")
        remove_meetup = Meetup().delete_meetup(meetupId)
        if isinstance(remove_meetup, dict):
            return make_response(jsonify(remove_meetup))
        else:
            return make_response(jsonify({
                "message": f"meetup with id '{meetupId}' deleted successfully"
            }))
    except:
        return make_response(jsonify({
            "error": "This resource is accessible by admins only",
            "status": 403
        }))


""" This route posts RSVPS on meetups """
@v2.route("/<int:userId>/meetups/<int:meetupId>/rsvp", methods=['POST'])
@AuthenticationRequired
def post_RSVP(meetupId, userId):
    data = {}

    try:
        meetup_id = Meetup().fetch_specific_meetup('id', f"id = {meetupId}")[0]
        meetup = Meetup().fetch_specific_meetup('topic', f"id = {meetupId}")[0]
        user_id = User().fetch_specific_user('id', f"id = {userId}")[0]

        try:
            data = request.get_json()
            data['status']
        except:
            return make_response(jsonify({
                "error": 'You missed the status key, value pair',
                "status": 400
            }), 400)

        rsvp = dict(
            userId=user_id,
            meetupId=meetup_id,
            status=data['status']
        )

        responses = {
            "yes": f"You have successfully RSVP'd on meetup '{meetup.upper()}'",
            "no": f"You have confirmed you're not attending meetup '{meetup.upper()}'",
            "maybe": f"You have confirmed you might attend '{meetup.upper()}' meetup"
        }

        def confirm(res):
            str(res).lower()
            if res == 'yes' or res == 'no' or res == 'maybe':
                return responses[res]
            else:
                return False

        if not confirm(rsvp['status']):
            return make_response(jsonify({
                "error": "Invalid response! Respond with YES/NO/MAYBE",
                "status": 400
            }))
        else:
            rsvp_tuple = Meetup().fetch_rsvps('(userId, meetupId)', f'True = True')
            incoming_rsvp = [(f'({userId},{meetupId})',)]

            if incoming_rsvp[0] in rsvp_tuple:
                
                return make_response(jsonify({
                    "status": 400,
                    "error": "You've already RSVPd on this meetup!"
                }))
            else:
                Meetup().rsvp_meetup(rsvp)

                return jsonify({
                    "status": 200,
                    "message": confirm(rsvp['status']),
                    "data": rsvp
                }), 201
    except:
        return jsonify({
            "error": 'Meetup not found or does not exist',
            "status": 404
        }), 404
        