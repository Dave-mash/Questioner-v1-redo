"""
This module sets up all the comments endpoints
Author: Dave
"""


from flask import Blueprint
from flask import request, jsonify, make_response, Blueprint

from app.api.v2.models.question import Question, AuthenticationRequired
from app.api.v2.models.comment import Comment
from app.api.v2.models.user import User

v2 = Blueprint('commentv2', __name__, url_prefix='/api/v2/')


""" This route posts a comment on a question """
@v2.route("/<int:userId>/<int:questionId>/comments", methods=['POST'])
@AuthenticationRequired
def comment_on_question(questionId, userId):
    data = request.get_json()

    try:
        data['comment']
    except:
        return jsonify({
            "error": 'You missed the {} key, value pair'.format(data['comment'])
        })
        
    question = Question().fetch_specific_question('id', f"id = {questionId}")
    user = User().fetch_specific_user('id', f"id = {userId}")

    if question and user:
    
        comment = {
            "authorId": userId,
            "comment": data['comment'],
            "questionId": questionId,
        }

        comment_model = Comment(comment)

        comment_model.save_comment()
    
        return make_response(jsonify({
            "status": 201,
            "message": "You have successfully commented on this question",
            "data": [{
                "question": questionId,
                "comment": comment['comment']
            }]
        }), 201)
    elif not question:
        return make_response(jsonify({
            "error": "Question not found or does not exist",
            "status": 404
        }), 404)
    elif not user:
        return make_response(jsonify({
            "error": "User not found or does not exist",
            "status": 404
        }), 404)


""" This route updates a comment """
@v2.route("/<int:userId>/comments/<int:commentId>", methods=['PUT'])
@AuthenticationRequired
def edit_comment(userId, commentId):
    data = request.get_json()

    try:
        data['comment']
    except:
        return jsonify({
            "error": 'You missed the {} key, value pair'.format(data['comment'])
        })
     
    if Comment().fetch_specific_comment('userId', f"id = {commentId}")[0] == userId:
        
        comment = Comment().update_comment(commentId, data)
        
        if isinstance(comment, dict):
            return make_response(comment, 404)
        else:
            return make_response(jsonify({
                "message": "You have successfully updated this comment",
                "status": 200
            }), 200)
    else:
        return make_response(jsonify({
            "error": "You are not authorized to perform this action!",
            "status": 401
        }), 401)
        

""" This route deletes a comment """
@v2.route("/<int:userId>/comments/<int:commentId>", methods=['DELETE'])
@AuthenticationRequired
def delete_comment(userId, commentId):

    if Comment().fetch_specific_comment('userId', f"id = {commentId}")[0] == userId:
        
        comment = Comment().delete_comment(commentId)

        if isinstance(comment, dict):
            return make_response(jsonify(comment), 404)
        else:
            return make_response(jsonify({
                "error": 'comment was deleted successfully',
                "status": 200
            }), 200)
    else:
        return make_response(jsonify({
            "error": "You are not authorized to perform this action!",
            "status": 401
        }), 401)

