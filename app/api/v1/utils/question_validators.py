"""
This module takes care of validating input from the endpoints
"""

from app.api.v1.models.base_model import BaseModel
from app.api.v1.utils.meetup_validators import MeetupValidator

class QuestionValidator(MeetupValidator):

    def __init__(self, title='', description=''):
        self.title = title
        self.description = description

    def data_exists(self):
        if not self.title or not self.description:
            return 'You missed a required field'

    def valid_title(self):
        if len(self.title) < 20:
            return 'Your question is too short. Try being abit more descriptive'

# Access valid_description from MeetupValidator