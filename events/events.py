from enums.enums import EventType
from events.data import EventData


'''
這邊放Event
'''


class Event:
    _listeners = []

    def __init__(self, event_type: EventType, data: EventData):
        self.event_type = event_type
        self.data = data

    @classmethod
    def add_listener(cls, listener):
        cls._listeners.append(listener)

    def emit(self):
        for listener in self._listeners:
            listener(self)