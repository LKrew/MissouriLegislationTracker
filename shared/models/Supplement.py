from typing import Any, Dict

class Supplement:
    def __init__(self, supplement_id: int, date: str, type: str, type_id: int, title: str,
                 description: str, mime: str, mime_id: int, url: str, state_link: str,
                 supplement_size: int, supplement_hash: str, alt_supplement: int, alt_mime: str,
                 alt_mime_id: int, alt_state_link: str, alt_supplement_size: int, alt_supplement_hash: str):
        self.supplement_id = supplement_id
        self.date = date
        self.type = type
        self.type_id = type_id
        self.title = title
        self.description = description
        self.mime = mime
        self.mime_id = mime_id
        self.url = url
        self.state_link = state_link
        self.supplement_size = supplement_size
        self.supplement_hash = supplement_hash
        self.alt_supplement = alt_supplement
        self.alt_mime = alt_mime
        self.alt_mime_id = alt_mime_id
        self.alt_state_link = alt_state_link
        self.alt_supplement_size = alt_supplement_size
        self.alt_supplement_hash = alt_supplement_hash

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Supplement':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__