import asyncio
import logging
import sys

from bot.rabbit_consumer import Consumer

consumer = Consumer()


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    consumer.start_consuming()


if __name__ == "__main__":
    try:

        print(sys.path)
        # current_dir = 4
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
