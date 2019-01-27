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
            "body": "This is python code"
        }
        self.question = QuestionValidator(self.question)

    def test_question_data_exists(self):
        question_data = {
            "title": '',
            "body": "This is Python?"
        }
        question = QuestionValidator(question_data)
        self.assertEqual(question.data_exists(), 'Title is a required field!')  
        question_data2 = {
            "title": 'Python',
            "body": ''
        }
        question = QuestionValidator(question_data2)
        self.assertEqual(question.data_exists(), 'body is a required field!')  

    def test_question_fields(self):
        data = {
            "body": "This is python code"           
        }
        validate = QuestionValidator().question_fields(data)
        self.assertEqual(validate, {
            "error": "You missed the title key, value pair",
            "status": 400
        })

    def test_valid_que(self):
        que = {
            "title": "p",
            "body": "Is this Python?"
        }
        question = QuestionValidator(que)
        self.assertEqual(question.valid_que(), "Your title is too short!")
