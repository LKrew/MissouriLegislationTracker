from typing import Any, Dict

class CalendarEvent:
    def __init__(self, type_id: int, type: str, date: str, time: str, location: str, description: str, event_hash: str):
        self.type_id = type_id
        self.type = type
        self.date = date
        self.time = time
        self.location = location
        self.description = description
        self.event_hash = event_hash

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'CalendarEvent':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__