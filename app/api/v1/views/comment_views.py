"""
This module sets up all the comments endpoints
Author: Dave
"""


from flask import Blueprint
from flask import request, jsonify, make_response, Blueprint

from app.api.v1.models.question import Question
from app.api.v1.models.meetup import Meetup
from app.api.v1.models.comment import Comment

v1 = Blueprint('commentv1', __name__, url_prefix='/api/v1/')


def errorParser(meetup, question, comment):

    def error(error):
        return make_response(jsonify({
            "status": 404,
            "error": "No {} found!".format(error)
        }))

    if not meetup:
        return error('meetup')

    elif not question:
        return error('question')

    elif not comment:
        return error('comment')


""" This route posts a comment on a question """
@v1.route("/<int:questionId>/comments", methods=['POST'])
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
@v1.route("/<int:meetupId>/<int:questionId>/<int:commentId>", methods=['PATCH'])
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
        return errorParser(meetup, question, comment)


""" This route deletes a comment """
@v1.route("/<int:meetupId>/<int:questionId>/<int:commentId>", methods=['DELETE'])
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
        return errorParser(meetup, question, comment)

