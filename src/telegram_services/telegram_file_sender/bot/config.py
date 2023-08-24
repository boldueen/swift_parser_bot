import os


class Settings():
    TG_BOT_TOKEN = os.environ.get('TG_BOT_TOKEN')


settings = Settings()
