"""
This module takes care of validating input from the endpoints
"""

from datetime import datetime

class MeetupValidator:

    def __init__(self, meetup={}):

        if meetup:
            self.title = meetup['title']
            self.description = meetup['description']
            self.location = meetup['location']
            self.images = meetup['images']
            self.happeningOn = meetup['happeningOn']
            self.tags = meetup['tags']
            self.meetup = meetup

    def errorHandler(self, error_name):
        errors = {
            "title": "Enter a valid title!",
            "location": "Enter a valid location!",
            "description": "Enter a valid description!"
        }

        return errors[error_name]

    def meetup_fields(self, data):
        fields = ['title', 'description', 'location', 'images', 'happeningOn', 'tags']
    
        for key in fields:
            try:
                data[key]
            except:
                return {
                    "error": 'You missed the {} key, value pair'.format(key),
                    "status": 400
                }

    def data_exists(self):
        if not self.title or not self.happeningOn or not self.description or not self.location:
            return 'You missed a required field'

    def valid_title(self):
        if not self.title.isalpha():
            return self.errorHandler("title")
        elif len(self.title) < 3:
            return 'Your title is too short!'
        elif len(self.title) > 30:
            return 'Your title is too long!'

    def valid_description(self):
        if not self.description.isalpha():
            return self.errorHandler('description')
        elif len(self.description) < 5:
            return 'Your description is too short'

    def valid_tags(self):
        if len(self.tags) == 0:
            return 'Have at least one tag'

    def valid_date(self):
        try:
            datetime.strptime(self.happeningOn, '%d-%m-%Y')
        except:
            return 'Date format should be DD-MM-YYYY'

    def valid_location(self):
        if not self.location.isalpha():
            return self.errorHandler('location')
        elif len(self.location) < 3:
            return 'Enter a valid location!'
