"""
This module contains tests the meetup model 
"""

import unittest

from app.api.v1.models.base_model import BaseModel
from app.api.v1.models.meetup import Meetup

class TestMeetup(unittest.TestCase):

    base_model = BaseModel('meetup_db')

    def setUp(self):

        self.meetup_item = {
            "id": 1,
            "location": 'Nairobi',
            "images": ['img1', 'img2'],
            "topic": 'Python',
            "happeningOn": '15/10/2019',
            "tags": ['Django', 'Flask'],
            "questions": []
        }
        self.meetup = Meetup(self.meetup_item)

    def test_save_meetup(self):
        
        self.meetup.save_meetup()
        meetups = self.meetup.fetch_meetups()

        saved = [item for item in meetups if item['id'] == self.meetup_item['id']]

        self.assertTrue(saved)

    def test_fetch_meetups(self):

        meetups = self.meetup.fetch_meetups()
        self.assertTrue(isinstance(meetups, list))

    def test_fetch_specific_meetup(self):

        self.meetup.save_meetup()
        meetup = self.meetup.fetch_specific_meetup(1)
        self.assertTrue(meetup)
        self.assertEqual(meetup['id'], 1)
        
        meetup2 = self.meetup.fetch_specific_meetup(5)
        self.assertFalse(meetup2)

    def test_edit_meetup(self):

        updates = {"location": "Thika"}
        self.meetup.save_meetup()
        self.meetup.edit_meetup(1, updates)

        meetup = self.meetup.fetch_specific_meetup(1)

        self.assertEqual(meetup['location'], 'Thika')


    def test_delete_meetup(self):

        self.meetup.delete_meetup(1)

        meetup = self.meetup.fetch_specific_meetup(1)

        self.assertFalse(meetup)
