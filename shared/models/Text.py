from typing import Any, Dict
from .Enums import MimeType, TextType

class Text:
    def __init__(self, doc_id: int, date: str, type: TextType, type_id: int, mime: MimeType, mime_id: int, url: str, state_link: str, text_size: int, text_hash: str, alt_bill_text: int, alt_mime: str, alt_mime_id: int, alt_state_link: str):
        self.doc_id = doc_id
        self.date = date
        self.type = type
        self.type_id = type_id
        self.mime = mime
        self.mime_id = mime_id
        self.url = url
        self.state_link = state_link
        self.text_size = text_size
        self.text_hash = text_hash
        self.alt_bill_text = alt_bill_text
        self.alt_mime = alt_mime
        self.alt_mime_id = alt_mime_id
        self.alt_state_link = alt_state_link

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Text':
        return cls(
            doc_id=data.get('doc_id'),
            date=data.get('date'),
            type=TextType(data.get('type_id')),
            type_id=data.get('type_id'),
            mime=MimeType(data.get('mime_id')),
            mime_id=data.get('mime_id'),
            url=data.get('url'),
            state_link=data.get('state_link'),
            text_size=data.get('text_size'),
            text_hash=data.get('text_hash'),
            alt_bill_text=data.get('alt_bill_text'),
            alt_mime=data.get('alt_mime'),
            alt_mime_id=data.get('alt_mime_id'),
            alt_state_link=data.get('alt_state_link')
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'doc_id': self.doc_id,
            'date': self.date,
            'type': self.type.value,
            'type_id': self.type_id,
            'mime': self.mime.value,
            'mime_id': self.mime_id,
            'url': self.url,
            'state_link': self.state_link,
            'text_size': self.text_size,
            'text_hash': self.text_hash,
            'alt_bill_text': self.alt_bill_text,
            'alt_mime': self.alt_mime,
            'alt_mime_id': self.alt_mime_id,
            'alt_state_link': self.alt_state_link
        }