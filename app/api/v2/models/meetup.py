"""
This module sets up the meetups model and all it's functionality
"""

from datetime import datetime
import os
from flask import jsonify

from app.api.v2.models.question import Question
from app.api.v2.models.base_model import BaseModel, AuthenticationRequired

class Meetup(BaseModel):


    def __init__(self, meetup={}, database=os.getenv('FLASK_DATABASE_URI')):

        self.base_model = BaseModel('meetups', database)

        if meetup:
            self.location = meetup['location']
            self.images = meetup['images']
            self.topic = meetup['topic']
            self.description = meetup['description']
            self.schedule = meetup['happeningOn']
            self.tags = meetup['tags']
            self.id = meetup['id']


    def save_meetup(self):

        meetup_item = dict(
            authorId=self.id,
            topic=self.topic,
            description=self.description,
            schedule=self.schedule,
            location=self.location,
            tags=self.tags,
            images=self.images
        )

        keys = ", ".join(meetup_item.keys())
        values = tuple(meetup_item.values())
        self.base_model.add_item(keys, values)


    def rsvp_meetup(self, rsvp):
        """ This method rsvps on a meetup """

        keys = ", ".join(rsvp.keys())
        values = tuple(rsvp.values())
        self.base_model.add_item_two('rsvps', keys, values)


    def cancel_rsvp(self, id):
        """ This method cancels a rsvp """


    def fetch_rsvps(self, fields, condition):
        """ This method fetches all the meetup ids """

        return self.base_model.grab_items(fields, 'rsvps', condition)


    def fetch_meetups(self, fields):
        """ This method fetches all meetups """

        return self.base_model.grab_all_items(f'{fields}', "True = True")
    

    def fetch_specific_meetup(self, column, condition):
        """ This method fetches a single meetup """

        return self.base_model.grab_items_by_name(column, condition)


    def update_meetup(self, id, updates):
        """ This method defines the update query """

        pairs_dict = {
            "topic": f"topic = '{updates['topic']}'",
            "description": f"description = '{updates['description']}'",
            "location": f"location = '{updates['location']}'",
            "images": f"images = '{updates['images']}'",
            "happeningOn": f"schedule = '{updates['happeningOn']}'",
            "tags": f"tags = '{updates['tags']}'"
        }
        
        pairs = ", ".join(pairs_dict.values())

        
        if self.fetch_specific_meetup('id', f"id = {id}"):
            return self.base_model.update_item(pairs, f"id = {id}")
        else:
            return jsonify({
                "error": "Meetup not found or does not exist!",
                "status": 404
            })


    def delete_meetup(self, id):
        """ This method defines the delete query """

        if self.fetch_specific_meetup('id', f"id = {id}"):
            return self.base_model.delete_item(f"id = {id}")
        else:
            return {
                "error": "Meetup not found or does not exist!"
            }

            