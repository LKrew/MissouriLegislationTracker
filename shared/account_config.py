import os

class AccountConfig:
    def __init__(self):
        self.legiscan_api_key = os.getenv('LEGISCAN_API_KEY')
        self.db_name = os.getenv('COSMOS_DATABASE')
        self.legiscan_base_url = os.getenv('LEGISCAN_BASE_URL')
        self.legiscan_session_uri = os.getenv('LEGISCAN_SESSION_URI')
        self.legiscan_bill_uri = os.getenv('LEGISCAN_BILL_URI')
        self.legiscan_masterlist_uri = os.getenv('LEGISCAN_MASTERLIST_URI')
        
    def __repr__(self):
        return (f"AccountConfig(db_name={self.db_name}, container_name={self.container_name})")


class USAccountConfig(AccountConfig):
    def __init__(self):
        super().__init__()
        self.code = "US"
        
        #BSKY
        self.bsky_user = os.getenv('US_BSKY_USER')
        self.bsky_password = os.getenv('US_BSKY_PASSWORD')
        
        #Mastodon
        # self.mast_client_id = os.getenv('US_MAST_CLIENT_ID')
        # self.mast_client_secret = os.getenv('US_MAST_CLIENT_SECRET')
        # self.mast_access_token = os.getenv('US_MAST_ACCESS_TOKEN')
        
        # #Twitter
        # self.consumer_key = os.environ['US_TWITTER_CONSUMER_KEY']
        # self.consumer_secret = os.environ['US_TWITTER_CONSUMER_SECRET']
        # self.access_token = os.environ['US_TWITTER_ACCESS_TOKEN']
        # self.access_token_secret = os.environ['US_TWITTER_ACCESS_TOKEN_SECRET']
        
        self.container_name = os.getenv('US_COSMOS_CONTAINER')
        self.legiscan_state_id = os.getenv('LEGISCAN_STATE_ID_US')
        self.target_actions = ["Became Public Law",
                               "Signed by President",
                               "Introduced in House",
                               ]
        self.excluded_actions = ["Informal", "Calendar"]
        
    def __repr__(self):
        return (f"USAccountConfig(db_name={self.db_name}, container_name={self.container_name}, "
                f"bsky_account_name={self.bsky_user}, bsky_password=****, legiscan_api_key=****)")


class MOAccountConfig(AccountConfig):
    def __init__(self):
        super().__init__()
        
        self.code = "MO"
        #BSKY
        self.bsky_user = os.getenv('MO_BSKY_USER')
        self.bsky_password = os.getenv('MO_BSKY_PASSWORD')
        #Mastodon
        self.mast_client_id = os.getenv('MO_MAST_CLIENT_ID')
        self.mast_client_secret = os.getenv('MO_MAST_CLIENT_SECRET')
        self.mast_access_token = os.getenv('MO_MAST_ACCESS_TOKEN')
        #Twitter
        self.consumer_key = os.getenv('MO_TWITTER_CONSUMER_KEY')
        self.consumer_secret = os.getenv('MO_TWITTER_CONSUMER_SECRET')
        self.access_token = os.getenv('MO_TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('MO_TWITTER_ACCESS_TOKEN_SECRET')
        
        self.container_name = os.getenv('MO_COSMOS_CONTAINER')
        self.legiscan_state_id = os.getenv('LEGISCAN_STATE_ID_MO')
        self.target_actions = ["Prefiled",
                  "First Read",
                  "Third Read and Passed",
                  "Truly Agreed To and Finally Passed",
                  "Signed by Senate President Pro Tem",
                  "Signed by House Speaker",
                  "Delivered to Governor",
                  "Signed by Governor",
                  "Governor took no action",
                  "Delivered to Secretary of State",
                  "Withdrawn"]
        self.excluded_actions = ["Informal", "Calendar"]
        
    def __repr__(self):
        return (f"MOAccountConfig(db_name={self.db_name}, container_name={self.container_name}, "
                f"mo_specific_config={self.mo_specific_config})")
        
class EOAccountConfig(AccountConfig):
    def __init__(self):
        super().__init__()
        self.code = "EO"
        
        #BSKY
        self.bsky_user = os.getenv('EO_BSKY_USER')
        self.bsky_password = os.getenv('EO_BSKY_PASSWORD')
        
        self.container_name = os.getenv('EO_COSMOS_CONTAINER')
        self.api_url = os.getenv('EO_API_URL')
    
    def __repr__(self):
        return (f"MOAccountConfig(db_name={self.db_name}, container_name={self.container_name}, "
                f"mo_specific_config={self.mo_specific_config})")