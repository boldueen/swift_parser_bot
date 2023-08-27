from loguru import logger
from rabbit_publisher import publisher


class Logger():
    @staticmethod
    def info(message: str):
        logger.info(message)
        payload = {
            'level': 'INFO',
            'message': message
        }
        publisher.publish('log_sender', payload)

    @staticmethod
    def error(message: str):
        logger.error(message)
        payload = {
            'level': 'ERROR',
            'message': message
        }
        publisher.publish('log_sender', payload)


__all__ = ['Logger']
