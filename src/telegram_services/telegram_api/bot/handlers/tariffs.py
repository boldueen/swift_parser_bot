import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile

from bot.container import publisher


logger = logging.getLogger(__name__)
router: Router = Router()


@router.message(Command('yandex_b2b'))
async def send_yandex_b2b(message: Message):
    await message.reply('wait a second...')
    payload = {
        'filetype': 'yandex_b2b',
        'id_to_send_file_to': message.from_user.id
    }

    await publisher.publish('file_sender', payload)


@router.message(Command('yandex_b2c'))
async def send_yandex_b2c(message: Message):
    await message.reply('wait a second...')
    payload = {
        'filetype': 'yandex_b2c',
        'id_to_send_file_to': message.from_user.id
    }

    await publisher.publish('file_sender', payload)


@router.message(Command('citymobil'))
async def send_citymobil(message: Message):
    await message.reply('wait a second...')
    payload = {
        'filetype': 'citymobil',
        'id_to_send_file_to': message.from_user.id
    }

    await publisher.publish('file_sender', payload)
