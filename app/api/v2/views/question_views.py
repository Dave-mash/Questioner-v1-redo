"""
This module sets up all the question endpoints
Author: Dave
"""

from flask import request, jsonify, make_response, Blueprint

from app.api.v2.models.question import Question, AuthenticationRequired
from app.api.v2.utils.question_validators import QuestionValidator
from app.api.v2.models.meetup import Meetup
from app.api.v2.models.user import User

v2 = Blueprint('questionv2', __name__, url_prefix='/api/v2/')


def vote(questionId, userId, vote):
    """ This function defines the votes functionality """
    
    voters_list = Question().vote_on_question(userId, questionId, vote)

    if isinstance(voters_list, dict):
        
        return make_response(jsonify(voters_list), voters_list['status'])
    else:
        return make_response(jsonify({
            "status": 200,
            "data": [{
                "meetup": f"{questionId}"
            }],
            "message": f"You have {vote} this question"
        }), 200)


""" This route posts a question """
@v2.route("/<int:userId>/<int:meetupId>/questions", methods=['POST'])
@AuthenticationRequired
def post_a_question(meetupId, userId):
    data = request.get_json()
    
    if QuestionValidator().question_fields(data):
        return make_response(jsonify(QuestionValidator().question_fields(data)), 400)
    else:
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
            
        meetup = Meetup().fetch_specific_meetup('id', f"id = {meetupId}")
        user = User().fetch_specific_user('id', f"id = {userId}")

        question = {
            "authorId": userId,
            "title": data['title'],
            "body": data['body'],
            "meetupId": meetupId
        }
        
        if meetup and user:

            question_model = Question(question)
            question_model.save_question()

            return make_response(jsonify({
                "status": 201,
                "message": "You have successfully posted a question",
                "data": [{
                    "title": data['title'],
                    "body": data['body'],
                    "meetup": meetupId,
                    "user": userId
                }]
            }), 201)
        elif not meetup:
            return make_response(jsonify({
                "error": "Meetup not found or does not exist!",
                "status": 404
            }), 404)
        elif not user:
            return make_response(jsonify({
                "error": "Please create an account first!",
                "status": 403
            }), 403)


""" This route displays a meetup's questions """
@v2.route("/<int:meetupId>/questions", methods=['GET'])
def meetup_questions(meetupId):

    if not Meetup().fetch_specific_meetup('id', f"id = {meetupId}"):
        return make_response(jsonify({
            "error": "Meetup not found or does not exist!",
            "status": 404
        }), 404)

    try:
        questions = Question().fetch_questions('(title, body)', f"meetupId = {meetupId}")[0]
        return make_response(jsonify({
            "status": 200,
            "questions": questions
        }), 200)
    except:
        return make_response(jsonify({
            "message": "No questions on this meetup!",
            "status": 200
        }), 200)


""" This route upvotes a question """
@v2.route("/<int:userId>/questions/<int:questionId>/upvote", methods=['PATCH'])
@AuthenticationRequired
def upvote_question(questionId, userId):

    return vote(questionId, userId, "upvote")


""" This route downvotes a question """
@v2.route("<int:userId>/questions/<int:questionId>/downvote", methods=['PATCH'])
@AuthenticationRequired
def downvote_question(userId, questionId):

    return vote(questionId, userId, "downvote")


""" This route updates a question """
@v2.route("/<int:userId>/questions/<int:questionId>", methods=['PUT'])
@AuthenticationRequired
def edit_question(questionId, userId):
    data = request.get_json()
    
    if QuestionValidator().question_fields(data):
        return make_response(jsonify(QuestionValidator().question_fields(data)), 400)
    else:
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

    if Question().fetch_specific_question('authorId', f"id = {questionId}")[0] == userId:

        question = Question().update_question(questionId, data)

        if isinstance(question, dict):
            return make_response(question)
        else:
            return make_response(jsonify({
                "message": "You have successfully updated this question",
                "status": 200
            }), 200)
    else:
        return make_response(jsonify({
            "error": "You are not authorized to perform this action!",
            "status": 401
        }), 401)


""" This route deletes a question """
@v2.route("<int:userId>/questions/<int:questionId>", methods=['DELETE'])
@AuthenticationRequired
def delete_question(questionId, userId):

    if Question().fetch_specific_question('authorId', f"id = {questionId}")[0] == userId:
        
        question = Question().delete_question(questionId)

        if isinstance(question, dict):
            return make_response(jsonify(question), 404)
        else:
            return make_response(jsonify({
                "error": 'question was deleted successfully',
                "status": 200
            }), 200)
    else:
        return make_response(jsonify({
            "error": "You are not authorized to perform this action!",
            "status": 401
        }), 401)