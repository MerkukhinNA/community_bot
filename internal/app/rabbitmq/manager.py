import pika, aio_pika, os, json, asyncio
from functools import partial
import aio_pika

from utils.logger import logger
from rabbitmq.consumers.user import check_user, create_user, create_visit, get_user_visits


class RabbitMQManager:
    
    def __init__(self):
        pass
        
    async def run(self):
        # Запускаем все consumers параллельно
        await asyncio.gather(
            self.run_consumer('check_user', check_user),
            self.run_consumer('create_user', create_user),
            self.run_consumer('create_visit', create_visit),
            self.run_consumer('get_user_visits', get_user_visits),
        )
        
    async def run_consumer(self, queue_name, consumer_func):
        connection = await aio_pika.connect_robust(
            host=os.environ['RABBITMQ_HOST_INTERNAL'],
            port=int(os.environ['RABBITMQ_PORT_INTERNAL']),
            login=os.environ['RABBITMQ_USER_INTERNAL'],
            password=os.environ['RABBITMQ_PASSWORD_INTERNAL'],
        )
        
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(queue_name)
            
            await queue.consume(partial(consumer_func, channel=channel))  # Через partial прокидываем в наш обработчик сам канал

            try:
                await asyncio.Future()
            except Exception:
                pass


rabbitmq = RabbitMQManager()