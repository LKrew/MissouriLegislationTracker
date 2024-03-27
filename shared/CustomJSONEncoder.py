import datetime
from typing import Any
from shared.bill import Sponsor
import json

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Sponsor):
            return {
                'name': o.name,
                'partyAffiliation': o.party_affiliation,
                'district': o.district
            }
        elif isinstance(o, datetime.datetime):
            return o.isoformat()
        return super().default(o)
 