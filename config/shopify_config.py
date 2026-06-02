from env import get_settings


class ShopifyConfig:
    def __init__(self):
        settings = get_settings()

        self.WEBHOOK_SECRET = settings.SHOPIFY_WEBHOOK_SECRET
        self.ACCESS_TOKEN = settings.SHOPIFY_ACCESS_TOKEN
        self.BASE_URL = settings.SHOPIFY_BASE_URL


def get_shopify_config():
    return ShopifyConfig()
