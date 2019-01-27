"""
This module sets up tests for the comment module
"""

import unittest

from app.api.v1.models.base_model import BaseModel
from app.api.v1.models.comment import Comment

class TestComment(unittest.TestCase):
    
    base_model = BaseModel('comment_db')

    def setUp(self):

        self.comment_item = {
            "id": 0,
            "question": 1,
            "createdOn": "12-12-2019",
            "title": "Python",
            "body": "This is python",
            "comment": "This is a comment!"
        }

        self.comment = Comment(self.comment_item)

    def test_save_comment(self):
        length = len(self.base_model.comments_list)
        self.comment.save_comment()
        self.assertEqual(len(self.base_model.comments_list), length + 1)

    def test_fetch_comments(self):
        self.assertEqual(len(self.comment.fetch_comments()), 1)

    def test_fetch_specific_comment(self):
        comment = self.comment.fetch_specific_comment(0)
        self.assertEqual(comment['body'], "This is python")
        self.assertEqual(comment['question'], 1)

    def test_delete_comment(self):
        comment = self.comment.fetch_specific_comment(0)
        self.comment.delete_comment(0)
        self.assertFalse(comment)

    def test_edit_comment(self):
        self.comment.save_comment()
        updates = { "comment": "An updated comment" }
        self.comment.edit_comment(0, updates)
        comment = self.comment.fetch_specific_comment(0)
        self.assertEqual(comment['comment'], "An updated comment")

    def test_error_parser(self):
        
        self.assertEqual(self.comment.errorParser(False, True, True), { "error": "No meetup found!" })
        self.assertEqual(self.comment.errorParser(True, False, True), { "error": "No question found!" })
        self.assertEqual(self.comment.errorParser(True, True, False), { "error": "No comment found!" })
