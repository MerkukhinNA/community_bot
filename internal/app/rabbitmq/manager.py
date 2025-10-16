import pika, aio_pika, os, json, asyncio
from pika import BlockingConnection

from utils.logger import logger


class RabbitMQManager:
    
    def __init__(self):
        self.consumer_tasks = []
    
        with self.create_connection() as connection:
            with connection.channel() as channel:
                channel.queue_declare(queue='user_check', durable=True)
                channel.queue_declare(queue='user_create', durable=True)

    def publish(self, routing_key: str, body: dict[str, str], exchange: str = ''):
        body['for'] = 'external'
        
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
                host=os.environ['RABBITMQ_HOST_INTERNAL'],
                port=os.environ['RABBITMQ_PORT_INTERNAL'],
                credentials=pika.PlainCredentials(
                    username=os.environ['RABBITMQ_USER_INTERNAL'],
                    password=os.environ['RABBITMQ_PASSWORD_INTERNAL']
                ),
                heartbeat=600
            )
        )
    
    async def consumer_task(self, queue: str, handler: dict):
        connection = await aio_pika.connect_robust(
            host=os.environ['RABBITMQ_HOST_INTERNAL'],
            port=int(os.environ['RABBITMQ_PORT_INTERNAL']),
            login=os.environ['RABBITMQ_USER_INTERNAL'],
            password=os.environ['RABBITMQ_PASSWORD_INTERNAL'],
        )
        
        async def callback(message: aio_pika.IncomingMessage):
            body = json.loads(message.body.decode())

            try:
                if body['for'] != 'internal':
                    logger.info(f"\nQueue: {queue} | Body: {body} - Сообщение не обработано\n")
                    # await message.reject(requeue=False)  # Удалить сообщение
                    return
                
                await handler(body)  # Бизнес-логика
                await message.ack()  # Сообщение обратотано успешно - удалить
                logger.info(f"\nQueue: {queue} | Body: {body} - Сообщение успешно обработано\n")
                
            except Exception as e:
                # await message.reject(requeue=False)  # Удалить сообщение
                logger.info(f"\nQueue: {queue} | Body: {body} - Ошибка обработки сообщения -> '{e}'\n")
        
        async with connection:
            async with connection.channel() as channel:
                queue = await channel.get_queue(queue)
                
                await queue.consume(callback)
                await asyncio.Future()  # Бесконечное ожидание

    def create_consumer_tasks(self, queues: dict):
        # Запускаем все потребители в отдельных задачах
        for queue, handler in queues.items():
            task = asyncio.create_task(self.consumer_task(queue, handler))
            self.consumer_tasks.append(task)

        
rabbitmq = RabbitMQManager()