import logging
import json
from pika.exchange_type import ExchangeType
from pika import ConnectionParameters
import pika
import asyncio
from .commands import send_file_to_user_by_id
from .utils import is_body_correct, get_filepath_by_filetype


from asgiref.sync import async_to_sync

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

        self.channel.queue_declare(queue='file_sender', auto_delete=True)
        self.channel.queue_bind(
            queue='file_sender', exchange='telegram_services')
        self.channel.basic_qos(prefetch_count=1)

        self.channel.basic_consume('file_sender', auto_ack=True,
                                   on_message_callback=self.callback)

    def callback(self, channel, method, properties, body):
        print('tg-file-sednder. [X] recieved data', body, flush=True)

        try:
            parsed_body: dict = json.loads(body)
            if not is_body_correct(parsed_body):
                return

            id_to_send_file_to = parsed_body.get('id_to_send_file_to')
            filetype = parsed_body.get('filetype')

            filepath_to_send = get_filepath_by_filetype(filetype=filetype)

            if filepath_to_send is None:
                # TODO: handle error
                print(f'no file for filetype {filetype}', flush=True)
                return

            send_file_to_user_by_id(
                user_id=id_to_send_file_to, filepath_to_send=filepath_to_send)

        except Exception as e:
            print(e, flush=True)
            print(f'error occured while sending file to user', flush=True)
            return

    def start_consuming(self):
        self.channel.start_consuming()
