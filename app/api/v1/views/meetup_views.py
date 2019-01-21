from flask import Blueprint
from flask import request, jsonify, make_response, Blueprint

from app.api.v1.models.meetup import Meetup

v1 = Blueprint('meetupv1', __name__, url_prefix='/api/v1/')

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