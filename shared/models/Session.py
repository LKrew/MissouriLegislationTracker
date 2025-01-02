from typing import Any, Dict

class Session:
    def __init__(self, session_id: int, state_id: int, year_start: int, year_end: int, prefile: int, sine_die: int, prior: int, special: int, session_name: str, session_title: str, session_tag: str):
        self.session_id = session_id
        self.state_id = state_id
        self.year_start = year_start
        self.year_end = year_end
        self.prefile = prefile
        self.sine_die = sine_die
        self.prior = prior
        self.special = special
        self.session_name = session_name
        self.session_title = session_title
        self.session_tag = session_tag

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Session':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__