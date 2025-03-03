from typing import Any, Dict, Optional
from .Enums import MimeType
import logging

class Amendment:
    def __init__(self, 
                 amendment_id: int,
                 chamber: str,
                 chamber_id: int,
                 adopted: bool,
                 date: str,
                 title: str,
                 description: str,
                 mime: str,
                 mime_id: int,
                 url: str,
                 state_link: str,
                 amendment_size: int,
                 amendment_hash: str,
                 alt_amendment: Optional[int] = None,
                 alt_mime: Optional[str] = None,
                 alt_mime_id: Optional[int] = None,
                 alt_state_link: Optional[str] = None,
                 alt_amendment_size: Optional[int] = None,
                 alt_amendment_hash: Optional[str] = None):
        self.amendment_id = amendment_id
        self.chamber = chamber
        self.chamber_id = chamber_id
        self.adopted = bool(adopted)  # Convert from 0/1 to bool
        self.date = date
        self.title = title
        self.description = description
        self.mime = MimeType(mime_id)  # Convert using ID instead of string
        self.mime_id = mime_id
        self.url = url
        self.state_link = state_link
        self.amendment_size = amendment_size
        self.amendment_hash = amendment_hash
        self.alt_amendment = alt_amendment
        self.alt_mime = alt_mime
        self.alt_mime_id = alt_mime_id
        self.alt_state_link = alt_state_link
        self.alt_amendment_size = alt_amendment_size
        self.alt_amendment_hash = alt_amendment_hash

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Amendment':
        try:
            return cls(
                amendment_id=data['amendment_id'],
                chamber=data['chamber'],
                chamber_id=data['chamber_id'],
                adopted=data['adopted'],
                date=data['date'],
                title=data['title'],
                description=data['description'],
                mime=data['mime'],
                mime_id=data['mime_id'],
                url=data['url'],
                state_link=data['state_link'],
                amendment_size=data['amendment_size'],
                amendment_hash=data['amendment_hash'],
                alt_amendment=data.get('alt_amendment'),
                alt_mime=data.get('alt_mime'),
                alt_mime_id=data.get('alt_mime_id'),
                alt_state_link=data.get('alt_state_link'),
                alt_amendment_size=data.get('alt_amendment_size'),
                alt_amendment_hash=data.get('alt_amendment_hash')
            )
        except Exception as e:
            logging.error(f"Error creating Amendment from JSON: {str(e)}")
            raise

    def to_dict(self) -> Dict[str, Any]:
        return {
            'amendment_id': self.amendment_id,
            'chamber': self.chamber,
            'chamber_id': self.chamber_id,
            'adopted': self.adopted,
            'date': self.date,
            'title': self.title,
            'description': self.description,
            'mime': self.mime.value,
            'mime_id': self.mime_id,
            'url': self.url,
            'state_link': self.state_link,
            'amendment_size': self.amendment_size,
            'amendment_hash': self.amendment_hash,
            'alt_amendment': self.alt_amendment,
            'alt_mime': self.alt_mime,
            'alt_mime_id': self.alt_mime_id,
            'alt_state_link': self.alt_state_link,
            'alt_amendment_size': self.alt_amendment_size,
            'alt_amendment_hash': self.alt_amendment_hash
        }