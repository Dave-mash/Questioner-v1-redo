"""
This module sets up tests for the question model 
"""

import unittest

from app.api.v1.models.base_model import BaseModel
from app.api.v1.models.question import Question

class TestQuestion(unittest.TestCase):

    base_model = BaseModel('question_db')

    def setUp(self):

        self.question_item = {
            "id": 1,
            "createdOn": "10/10/2019",
            "title": "Python",
            "meetupId": 0,
            "body": "What are python data structures?",
            "votes": 0
        }
        self.question = Question(self.question_item)

    def test_save_question(self):
        """ Test that a user posts a question it's saved """
        
        self.question.save_question()
        questions = self.question.fetch_questions()

        saved = [item for item in questions if item['id'] == self.question_item['id']]

        self.assertTrue(saved)

    def test_fetch_questions(self):
        """ Test that a user can fetch all question on a meetup """

        questions = self.question.fetch_questions()
        self.assertTrue(isinstance(questions, list))

    def test_fetch_specific_question(self):
        """ Test that a user can fetch a specific question on a meetup """

        self.question.save_question()
        question = self.question.fetch_specific_question(1)
        self.assertTrue(question)
        self.assertEqual(question['id'], 1)
        
        question2 = self.question.fetch_specific_question(5)
        self.assertFalse(question2)

    def test_vote_on_question(self):
        """ Test that a user can vote on a question """
        self.question.save_question()
        question = self.question.fetch_specific_question(1)

        self.question.vote_on_question(question['id'], "upvote")
        self.assertEqual(question['votes'], 1)

        self.question.vote_on_question(question['id'], "downvote")
        self.assertEqual(question['votes'], 0)

    def test_edit_question(self):
        """ Test that a user can edit a question on a meetup """

        updates = {"title": "Django"}
        self.question.save_question()
        self.question.edit_question(1, updates)

        question = self.question.fetch_specific_question(1)

        self.assertEqual(question['title'], 'Django')


    def test_delete_question(self):
        """ Test that a user can delete a question on a meetup """

        self.question.delete_question(1)
        question = self.question.fetch_specific_question(1)

        self.assertFalse(question)
