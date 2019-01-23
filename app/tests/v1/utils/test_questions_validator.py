"""
This module tests the questions_validator endpoint
"""

import unittest
from app.api.v1.utils.question_validators import QuestionValidator

class TestQuestionsValidator(unittest.TestCase):

    def setUp(self):
        """ Initializes app """
        self.question = {
            "title": "Python",
            "description": "This is python code"
        }

    def test_question_data_exists(self):
        question = QuestionValidator('', '')
        self.assertEqual(question.data_exists(), 'You missed a required field')  

    def test_invalid_data(self):
        question = QuestionValidator('b', 'This is python')
        self.assertEqual(question.valid_title(), 'Your question is too short. Try being abit more descriptive')

        question = QuestionValidator('Python', 'T')
        self.assertEqual(question.valid_description(), 'Your description is too short')
