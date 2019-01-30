# import unittest
# import datetime
# import json

# from app import create_app

# class TestMeetup(unittest.TestCase):

#     comments = []

#     def create_user(self):
#         """ simulate a fake user """
#         username = "".join(choice(
#                            string.ascii_letters) for x in range(randint(7, 10)))
#         params = {
#             "first_name": "Dave",
#             "last_name": "mwas",
#             "othername" : "mash",
#             "email": "{}@gmail.com".format(username),
#             "username": username,
#             "phoneNumber" : "+254729710290",
#             "password": "abc123@1A",
#             "confirm_password": "abc123@1A"
#         }
        
#         res = self.client.post("/api/v1/auth/signup",
#                                 data=json.dumps(params),
#                                 content_type="application/json")

#         user_id = res.json['user_id']
#         auth_token = res.json['auth_token']
#         return user_id, auth_token

#     def setUp(self):
#         """ Initializes app"""

#         self.app = create_app('testing')
#         self.client = self.app.test_client()
#         self.comment = {
#             "id": 0,
#             "question": 0,
#             "createdOn": "12/12/2019",
#             "title": "Python",
#             "body": "What are Python data structures?",
#             "comment": "This is Python!"
#         }
#         self.meetup = {
#             "id": 0,
#             "createdOn": "05/10/2019",
#             "topic": "a meetup",
#             "description": "this is a meetup",
#             "location": "Nairobi",
#             "happeningOn": "12-12-2019",
#             "tags": "['Django', 'Flask']"
#         }
#         self.question = {
#             "title": "Python",
#             "body": "What are Python Data structures?",
#             "id": 0,
#             "createdOn": "10/10/2019",
#             "meetupId": 0,
#             "votes": 0
#         }

#     def post_req(self, path='api/v1/0/comments', auth_token=1, data={}, headers=None):
#         """ This function utilizes the test client to send POST requests """
#         data = data if data else self.meetup
#         if auth_token is 1:
#             user = self.create_user()
#             auth_token = user[1]
#         if not headers:
#             headers = {"Authorization": "Bearer {}".format(auth_token)}

#         res = self.client.post(
#             path,
#             data=json.dumps(data),
#             headers=headers,
#             content_type='application/json'
#         )
#         return res

#     def get_req(self, path):
#         """ This function utilizes the test client to send GET requests """
        
#         res = self.client.get(path)
#         return res

#     # def test_post_a_comment(self):
#     #     """ Test that a user can post a comment to a question """

#     #     # test non-existing question
#     #     payload = self.post_req()
#     #     # self.assertEqual(payload.json['error'], "Question not found or does not exist")

#     #     # test existing question
#     #     # self.post_req(path="api/v1/meetups", data=self.meetup)
#     #     # self.post_req(path="api/v1/0/questions", data=self.question)
#     #     payload = self.post_req()
#         # self.assertEqual(self.get_req('api/v1/0/questions').status_code, 200)
#         # self.assertEqual(payload.json['message'], "You have successfully commented on this question")
        