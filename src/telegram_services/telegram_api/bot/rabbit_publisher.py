import json

import pika
import logging
from pika import URLParameters

from pika.exchange_type import ExchangeType


logger = logging.getLogger(__name__)


class Publisher():
    def __init__(self) -> None:
        connection_string = URLParameters(
            'amqp://guest:guest@rabbitmq:5672/%2F')
        print('trying to connect to rabbit...!', flush=True)

        self.connection = pika.BlockingConnection(connection_string)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="file_sender",
                                      exchange_type=ExchangeType.direct,
                                      passive=False,
                                      durable=True,
                                      auto_delete=False)

    async def publish(self, queue_name: str, payload: dict):
        print(f'message {payload} sent to {queue_name}', flush=True)
        self.channel.basic_publish('telegram_services', routing_key=queue_name,
                                   body=json.dumps(payload))
