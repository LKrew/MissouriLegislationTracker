from typing import Any, Dict, Optional

class History:
    def __init__(self, date: str, action: str, chamber: str, chamber_id: Optional[int] = None, importance: Optional[int] = None):
        self.date = date
        self.action = action
        self.chamber = chamber
        self.chamber_id = chamber_id
        self.importance = importance

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'History':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__