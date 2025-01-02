from typing import Any, Dict

class Subject:
    def __init__(self, subject_id: int, subject_name: str):
        self.subject_id = subject_id
        self.subject_name = subject_name

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Subject':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__