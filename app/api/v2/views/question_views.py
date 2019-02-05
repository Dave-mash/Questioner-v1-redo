"""
This module sets up all the question endpoints
Author: Dave
"""

from flask import request, jsonify, make_response, Blueprint

from app.api.v2.models.question import Question, AuthenticationRequired
from app.api.v2.utils.question_validators import QuestionValidator
from app.api.v2.models.meetup import Meetup

v2 = Blueprint('questionv2', __name__, url_prefix='/api/v2/')


""" This route posts a question """
@v2.route("/<int:meetupId>/questions", methods=['POST'])
@AuthenticationRequired
def post_a_question(meetupId):
    data = request.get_json()
    
    if QuestionValidator().question_fields(data):
        return make_response(jsonify(QuestionValidator().question_fields(data)), 400)
    else:
        # Validate user
        validate_question = QuestionValidator(data)
        validation_methods = [
            validate_question.valid_que,
            validate_question.data_exists
        ]

        for error in validation_methods:
            if error():
                return make_response(jsonify({
                    "error": error()
                }), 422)
            
        meetups = Meetup().fetch_meetups()
        meetup = [meetup for meetup in meetups if meetup['id'] == meetupId]

        question = {
            "title": data['title'],
            "body": data['body'],
            "meetupId": meetupId
        }
        
        question_model = Question(question)

        question_model.save_question()
        
        if meetup:
            return make_response(jsonify({
                "status": 201,
                "message": "You have successfully posted a question",
                "data": [{
                    "title": data['title'],
                    "body": data['body'],
                    "meetup": meetupId
                }]
            }), 201)
        else:
            return make_response(jsonify({
                "error": "Meetup not found or does not exist",
                "status": 404
            }), 404)


""" This route displays a meetup's questions """
@v2.route("/<int:meetupId>/questions", methods=['GET'])
def meetup_questions(meetupId):

    questions = Question().fetch_questions()
    meetup_ques = [que for que in questions if que['meetupId'] == meetupId]

    try:
        return make_response(jsonify({
            "status": 200,
            "questions": meetup_ques
        }), 200)
    except:
        return make_response(jsonify({
            "message": "No questions from this meetup!"
        }), 200)


""" This route upvotes a question """
@v2.route("/questions/<int:questionId>/upvote", methods=['PATCH'])
@AuthenticationRequired
def upvote_question(questionId):

    questions = Question().fetch_questions()
    question = [que for que in questions if que['id'] == questionId]

    if question:
        Question().vote_on_question(questionId, "upvote")
        return make_response(jsonify({
            "status": 200,
            "data": [{
                "meetup": "{}".format(questionId),
                "title": question[0]['title'],
                "body": question[0]['body'],
                "votes": question[0]['votes']
            }],
            "message": "You have upvoted this question"
        }), 200)
    else:
        return make_response(jsonify({
            "error": "Question not found or does\'nt exist"
        }), 404)


""" This route downvotes a question """
@v2.route("/questions/<int:questionId>/downvote", methods=['PATCH'])
@AuthenticationRequired
def downvote_question(questionId):

    questions = Question().fetch_questions()
    question = [que for que in questions if que['id'] == questionId]

    if question:
        Question().vote_on_question(questionId, "downvote")
        return make_response(jsonify({
            "status": 200,
            "data": [{
                "meetup": "{}".format(questionId),
                "title": question[0]['title'],
                "body": question[0]['body'],
                "votes": question[0]['votes']
            }],
            "message": "You have downvoted this question"
        }), 200)
    else:
        return make_response(jsonify({
            "error": "Question not found or does\'nt exist"
        }), 404)


""" This route edits a question """
@v2.route("questions/<int:questionId>", methods=['PATCH'])
@AuthenticationRequired
def edit_question(questionId):
    data = request.get_json()

    question = Question().fetch_specific_question(questionId)

    if question:

        updates = {
            "title": data['title'],
            "body": data['body']
        }

        Question().edit_question(questionId, updates)
        return jsonify({
            "status": 200,
            "message": "{} was updated".format(question['title'].upper())
        }), 200
    else:
        return make_response(jsonify({
            "error": 'question not found!',
            "status": 404
        }), 404)


""" This route deletes a question """
@v2.route("questions/<int:questionId>", methods=['DELETE'])
@AuthenticationRequired
def delete_question(questionId):

    question = Question().fetch_specific_question(questionId)

    if question:
        Question().delete_question(questionId)
        return jsonify({
            "status": 200,
            "message": "{} was deleted".format(question['title'].upper())
        }), 200
    else:
        return make_response(jsonify({
            "error": 'question not found!',
            "status": 404
        }), 404)
