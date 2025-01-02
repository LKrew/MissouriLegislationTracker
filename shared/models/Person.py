from typing import Any, Dict, Optional
from .Enums import PoliticalParty, Role

class Person:
    def __init__(self, people_id: int, person_hash: str, state_id: int, party_id: int, party: PoliticalParty, role_id: int, role: Role, name: str, first_name: str, middle_name: Optional[str], last_name: str, suffix: Optional[str], district: str, ftm_eid: int, votesmart_id: int, opensecrets_id: Optional[str], knowwho_pid: int, ballotpedia: str, committee_sponsor: int, committee_id: Optional[int]):
        self.people_id = people_id
        self.person_hash = person_hash
        self.state_id = state_id
        self.party_id = party_id
        self.party = party
        self.role_id = role_id
        self.role = role
        self.name = name
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.suffix = suffix
        self.district = district
        self.ftm_eid = ftm_eid
        self.votesmart_id = votesmart_id
        self.opensecrets_id = opensecrets_id
        self.knowwho_pid = knowwho_pid
        self.ballotpedia = ballotpedia
        self.committee_sponsor = committee_sponsor
        self.committee_id = committee_id

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Person':
        data['party'] = PoliticalParty(int(data['party_id'])).name
        data['role'] = Role(int(data['role_id'])).name
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'people_id': self.people_id,
            'person_hash': self.person_hash,
            'state_id': self.state_id,
            'party_id': self.party_id,
            'party': self.party,
            'role_id': self.role_id,
            'role': self.role,
            'name': self.name,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'suffix': self.suffix,
            'district': self.district,
            'ftm_eid': self.ftm_eid,
            'votesmart_id': self.votesmart_id,
            'opensecrets_id': self.opensecrets_id,
            'knowwho_pid': self.knowwho_pid,
            'ballotpedia': self.ballotpedia,
            'committee_sponsor': self.committee_sponsor,
            'committee_id': self.committee_id
        }