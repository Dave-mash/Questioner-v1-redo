"""
This module sets up the question model and all it's functionality
"""

import os
from flask import jsonify

from app.api.v2.models.base_model import BaseModel, AuthenticationRequired
from app.api.v2.models.user import User

class Question(BaseModel):
    
    def __init__(self, question={}, database=os.getenv('FLASK_DATABASE_URI')):
    
        self.base_model = BaseModel('questions', database)
    
        if question:
            self.title = question['title']
            self.meetupId = question['meetupId']
            self.body = question['body']
            self.authorId = question['authorId']


    def save_question(self):

        question_item = dict(
            title=self.title,
            body=self.body,
            meetupId=self.meetupId,
            authorId=self.authorId
        )

        keys = ", ".join(question_item.keys())
        values = tuple(question_item.values())
        self.base_model.add_item(keys, values)


    def fetch_questions(self, fields, condition, name=''):
        """ This method fetches all questions """

        return self.base_model.grab_all_items(f'{fields}', condition, name)


    def fetch_specific_question(self, column, condition):
        """ This method fetches a single question """

        return self.base_model.grab_items_by_name(column, condition)


    def vote_on_question(self, userId, questionId, vote):
        """ This method votes on a question """
        
        # check that user exists
        if not User().fetch_specific_user('id', f"id = {userId}"):
            return {
                "error": "User not found or does'nt exist",
                "status": 404
            }            
        elif not Question().fetch_specific_question('id', f"id = {questionId}"):
            return {
                "error": "Question not found or does'nt exist",
                "status": 404
            }
        
        # Array --> [(['1', '1', '2'],)]

        updateVote = self.fetch_specific_question('totalVotes', f"id = {questionId}")[0]
        if vote == "upvote":
            updateVote += 1
        elif vote == "downvote":
            updateVote -= 1

        voters_list = self.fetch_questions('voters', f"questionId = {questionId}", 'votes')

        # fetch user & question
        user = { User().fetch_specific_user('id', f"id = {userId}")[0] }
        user_id = {userId}
        question = Question().fetch_specific_question('id', f"id = {questionId}")[0]
       
        # votes item 
        fields = dict(
            voters=str(user), 
            questionId=question
        )

        keys = ", ".join(fields.keys())
        values = tuple(fields.values())

        if voters_list:
            # Check if user has already voted on question
            if str(userId) in voters_list[0][0]:
                return {
                    "error": "Sorry, You can only vote once!",
                    "status": 403
                }
            else:
                question_id = self.base_model.grab_items_by_name('questionId', f"questionId = {questionId}", 'votes')

                # check if questionId exists in votes table
                if question_id:
                    self.base_model.update_item(f"voters = array_cat(voters, '{user_id}')", f"questionId = {questionId}", 'votes')
                    return self.base_model.update_item(f"totalVotes = {updateVote}", f"id = {questionId}")
                else:
                    self.base_model.add_item(keys, values, 'votes')
                    return self.base_model.update_item(f"totalVotes = {updateVote}", f"id = {questionId}")
        else:
            self.base_model.add_item(keys, values, 'votes')
            return self.base_model.update_item(f"totalVotes = {updateVote}", f"id = {questionId}")


    def update_question(self, id, updates):
        """ This method updates a question """

        pairs_dict = {
            "title": f"title = '{updates['title']}'",
            "body": f"body = '{updates['body']}'",
        }
        
        pairs = ", ".join(pairs_dict.values())
        
        if self.fetch_specific_question('id', f"id = {id}"):
            return self.base_model.update_item(pairs, f"id = {id}")
        else:
            return jsonify({
                "error": "Question not found or does not exist!",
                "status": 404
            })


    def delete_question(self, id):
        """ This method deletes a question """

        if self.fetch_specific_question('id', f"id = {id}"):
            return self.base_model.delete_item(f"id = {id}")
        else:
            return {
                "error": "Meetup not found or does not exist!",
                "status": 404
            }
