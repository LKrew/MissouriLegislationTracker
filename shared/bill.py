
class Bill:
    def __init__(self, bill_id, number, change_hash, url, status_date,
                 status, last_action_date, last_action, title, description,
                 sponsors, text, state_link):
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
        self.sponsors = sponsors
        self.text = text
        self.state_link = state_link
        
    @classmethod
    def from_json(cls, json_data):
        bill = cls.__new__(cls)
        bill.bill_id = json_data['bill_id']
        bill.number = json_data['number']
        bill.change_hash = json_data['change_hash']
        bill.url = json_data['url']
        bill.status_date = json_data['status_date']
        bill.status = json_data['status']
        bill.last_action_date = json_data['last_action_date']
        bill.last_action = json_data['last_action']
        bill.title = json_data['title']
        bill.description = json_data['description']
        bill.last_action = json_data['last_action']
        bill.last_action_date = json_data['last_action_date']
        return bill

        