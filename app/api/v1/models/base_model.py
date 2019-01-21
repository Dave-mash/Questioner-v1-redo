"""
This module serves as a database mock-up for the project
"""

meetups_list = []
questions_list = []
users_list = []

class BaseModel:

    def __init__(self, db_name=''):

        if isinstance(db_name, str):
            self.db_name = db_name
        else:
            print('db_name must be a string')

        self.db = None
        self.meetups_list = meetups_list
        self.questions_list = questions_list
        self.users_list = users_list

    def check_db(self):
        if self.db_name == 'meetup_db':
            self.db = self.meetups_list
        elif self.db_name == 'question_db':
            self.db = self.questions_list
        elif self.db_name == 'user_db':
            self.db = self.users_list
        else:
            self.db = None
            return'Invalid db_name'

    def delete_item(self, item_id):
        self.check_db()
        del_item = [item for item in self.db if item['id'] == item_id]

        if del_item:
            self.db.remove(del_item[0])
        else:
            return "No item"

    def edit_item(self, item_id, updates):
        self.check_db()
        edit_item = [item for item in self.db if item['id'] == item_id]

        if edit_item:
            edit_item[0].update(updates)
        else: 
            return "No item"