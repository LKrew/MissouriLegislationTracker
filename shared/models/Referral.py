from typing import Any, Dict, Optional

class Referral:
    def __init__(self, date: str, committee_id: int, chamber: Optional[str] = None, chamber_id: Optional[int] = None, name: Optional[str] = None):
        self.date = date
        self.committee_id = committee_id
        self.chamber = chamber
        self.chamber_id = chamber_id
        self.name = name

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Referral':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__