import json

import pika
from pika import ConnectionParameters
from pika.exchange_type import ExchangeType


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

    def publish(self, queue_name: str, payload: dict):
        '''def to publish logs in log sender channel'''
        print(f'message {payload} sent to {queue_name}', flush=True)
        self.channel.basic_publish('', routing_key=queue_name,
                                   body=json.dumps(payload))


publisher = Publisher()
