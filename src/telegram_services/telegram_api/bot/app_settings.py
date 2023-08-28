import os


class Settings():
    TG_BOT_TOKEN: str = os.environ.get('TG_BOT_TOKEN')
    TG_ADMIN: int = int(os.environ.get('TG_ADMIN'))
