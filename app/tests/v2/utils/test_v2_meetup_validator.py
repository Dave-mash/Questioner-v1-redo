"""
This module tests the meetup_validator endpoint
"""

import unittest
from app.api.v2.utils.question_validators import MeetupValidator

class TestQuestionsValidator(unittest.TestCase):

    def setUp(self):
        """ Initializes app """
        self.meetup = {
            "title": "a meetup",
            "description": "this is a meetup",
            "tags": ['Django', 'Flask'],
            "images": "[img1]",
            "happeningOn": "12-12-2019",
            "location": "Nairobi"
        }

    def test_meetup_data_exists(self):
        meetup = { **self.meetup }
        meetup['title'] = ''
        meetup['description'] = ''
        question = MeetupValidator(meetup)
        self.assertEqual(question.data_exists(), 'You missed a required field')  

    def test_invalid_data(self):

        meetup = { **self.meetup }
        meetup['title'] = 'b'
        question = MeetupValidator(meetup)
        self.assertEqual(question.valid_title(), 'Your title is too short!')

        meetup = { **self.meetup }
        meetup['description'] = 'T'
        question = MeetupValidator(meetup)
        self.assertEqual(question.valid_description(), 'Your description is too short')

        meetup = { **self.meetup }
        meetup['tags'] = []
        question = MeetupValidator(meetup)
        self.assertEqual(question.valid_tags(), 'Have at least one tag')

        meetup = { **self.meetup }
        meetup['happeningOn'] = '12/12/2019'
        question = MeetupValidator(meetup)
        self.assertEqual(question.valid_date(), 'Date format should be DD-MM-YYYY')

        meetup = { **self.meetup }
        meetup['location'] = 'N'
        question = MeetupValidator(meetup)
        self.assertEqual(question.valid_location(), 'Enter a valid location!')
