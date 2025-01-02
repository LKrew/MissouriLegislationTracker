from typing import Any, Dict, List, Optional
from .Enums import VoteType

class VoteDetail:
    def __init__(self, people_id: int, vote_id: int, vote_text: VoteType):
        self.people_id = people_id
        self.vote_id = vote_id
        self.vote_text = vote_text

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'VoteDetail':
        data['vote_text'] = VoteType(data['vote_text'])
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'people_id': self.people_id,
            'vote_id': self.vote_id,
            'vote_text': self.vote_text.value
        }

class Vote:
    def __init__(self, roll_call_id: int, bill_id: int, date: str, desc: str, yea: int, nay: int, nv: int, absent: int, total: int, passed: bool, chamber: str, chamber_id: int, votes: Optional[List[VoteDetail]] = None, url: str = '', state_link: str = ''):
        self.roll_call_id = roll_call_id
        self.bill_id = bill_id
        self.date = date
        self.desc = desc
        self.yea = yea
        self.nay = nay
        self.nv = nv
        self.absent = absent
        self.total = total
        self.passed = passed
        self.chamber = chamber
        self.chamber_id = chamber_id
        self.votes = votes or []
        self.url = url
        self.state_link = state_link

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Vote':
        votes = [VoteDetail.from_json(vote) for vote in data.get('votes', [])]
        return cls(
            roll_call_id=data.get('roll_call_id'),
            bill_id=data.get('bill_id'),
            date=data.get('date'),
            desc=data.get('desc'),
            yea=data.get('yea'),
            nay=data.get('nay'),
            nv=data.get('nv'),
            absent=data.get('absent'),
            total=data.get('total'),
            passed=data.get('passed'),
            chamber=data.get('chamber'),
            chamber_id=data.get('chamber_id'),
            votes=votes,
            url=data.get('url', ''),
            state_link=data.get('state_link', '')
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'roll_call_id': self.roll_call_id,
            'bill_id': self.bill_id,
            'date': self.date,
            'desc': self.desc,
            'yea': self.yea,
            'nay': self.nay,
            'nv': self.nv,
            'absent': self.absent,
            'total': self.total,
            'passed': self.passed,
            'chamber': self.chamber,
            'chamber_id': self.chamber_id,
            'votes': [vote.to_dict() for vote in self.votes],
            'url': self.url,
            'state_link': self.state_link
        }