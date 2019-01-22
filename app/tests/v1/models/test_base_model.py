"""
This module tests that the base model works correctly
"""

# 3rd party imports
import unittest

# local imports
from app.api.v1.models.base_model import BaseModel

class TestBaseModel(unittest.TestCase):

    def setUp(self):
        self.meetup = BaseModel('meetup_db')
        self.questions = BaseModel('question_db')
        self.users = BaseModel('user_db')

        self.meetup_item = {"content": 'item', "id": 1}
        self.user_item = {"question": 'a question', "id": 1}
        self.question_item = {"name": 'dave', "id": 1}

    def test_check_db(self):
        """ Test base model's check_db method  works as expected """

        # test meetup_db
        self.meetup.check_db()
        self.assertEqual(self.meetup.db_name, 'meetup_db')
        self.assertEqual(self.meetup.db, self.meetup.meetups_list)

        # test question_db
        self.questions.check_db()
        self.assertEqual(self.questions.db_name, 'question_db')
        self.assertEqual(self.questions.db, self.questions.questions_list)

        # test user_db
        self.users.check_db()
        self.assertEqual(self.users.db_name, 'user_db')
        self.assertEqual(self.users.db, self.users.users_list)

        # test invalid db_name
        other = BaseModel('other')
        other.check_db()
        self.assertEqual(other.check_db(), 'Invalid db_name')

    def test_add_item(self):
        """ Test base model's add_item method works as expected """

        # test meetup_db
        self.meetup.add_item(self.meetup_item)
        self.assertTrue(self.meetup.meetups_list)
        self.assertEqual(self.meetup.meetups_list[0], self.meetup_item)

        # test question_db
        self.questions.add_item(self.question_item)
        self.assertTrue(self.questions.meetups_list)
        self.assertEqual(self.questions.questions_list[0], self.question_item)

        # test users_db
        self.users.add_item(self.user_item)
        self.assertTrue(self.users.users_list)
        self.assertEqual(self.users.users_list[0], self.user_item)


    def test_edit_item(self):
        """ Test base model's delete method  works as expected """

        updates = {"id": 20}

        # test no id found
        self.assertEqual(BaseModel('meetup_db').edit_item(10, updates), "No item")

        # test meetups list
        self.meetup.add_item(self.meetup_item)
        self.meetup.edit_item(1, updates)
        self.assertEqual(self.meetup.meetups_list[0]['id'], 20)

        # test questions list
        self.questions.add_item(self.question_item)
        self.questions.edit_item(1, updates)
        self.assertEqual(self.questions.questions_list[0]['id'], 20)

        # test users list
        self.users.add_item(self.user_item)
        self.users.edit_item(1, updates)
        self.assertEqual(self.users.users_list[0]['id'], 20)

        
    def test_del_item(self):
        """ Test base model's delete method  works as expected """

        # test no id found
        self.assertEqual(BaseModel('meetup_db').delete_item(10), "No item")

        # test meetups list
        self.meetup.delete_item(1)
        self.assertFalse(self.meetup.db)

        # test questions list
        self.questions.delete_item(1)
        self.assertFalse(self.questions.db)

        # test users list
        self.users.delete_item(1)
        self.assertFalse(self.users.db)
    
    def tearDown(self):

        self.meetup_item = {}
        self.user_item = {}
        self.question_item = {}