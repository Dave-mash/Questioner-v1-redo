from flask import Blueprint
from flask import request, jsonify, make_response, Blueprint

from app.api.v1.models.meetup import Meetup

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
def post_a_meetup():
    data = request.get_json()

    meetup = {
        "topic": data['topic'],
        "description": data['description'],
        "location": data['location'],
        "images": ["img1", "img2"],
        "happeningOn": data['happeningOn'],
        "tags": data['tags'],
    }
    
    meetup_model = Meetup(meetup)

    meetup_model.save_meetup()
    
    return make_response(jsonify({
        "status": 201,
        "message": "You have successfully posted a meetup",
        "data": [{
            "topic": data['topic'],
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


""" This route deletes a specific meetup """
@v1.route("admin/meetups/<int:meetupId>", methods=['DELETE'])
def delete_meetup(meetupId):

    get_meetup = Meetup().fetch_specific_meetup(meetupId)

    if get_meetup:
        Meetup().delete_meetup(meetupId)
        return jsonify({
            "status": 200,
            "message": "{} was deleted".format(get_meetup['topic'].upper())
        }), 200
    else:
        return make_response(jsonify({
            "error": 'Meetup not found!',
            "status": 404
        }), 404)

""" This route posts RSVPS on meetups """
@v1.route("/meetups/<int:meetupId>/rsvp", methods=['POST'])
def post_RSVP(meetupId):
    data = request.get_json()
    meetups = Meetup().fetch_meetups()
    meetup = [meetup for meetup in meetups if meetup['id'] == meetupId]

    if meetup:
        
        topic = meetup[0]['topic'].upper()
        rsvp = {
            "meetup": meetupId,
            "topic": topic,
            "status": data['status']
        }

        def confirm():
            if rsvp['status'] == "yes":
                return "You have successfully RSVP'd on {} meetup".format(topic)
            elif rsvp['status'] == "no":
                return "You have confirmed you're not attending the {} meetup".format(topic)
            elif rsvp['status'] == "maybe":
                return "You have confirmed you might attend the {} meetup".format(topic)

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
