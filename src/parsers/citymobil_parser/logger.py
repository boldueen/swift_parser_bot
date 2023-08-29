import json
from loguru import logger as loglog
from rabbit_publisher import publisher


class Logger():

    def info(self, message: str):
        loglog.info(message)

        payload = {
            "message": message,
        }
        print('sending log to rabbit', flush=True)
        publisher.publish('log_sender', payload=payload)

    def warn(self, message: str):
        loglog.warning(message)

    def error(self, message: str):
        loglog.error(message)

        payload = {
            'message': message,
            'level': 'ERROR'

        }
        publisher.publish('log_sender', payload=payload)


log = Logger()


__all__ = ['log']
