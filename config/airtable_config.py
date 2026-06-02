from env import get_settings

class AirtableConfig:
    def __init__(self):
        settings = get_settings()

        self.API_TOKEN = settings.AIRTABLE_API_TOKEN
        self.BASE_ID = settings.AIRTABLE_BASE_ID
        self.TABLE_NAME = settings.AIRTABLE_TABLE_NAME

def get_airtable_config():
    return AirtableConfig()