"""
This module takes care of validating input from the endpoints
"""

from app.api.v1.models.base_model import BaseModel
from app.api.v1.utils.meetup_validators import MeetupValidator

class QuestionValidator(MeetupValidator):

    def __init__(self, data={}):
        if data:
            self.title = data['title']
            self.body = data['body']

    # Validator methods
    def question_fields(self, data):
        
        fields = ['title', 'body']
        for key in fields:
            try:
                data[key]
            except:
                return {
                    "error": 'You missed the {} key, value pair'.format(key),
                    "status": 400
                }

    def data_exists(self):
        if not self.title:
            return "Title is a required field!"
        elif not self.body:
            return "body is a required field!"

    def valid_que(self):
        if len(self.body) < 5:
            return "Your question is too short. Try being abit more descriptive"
        elif len(self.title) < 3:
            return "Your title is too short!"