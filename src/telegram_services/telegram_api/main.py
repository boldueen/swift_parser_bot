import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from bot.container import settings
from bot.handlers import tariffs


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")

    config = settings

    bot: Bot = Bot(token=config.TG_BOT_TOKEN, parse_mode="HTML")
    dp: Dispatcher = Dispatcher()

    dp.include_router(tariffs.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:

        print(sys.path)
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
