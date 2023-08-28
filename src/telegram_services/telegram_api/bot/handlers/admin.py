import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile

from bot.filters import AdminFilter
from bot.container import publisher
from bot.container import settings


logger = logging.getLogger(__name__)
router = Router()
router.message.filter(
    AdminFilter(admins=settings.TG_ADMIN)
)


@router.message(Command('update'))
async def send_yandex_b2b(message: Message):
    await message.reply('good morning my creator')
