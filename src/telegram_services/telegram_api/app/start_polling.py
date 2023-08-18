import time

import aiogram
import pika

from container import settings


if __name__ == '__main__':
    print('tg_bot starting...', flush=True)

    while True:
        print('tg_bot is listening for messages...', flush=True)

        time.sleep(1)
