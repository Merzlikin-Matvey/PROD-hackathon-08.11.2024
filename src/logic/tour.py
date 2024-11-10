import json
import time
import uuid
from src.logic.adapter import Adapter
from src.logic.event import Event, EventType, EventDate

class Tour:
    def __init__(self, name, country=None, events=None, planned_budget=None, _uuid=None):
        self.name = name
        self.country = country
        self.events = events or []
        self.planned_budget = planned_budget
        self.uuid = _uuid or str(uuid.uuid4())

    def add_event(self, event_uuid):
        if event_uuid not in self.events:
            self.events.append(event_uuid)

    def remove_event(self, event_uuid):
        if event_uuid in self.events:
            self.events.remove(event_uuid)

    def __str__(self):
        return f"Tour: {self.name}, Country: {self.country}, Events: {self.events}, Planned Budget: {self.planned_budget}"

    def __repr__(self):
        return self.__str__()

    def save_to_repository(self):
        adapter = Adapter()
        existing_tour = adapter.select_sth_by_uuid('*', 'tours', self.uuid)
        events_json = json.dumps(self.events).replace("'", "''")
        planned_budget_value = self.planned_budget if self.planned_budget is not None else "NULL"
        if existing_tour:
            update_request = f"name='{self.name}', country='{self.country}', events='{events_json}', planned_budget={planned_budget_value}"
            adapter.update('tours', update_request, self.uuid)
        else:
            columns = "uuid, name, country, events, planned_budget"
            values = f"'{self.uuid}', '{self.name}', '{self.country}', '{events_json}', {planned_budget_value}"
            adapter.insert('tours', columns, values)
        return self

    def get_uuid(self):
        return self.uuid

    @staticmethod
    def get_tour_by_uuid(uuid):
        adapter = Adapter()
        if len(str(uuid)) == 0:
            return
        tour_data = adapter.select_sth_by_uuid('*', 'tours', uuid)
        if tour_data:
            tour_data = tour_data[0]
            tour = Tour(
                name=tour_data[2],
                country=tour_data[4],
                events=tour_data[3],
                planned_budget=tour_data[1],
                _uuid=tour_data[0]
            )
            return tour
        return None

    def get_events(self):
        adapter = Adapter()
        events = []

        for event in self.events:
            event_data = adapter.select_sth_by_uuid('*', 'events', event)
            if event_data:
                event_data = event_data[0]
                print(event_data)
                event = Event(
                    name=event_data[4],
                    event_type=EventType(event_data[0]),
                    event_date=EventDate(event_data[1], event_data[2]),
                    event_data=event_data[3],
                    _uuid=event_data[5]
                )
                events.append(event)

        events.sort(key=lambda x: x.event_date.start_date)
        return events

    def get_start(self):
        start_time = None
        for event in self.get_events():
            if not start_time or event.event_date.start_date < start_time:
                start_time = event.event_date.start_date
        return start_time

    def get_end(self):
        end_time = None
        for event in self.get_events():
            if not end_time or event.event_date.end_date > end_time:
                end_time = event.event_date.end_date
        return end_time
