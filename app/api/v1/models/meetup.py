""" This module sets up the meetups model and all it's functionality """

from datetime import datetime

from app.api.v1.models.base_model import BaseModel

class Meetup(BaseModel):

    base_model = BaseModel('meetup_db')

    def __init__(self, meetup={}):

        if meetup:
            self.id = len(self.fetch_meetups())
            self.createdOn = datetime.now()
            self.location = meetup['location']
            self.images = meetup['images']
            self.topic = meetup['topic']
            self.happeningOn = meetup['happeningOn']
            self.tags = meetup['tags']

    def save_meetup(self):

        meetup_item = {
            "id": self.id,
            "createdOn": self.createdOn,
            "location": self.location,
            "images": self.images,
            "topic": self.topic,
            "happeningOn": self.happeningOn,
            "tags": self.tags
        }

        self.base_model.add_item(meetup_item)

    def fetch_meetups(self):

        return self.base_model.meetups_list


    def fetch_specific_meetup(self, id):

        db = self.base_model.meetups_list
        item = [item for item in db if item['id'] == id]

        if item:
            return item[0]
        else:
            return False

    def edit_meetup(self, id, udpates):

        self.base_model.edit_item(id, udpates)

    def delete_meetup(self, id):

        self.base_model.delete_item(id)