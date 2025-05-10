from enums.enums import EventType
from events.data import EventData
from events.events import Event
from typing import Callable


class EventListener:
    def __init__(self):
        self._mapping: dict[EventType, Callable[[EventData], None]] = {}
        Event.add_listener(self.listen)
    
    def add_handler(self, event_type: EventType, handler: Callable[[EventData], None]):
        self._mapping[event_type] = handler

    def get_handler(self, event_type: EventType) -> Callable[[EventData], None] | None:
        return self._mapping.get(event_type)
    
    def listen(self, event: Event):
        handler = self.get_handler(event.event_type)
        if not handler:
            return
        handler(event.data)