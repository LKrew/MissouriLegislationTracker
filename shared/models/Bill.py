from typing import Any, Dict, List, Optional
from .Referral import Referral
from .History import History
from .Sponsor import Sponsor
from .Sast import Sast
from .Subject import Subject
from .Text import Text
from .Vote import Vote
from .Amendment import Amendment
from .Supplement import Supplement
from .CalendarEvent import CalendarEvent
from .Enums import BillType
from .Session import Session

class Bill:
    def __init__(self, bill_id: int, number: str, change_hash: str, url: str, status_date: str, status: int, last_action_date: str, last_action: str, title: str, description: str, session: Optional[Session] = None, state_link: Optional[str] = None, completed: Optional[int] = None, progress: Optional[List[dict]] = None, state: Optional[str] = None, state_id: Optional[int] = None, bill_number: Optional[str] = None, bill_type: BillType = None, bill_type_id: Optional[int] = None, body: Optional[str] = None, body_id: Optional[int] = None, current_body: Optional[str] = None, current_body_id: Optional[int] = None, pending_committee_id: Optional[int] = None, committee: Optional[List[dict]] = None, referrals: Optional[List[Referral]] = None, history: Optional[List[History]] = None, sponsors: Optional[List[Sponsor]] = None, sasts: Optional[List[Sast]] = None, subjects: Optional[List[Subject]] = None, texts: Optional[List[Text]] = None, votes: Optional[List[Vote]] = None, amendments: Optional[List[Amendment]] = None, supplements: Optional[List[Supplement]] = None, calendar: Optional[List[CalendarEvent]] = None):
        self.bill_id = bill_id
        self.number = number
        self.change_hash = change_hash
        self.url = url
        self.status_date = status_date
        self.status = status
        self.last_action_date = last_action_date
        self.last_action = last_action
        self.title = title
        self.description = description
        self.session = session
        self.state_link = state_link
        self.completed = completed
        self.progress = progress or []
        self.state = state
        self.state_id = state_id
        self.bill_number = bill_number
        self.bill_type = bill_type
        self.bill_type_id = bill_type_id
        self.body = body
        self.body_id = body_id
        self.current_body = current_body
        self.current_body_id = current_body_id
        self.pending_committee_id = pending_committee_id
        self.committee = committee or []
        self.referrals = referrals or []
        self.history = history or []
        self.sponsors = sponsors or []
        self.sasts = sasts or []
        self.subjects = subjects or []
        self.texts = texts or []
        self.votes = votes or []
        self.amendments = amendments or []
        self.supplements = supplements or []
        self.calendar = calendar or []

    @classmethod
    def from_json(cls, data: dict) -> 'Bill':
        return cls(
            bill_id=data.get('bill_id'),
            number=data.get('number'),
            change_hash=data.get('change_hash'),
            url=data.get('url'),
            status_date=data.get('status_date'),
            status=data.get('status'),
            last_action_date=data.get('last_action_date'),
            last_action=data.get('last_action'),
            title=data.get('title'),
            description=data.get('description'),
            session=Session.from_json(data['session']) if 'session' in data else None,
            state_link=data.get('state_link'),
            completed=data.get('completed'),
            progress=data.get('progress', []),
            state=data.get('state'),
            state_id=data.get('state_id'),
            bill_number=data.get('bill_number'),
            bill_type=BillType(int(data.get('bill_type_id'))) if 'bill_type_id' in data else None,
            bill_type_id=data.get('bill_type_id'),
            body=data.get('body'),
            body_id=data.get('body_id'),
            current_body=data.get('current_body'),
            current_body_id=data.get('current_body_id'),
            pending_committee_id=data.get('pending_committee_id'),
            committee=data.get('committee', []),
            referrals=[Referral.from_json(referral) for referral in data.get('referrals', [])] if 'referrals' in data else [],
            history=[History.from_json(history) for history in data.get('history', [])] if 'history' in data else [],
            sponsors=[Sponsor.from_json(sponsor) for sponsor in data.get('sponsors', [])] if 'sponsors' in data else [],
            sasts=[Sast.from_json(sast) for sast in data.get('sasts', [])] if 'sasts' in data else [],
            subjects=[Subject.from_json(subject) for subject in data.get('subjects', [])] if 'subjects' in data else [],
            texts=[Text.from_json(text) for text in data.get('texts', [])] if 'texts' in data else [],
            votes=[Vote.from_json(vote) for vote in data.get('votes', [])] if 'votes' in data else [],
            amendments=[Amendment.from_json(amendment) for amendment in data.get('amendments', [])] if 'amendments' in data else [],
            supplements=[Supplement.from_json(supplement) for supplement in data.get('supplements', [])] if 'supplements' in data else [],
            calendar=[CalendarEvent.from_json(event) for event in data.get('calendar', [])] if 'calendar' in data else []
        )

    def update_from_json(self, data: dict) -> None:
        self.bill_id = data.get('bill_id', self.bill_id)
        self.number = data.get('number', self.number)
        self.change_hash = data.get('change_hash', self.change_hash)
        self.url = data.get('url', self.url)
        self.status_date = data.get('status_date', self.status_date)
        self.status = data.get('status', self.status)
        self.last_action_date = data.get('last_action_date', self.last_action_date)
        self.last_action = data.get('last_action', self.last_action)
        self.title = data.get('title', self.title)
        self.description = data.get('description', self.description)
        self.session = Session.from_json(data['session']) if 'session' in data else self.session
        self.state_link = data.get('state_link', self.state_link)
        self.completed = data.get('completed', self.completed)
        self.progress = data.get('progress', self.progress)
        self.state = data.get('state', self.state)
        self.state_id = data.get('state_id', self.state_id)
        self.bill_number = data.get('bill_number', self.bill_number)
        self.bill_type = BillType(int(data.get('bill_type_id'))) if 'bill_type_id' in data else self.bill_type
        self.bill_type_id = data.get('bill_type_id', self.bill_type_id)
        self.body = data.get('body', self.body)
        self.body_id = data.get('body_id', self.body_id)
        self.current_body = data.get('current_body', self.current_body)
        self.current_body_id = data.get('current_body_id', self.current_body_id)
        self.pending_committee_id = data.get('pending_committee_id', self.pending_committee_id)
        self.committee = data.get('committee', self.committee)
        self.referrals = [Referral.from_json(referral) for referral in data.get('referrals', [])] if 'referrals' in data else self.referrals
        self.history = [History.from_json(history) for history in data.get('history', [])] if 'history' in data else self.history
        self.sponsors = [Sponsor.from_json(sponsor) for sponsor in data.get('sponsors', [])] if 'sponsors' in data else self.sponsors
        self.sasts = [Sast.from_json(sast) for sast in data.get('sasts', [])] if 'sasts' in data else self.sasts
        self.subjects = [Subject.from_json(subject) for subject in data.get('subjects', [])] if 'subjects' in data else self.subjects
        self.texts = [Text.from_json(text) for text in data.get('texts', [])] if 'texts' in data else self.texts
        self.votes = [Vote.from_json(vote) for vote in data.get('votes', [])] if 'votes' in data else self.votes
        self.amendments = [Amendment.from_json(amendment) for amendment in data.get('amendments', [])] if 'amendments' in data else self.amendments
        self.supplements = [Supplement.from_json(supplement) for supplement in data.get('supplements', [])] if 'supplements' in data else self.supplements
        self.calendar = [CalendarEvent.from_json(event) for event in data.get('calendar', [])] if 'calendar' in data else self.calendar

    def to_dict(self) -> dict:
        return {
            'bill_id': self.bill_id,
            'number': self.number,
            'change_hash': self.change_hash,
            'url': self.url,
            'status_date': self.status_date,
            'status': self.status,
            'last_action_date': self.last_action_date,
            'last_action': self.last_action,
            'title': self.title,
            'description': self.description,
            'session': self.session.to_dict() if self.session else None,
            'state_link': self.state_link,
            'completed': self.completed,
            'progress': self.progress,
            'state': self.state,
            'state_id': self.state_id,
            'bill_number': self.bill_number,
            'bill_type': self.bill_type.value if self.bill_type else None,
            'bill_type_id': self.bill_type_id,
            'body': self.body,
            'body_id': self.body_id,
            'current_body': self.current_body,
            'current_body_id': self.current_body_id,
            'pending_committee_id': self.pending_committee_id,
            'committee': self.committee,
            'referrals': [referral.to_dict() for referral in self.referrals],
            'history': [history.to_dict() for history in self.history],
            'sponsors': [sponsor.to_dict() for sponsor in self.sponsors],
            'sasts': [sast.to_dict() for sast in self.sasts],
            'subjects': [subject.to_dict() for subject in self.subjects],
            'texts': [text.to_dict() for text in self.texts],
            'votes': [vote.to_dict() for vote in self.votes],
            'amendments': [amendment.to_dict() for amendment in self.amendments],
            'supplements': [supplement.to_dict() for supplement in self.supplements],
            'calendar': [event.to_dict() for event in self.calendar]
        }