"""
This module sets up the question model and all it's functionality
"""

from datetime import datetime

from app.api.v2.models.base_model import BaseModel, AuthenticationRequired

class Question(BaseModel):
    
    base_model = BaseModel('question_db')

    def __init__(self, question={}):

        if question:
            self.id = len(self.fetch_questions())
            self.createdOn = datetime.now()
            self.title = question['title']
            self.meetupId = question['meetupId']
            self.body = question['body']

    def save_question(self):

        question_item = {
            "title": self.title,
            "body": self.body,
            "id": self.id,
            "createdOn": self.createdOn,
            "meetupId": self.meetupId,
            "votes": 0
        }

        self.base_model.add_item(question_item)

    def fetch_questions(self):

        return self.base_model.questions_list


    def fetch_specific_question(self, id):

        db = self.base_model.questions_list
        que = [que for que in db if que['id'] == id]

        if que:
            return que[0]
        else:
            return False

    def vote_on_question(self, id, vote):

        question = self.fetch_specific_question(id)

        if vote == "upvote":
            question['votes'] += 1
        elif vote == "downvote":
            question['votes'] -= 1

    def edit_question(self, id, udpates):

        self.base_model.edit_item(id, udpates)

    def delete_question(self, id):

        self.base_model.delete_item(id)