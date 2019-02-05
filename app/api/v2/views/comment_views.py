"""
This module sets up all the comments endpoints
Author: Dave
"""


from flask import Blueprint
from flask import request, jsonify, make_response, Blueprint

from app.api.v2.models.question import Question, AuthenticationRequired
from app.api.v2.models.meetup import Meetup
from app.api.v2.models.comment import Comment

v2 = Blueprint('commentv2', __name__, url_prefix='/api/v2/')


""" This route posts a comment on a question """
@v2.route("/<int:questionId>/comments", methods=['POST'])
@AuthenticationRequired
def comment_on_question(questionId):
    data = request.get_json()

    try:
        data['comment']
    except:
        return jsonify({
            "error": 'You missed the {} key, value pair'.format(data['comment'])
        })

    questions = Question().fetch_questions()
    question = [question for question in questions if question['id'] == questionId]

    if question:
    
        comment = {
            "question": questionId,
            "title": question[0]['title'],
            "body": question[0]['body'],
            "comment": data['comment']
        }
    
        comment_model = Comment(comment)

        comment_model.save_comment()
    
        return make_response(jsonify({
            "status": 201,
            "message": "You have successfully commented on this question",
            "data": [{
                "question": questionId,
                "title": comment['title'],
                "body": comment['body'],
                "comment": comment['comment']
            }]
        }), 201)
    else:
        return make_response(jsonify({
            "error": "Question not found or does not exist",
            "status": 404
        }), 404)


""" This route edits a comment """
@v2.route("/<int:meetupId>/<int:questionId>/<int:commentId>", methods=['PATCH'])
@AuthenticationRequired
def edit_comment(questionId, commentId, meetupId):
    data = request.get_json()

    meetup = Meetup().fetch_specific_meetup(meetupId)
    question = Question().fetch_specific_question(questionId)
    comment = Comment().fetch_specific_comment(commentId)

    if question and comment and meetup:

        updates = {
            "comment": data['comment']
        }

        Comment().edit_comment(commentId, updates)
        return jsonify({
            "status": 200,
            "message": "Comment with id '{}' was updated".format(commentId)
        }), 200
    else:
        return Comment().errorParser(meetup, question, comment)


""" This route deletes a comment """
@v2.route("/<int:meetupId>/<int:questionId>/<int:commentId>", methods=['DELETE'])
@AuthenticationRequired
def delete_comment(questionId, commentId, meetupId):

    meetup = Meetup().fetch_specific_meetup(meetupId)
    question = Question().fetch_specific_question(questionId)
    comment = Comment().fetch_specific_comment(commentId)

    if question and comment and meetup:
        Comment().delete_comment(commentId)
        return jsonify({
            "status": 200,
            "message": "Comment with id '{}' was deleted".format(commentId)
        }), 200
    else:
        return Comment().errorParser(meetup, question, comment)

