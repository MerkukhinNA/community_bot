import pika, aio_pika, os, json, asyncio
from pika import BlockingConnection
from aio_pika import Message, DeliveryMode
from aio_pika.patterns import RPC

from utils.logger import logger


class RabbitMQManager:
    
    def __init__(self):
        with self.create_connection() as connection:
            with connection.channel() as channel:
                channel.queue_declare(queue='user_check', durable=True)
                channel.queue_declare(queue='user_create', durable=True)

    def publish(self, routing_key: str, body: dict[str, str], exchange: str = ''):
        body['for'] = 'internal'

        with self.create_connection() as connection:
            with connection.channel() as channel:
                channel.basic_publish(
                    exchange=exchange,
                    routing_key=routing_key,
                    body=json.dumps(body)
                )
            
    def create_connection(self) -> BlockingConnection:
        return pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.environ['RABBITMQ_HOST_EXTERNAL'],
                port=os.environ['RABBITMQ_PORT_EXTERNAL'],
                credentials=pika.PlainCredentials(
                    username=os.environ['RABBITMQ_USER_EXTERNAL'],
                    password=os.environ['RABBITMQ_PASSWORD_EXTERNAL']
                ),
                heartbeat=600
            )
        )

    
rabbitmq = RabbitMQManager()