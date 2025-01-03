from typing import Any, Dict
from .Enums import MimeType

class Amendment:
    def __init__(self, amendment_id: int, chamber: str, chamber_id: int, bill_id: int, adopted: bool, date: str, title: str, description: str, mime: MimeType, mime_id: int, amendment_size: int, amendment_hash: str, doc: str):
        self.amendment_id = amendment_id
        self.chamber = chamber
        self.chamber_id = chamber_id
        self.bill_id = bill_id
        self.adopted = adopted
        self.date = date
        self.title = title
        self.description = description
        self.mime = mime
        self.mime_id = mime_id
        self.amendment_size = amendment_size
        self.amendment_hash = amendment_hash
        self.doc = doc

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Amendment':
        data['mime'] = MimeType(data['mime'])
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'amendment_id': self.amendment_id,
            'chamber': self.chamber,
            'chamber_id': self.chamber_id,
            'bill_id': self.bill_id,
            'adopted': self.adopted,
            'date': self.date,
            'title': self.title,
            'description': self.description,
            'mime': self.mime.value,
            'mime_id': self.mime_id,
            'amendment_size': self.amendment_size,
            'amendment_hash': self.amendment_hash,
            'doc': self.doc
        }