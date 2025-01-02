from typing import Any, Dict, Optional
from .Person import Person

class Sponsor:
    def __init__(self, person: Person, sponsor_type_id: int, sponsor_order: int, committee_sponsor: Optional[int], committee_id: Optional[int]):
        self.person = person
        self.sponsor_type_id = sponsor_type_id
        self.sponsor_order = sponsor_order
        self.committee_sponsor = committee_sponsor
        self.committee_id = committee_id

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Sponsor':
        person_data = data.get('person', {})
        if not person_data:
            person_data = {key: data[key] for key in Person.__init__.__annotations__.keys() if key in data}
        person = Person.from_json(person_data)
        return cls(
            person=person,
            sponsor_type_id=data.get('sponsor_type_id'),
            sponsor_order=data.get('sponsor_order'),
            committee_sponsor=data.get('committee_sponsor'),
            committee_id=data.get('committee_id')
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'person': self.person.to_dict(),
            'sponsor_type_id': self.sponsor_type_id,
            'sponsor_order': self.sponsor_order,
            'committee_sponsor': self.committee_sponsor,
            'committee_id': self.committee_id
        }