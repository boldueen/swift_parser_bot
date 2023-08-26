import logging
from pika.exchange_type import ExchangeType
from pika import ConnectionParameters
import pika

import json
from utils import is_body_correct, get_log_body, send_log

logger = logging.getLogger(__name__)


class Consumer():
    def __init__(self) -> None:
        connection_string = ConnectionParameters(
            host='rabbitmq',
            heartbeat=600,
            blocked_connection_timeout=300
        )
        print('trying to connect to rabbit...!', flush=True)

        self.connection = pika.BlockingConnection(connection_string, )

        print('connected to rabbit!', flush=True)

        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange='telegram_services',
            exchange_type=ExchangeType.direct,
            passive=False,
            durable=True,
            auto_delete=False)
        self.channel.queue_declare(queue='log_sender', auto_delete=True)
        self.channel.queue_bind(
            queue='log_sender', exchange='telegram_services', routing_key='')
        self.channel.basic_qos(prefetch_count=1)

        self.channel.basic_consume('log_sender', auto_ack=True,
                                   on_message_callback=self.callback)

    def callback(self, channel, method, properties, body):
        print('recieved message')
        try:
            parsed_body: dict = json.loads(body)
            if not is_body_correct(parsed_body):
                print('body is not corret', flush=True)
                return

            log_body = get_log_body(body=parsed_body)

            send_log(log_body)
        except Exception as exc:
            print('error occired', exc.args, flush=True)

    def start_consuming(self):
        print('start consuming messages...', flush=True)
        self.channel.start_consuming()
