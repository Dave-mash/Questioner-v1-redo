"""
This module takes care of validating input from the endpoints
"""

from datetime import datetime

class MeetupValidator:

    def __init__(self, meetupObj={}):
        self.title = meetupObj['topic']
        self.tags = meetupObj['tags']
        self.happeningOn = meetupObj['happeningOn']
        self.description = meetupObj['description']
        self.location = meetupObj['location']
        self.meetupObj = meetupObj

    def data_exists(self):
        if not self.title or not self.happeningOn or not self.description or not self.location:
            return 'You missed a required field'

    def valid_topic(self):
        if len(self.title) < 3:
            return 'Your topic is too short!'
        elif len(self.title) > 30:
            return 'Your topic is too long!'

    def valid_description(self):
        if len(self.description) < 5:
            return 'Your description is too short'

    def valid_tags(self):
        if len(self.tags) == 0:
            return 'Have at least one tag'

    def valid_date(self):
        try:
            datetime.strptime(self.happeningOn, '%d-%m-%Y')
        except:
            return 'Date format should be YYYY-MM-DD'

    def valid_location(self):
        if len(self.location) < 3:
            return 'Enter a valid location!'
