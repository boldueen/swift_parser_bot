import logging
from pika.exchange_type import ExchangeType
from pika import ConnectionParameters
import pika

from utils import save_filepath_to_redis
from yandex_b2c_parser import parse_links
from savers import save_to_excel


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
            exchange='parsers',
            exchange_type=ExchangeType.fanout,
            passive=False,
            durable=True,
            auto_delete=False)
        self.channel.queue_declare(queue='yandex_b2c_parser', auto_delete=True)
        self.channel.queue_bind(
            queue='yandex_b2c_parser', exchange='parsers', routing_key='standard_key')
        self.channel.basic_qos(prefetch_count=1)

        self.channel.basic_consume('yandex_b2c_parser', auto_ack=True,
                                   on_message_callback=self.callback)

    def callback(self, channel, method, properties, body):
        print('starting to parse citymobil rates', flush=True)
        rates = parse_links()
        yandex_b2c_filepath = save_to_excel(rates)
        save_filepath_to_redis(yandex_b2c_filepath)

    def start_consuming(self):
        print('start consuming messages...', flush=True)
        self.channel.start_consuming()
