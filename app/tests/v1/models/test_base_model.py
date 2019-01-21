"""
This module tests that the base model works correctly
"""

# 3rd party imports
import unittest

# local imports
from app.api.v1.models.base_model import BaseModel

class TestBaseModel(unittest.TestCase):

    def test_check_db(self):

        meetup = BaseModel('meetup_db')
        meetup.check_db()
        self.assertEqual(meetup.db_name, 'meetup_db')
        self.assertEqual(meetup.db, meetup.meetups_list)

        questions = BaseModel('question_db')
        questions.check_db()
        self.assertEqual(questions.db_name, 'question_db')
        self.assertEqual(questions.db, questions.questions_list)

        users = BaseModel('user_db')
        users.check_db()
        self.assertEqual(users.db_name, 'user_db')
        self.assertEqual(users.db, users.users_list)

        other = BaseModel('other')
        other.check_db()
        self.assertEqual(other.check_db(), 'Invalid db_name')

    def test_del_item(self):
        pass
    
    def test_edit_item(self):
        pass