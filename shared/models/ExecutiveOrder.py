from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime, timezone

@dataclass
class ExecutiveOrder:
    citation: str
    document_number: str
    end_page: int
    html_url: str
    pdf_url: str
    type: str
    subtype: str
    publication_date: date
    signing_date: date
    start_page: int
    title: str
    disposition_notes: Optional[str]
    executive_order_number: str
    not_received_for_publication: Optional[str]
    full_text_xml_url: str
    body_html_url: str
    json_url: str
    posted: bool = False
    posted_date: Optional[str] = None

    def __post_init__(self):
        if self.posted_date is None:
            self.posted_date = datetime.now(timezone.utc).isoformat()

    @classmethod
    def from_json(cls, data: dict) -> 'ExecutiveOrder':
        return cls(
            citation=data.get('citation') or '',
            document_number=data.get('document_number') or '',
            end_page=int(data.get('end_page') or 0),
            html_url=data.get('html_url') or '',
            pdf_url=data.get('pdf_url') or '',
            type=data.get('type') or '',
            subtype=data.get('subtype') or '',
            publication_date=date.fromisoformat(data.get('publication_date') or '1970-01-01'),
            signing_date=date.fromisoformat(data.get('signing_date') or '1970-01-01'),
            start_page=int(data.get('start_page') or 0),
            title=data.get('title') or '',
            disposition_notes=data.get('disposition_notes'),
            executive_order_number=data.get('executive_order_number') or '',
            not_received_for_publication=data.get('not_received_for_publication'),
            full_text_xml_url=data.get('full_text_xml_url') or '',
            body_html_url=data.get('body_html_url') or '',
            json_url=data.get('json_url') or '',
            posted=data.get('posted', False),
            posted_date=data.get('posted_date')
        )

    def to_dict(self) -> dict:
        return {
            'citation': self.citation,
            'document_number': self.document_number,
            'end_page': self.end_page,
            'html_url': self.html_url,
            'pdf_url': self.pdf_url,
            'type': self.type,
            'subtype': self.subtype,
            'publication_date': self.publication_date.isoformat(),
            'signing_date': self.signing_date.isoformat(),
            'start_page': self.start_page,
            'title': self.title,
            'disposition_notes': self.disposition_notes,
            'executive_order_number': self.executive_order_number,
            'not_received_for_publication': self.not_received_for_publication,
            'full_text_xml_url': self.full_text_xml_url,
            'body_html_url': self.body_html_url,
            'json_url': self.json_url,
            'posted': self.posted,
            'posted_date': self.posted_date
        }
