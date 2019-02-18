"""
This module sets up the comment model and all it's functionality
"""

import os
from flask import jsonify

from app.api.v2.models.base_model import BaseModel, AuthenticationRequired

class Comment(BaseModel):
    
    def __init__(self, comment={}, database=os.getenv('FLASK_DATABASE_URI')):
    
        self.base_model = BaseModel('comments', database)

        if comment:
            self.comment = comment['comment']
            self.userId = comment['authorId']
            self.questionId = comment['questionId']


    def save_comment(self):
        """ This method saves a comment """

        comment_item = dict(
            userId=self.userId,
            questionId=self.questionId,
            comment=self.comment
        )

        keys = ", ".join(comment_item.keys())
        values = tuple(comment_item.values())
        self.base_model.add_item(keys, values)


    def fetch_comments(self, fields):
        """ This method fetches all comments """

        return self.base_model.grab_all_items(f'{fields}', "True = True")


    def fetch_specific_comment(self, column, condition):
        """ This method fetches a single comment """

        return self.base_model.grab_items_by_name(column, condition)


    def update_comment(self, id, updates):
        """ This method updates a comment """

        pairs_dict = {
            "comment": f"comment = '{updates['comment']}'",
        }
        
        pairs = ", ".join(pairs_dict.values())
        
        if self.fetch_specific_comment('id', f"id = {id}"):
            return self.base_model.update_item(pairs, f"id = {id}")
        else:
            return jsonify({
                "error": "Comment not found or does not exist!",
                "status": 404
            })


    def delete_comment(self, id):
        """ This method deletes a comment """

        if self.fetch_specific_comment('id', f"id = {id}"):
            return self.base_model.delete_item(f"id = {id}")
        else:
            return jsonify({
                "error": "Comment not found or does not exist!",
                "status": 400
            })
