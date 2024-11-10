from src.logic.adapter import Adapter
from dotenv import load_dotenv
import os
from src.logic.tour import Tour

load_dotenv(dotenv_path='./.env', verbose=True)

# src/logic/user.py

class User:
    def __init__(self, email):
        db = Adapter(host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), dbname=os.getenv('DB_NAME'), sslmode="verify-full", user="Admin", password=os.getenv('DB_PASSWORD'), target_session_attrs="read-write")
        userdata = db.sel_userdata_by_email(email=email)
        self.uuid = userdata['uuid']
        self.name = userdata['username']
        self.email = email
        self.tour_uuids = userdata.get('tour_uuids', [])
        if isinstance(self.tour_uuids, str):
            self.tour_uuids = self.tour_uuids.strip('{}').split(',')
        self.event_uuids = userdata.get('event_uuids', [])
        if isinstance(self.event_uuids, str):
            self.event_uuids = self.event_uuids.strip('{}').split(',')
        self.airline = userdata.get('airline', False)
        self.db = db
        self.is_active = userdata['is_active']

    def _update_user_data(self):
        tour_uuids_str = '{' + ','.join(map(str, filter(None, self.tour_uuids))) + '}'
        event_uuids_str = '{' + ','.join(map(str, filter(None, self.event_uuids))) + '}'
        update_request = f"tour_uuids = '{tour_uuids_str}', event_uuids = '{event_uuids_str}', airline = {self.airline}"
        self.db.update('users', update_request, self.uuid)

    def _update_user_data(self):
        tour_uuids_str = '{' + ','.join(map(str, filter(None, self.tour_uuids))) + '}'
        event_uuids_str = '{' + ','.join(map(str, filter(None, self.event_uuids))) + '}'
        airlines_str = '{' + ','.join(map(str, filter(None, self.airlines))) + '}'
        update_request = f"tour_uuids = '{tour_uuids_str}', event_uuids = '{event_uuids_str}', airlines = '{airlines_str}'"
        self.db.update('users', update_request, self.uuid)


    def remove_event(self, event_uuid, tour_uuid=None):
        tour = Tour.get_tour_by_uuid(tour_uuid)
        if tour:
            tour.remove_event(event_uuid)
            return

    def get_all_tours(self):
        return self.tour_uuids

    def _update_user_data(self):
        tour_uuids_str = '{' + ','.join(map(str, filter(None, self.tour_uuids))) + '}'
        event_uuids_str = '{' + ','.join(map(str, filter(None, self.event_uuids))) + '}'
        update_request = f"tour_uuids = '{tour_uuids_str}', event_uuids = '{event_uuids_str}', airline = {self.airline}"
        self.db.update('users', update_request, self.uuid)