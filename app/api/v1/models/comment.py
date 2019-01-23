"""
This module sets up the comment model and all it's functionality
"""

from datetime import datetime

from app.api.v1.models.base_model import BaseModel

class Comment(BaseModel):
    
    base_model = BaseModel('comment_db')

    def __init__(self, comment={}):

        if comment:
            self.id = len(self.fetch_comments())
            self.createdOn = datetime.now()
            self.question = comment['question']
            self.title = comment['title']
            self.body = comment['body']
            self.comment = comment['comment']

    def save_comment(self):

        comment_item = {
            "id": self.id,
            "question": self.question,
            "createdOn": self.createdOn,
            "title": self.title,
            "body": self.body,
            "comment": self.comment
        }

        self.base_model.add_item(comment_item)

    def fetch_comments(self):

        return self.base_model.comments_list

    def fetch_specific_comment(self, id):

        db = self.base_model.comments_list
        comment = [comment for comment in db if comment['id'] == id]

        if comment:
            return comment[0]
        else:
            return False


    def edit_comment(self, id, udpates):

        self.base_model.edit_item(id, udpates)

    def delete_comment(self, id):

        self.base_model.delete_item(id)