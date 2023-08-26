import json
import logging

import pika
from pika import ConnectionParameters
from pika.exchange_type import ExchangeType


logger = logging.getLogger(__name__)


class Consumer():
    def __init__(self) -> None:
        connection_string = ConnectionParameters(
            host='rabbitmq',
            heartbeat=600,
            blocked_connection_timeout=300
        )


logger = logging.getLogger(__name__)


class Publisher():
    def __init__(self) -> None:
        connection_params = ConnectionParameters(
            host='rabbitmq',
            heartbeat=600,
            blocked_connection_timeout=300
        )

        self.connection = pika.BlockingConnection(connection_params)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="telegram_services",
                                      exchange_type=ExchangeType.direct,
                                      passive=False,
                                      durable=True,
                                      auto_delete=False)

    async def publish(self, queue_name: str, payload: dict):
        print(f'message {payload} sent to {queue_name}', flush=True)
        self.channel.basic_publish('telegram_services', routing_key=queue_name,
                                   body=json.dumps(payload))
