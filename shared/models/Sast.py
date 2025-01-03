from typing import Any, Dict

class Sast:
    def __init__(self, type_id: int, type: str, sast_bill_number: str, sast_bill_id: int):
        self.type_id = type_id
        self.type = type
        self.sast_bill_number = sast_bill_number
        self.sast_bill_id = sast_bill_id

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Sast':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__