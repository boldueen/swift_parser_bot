import requests
from aiogram import Bot, Dispatcher
from .config import settings


# document = FSInputFile('otchet.txt')
# await bot.send_document(chatid, document)

bot: Bot = Bot(token=settings.TG_BOT_TOKEN, parse_mode="HTML")
dp: Dispatcher = Dispatcher()


def send_file_to_user_by_id(user_id: int, filepath_to_send: str):
    print(f'sending {filepath_to_send} to {user_id}', flush=True)
    # TODO: tun request in threadpool

    document = open(filepath_to_send, "rb")

    url = f"https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendDocument"
    response = requests.post(url,
                             data={'chat_id': user_id},
                             files={'document': document}
                             )

    print(response.status_code, response.json(), flush=True)
