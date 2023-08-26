import json
import os


class Settings():
    TG_BOT_TOKEN = os.environ.get('TG_BOT_TOKEN')
    TG_ADMIN = os.environ.get('TG_ADMIN')


settings = Settings()
