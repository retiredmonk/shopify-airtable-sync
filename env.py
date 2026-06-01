from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AIRTABLE_API_TOKEN : str
    AIRTABLE_BASE_ID : str
    AIRTABLE_TABLE_NAME : str

    SHOPIFY_WEBHOOK_SECRET : str
    SHOPIFY_ACCESS_TOKEN : str
    SHOPIFY_BASE_URL : str

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()