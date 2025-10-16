import pika, aio_pika, os, json, asyncio
from functools import partial
import aio_pika

from utils.logger import logger
from rabbitmq.consumers.user import check_user, create_user, create_visit, read_user_visits, read_user_events,\
    read_user_feedbacks
from rabbitmq.consumers.community import read_communityes, delete_community, update_community, create_community
from rabbitmq.consumers.visit import read_visits, delete_visit
from rabbitmq.consumers.event import create_event, read_events, delete_event
from rabbitmq.consumers.feedback import create_feedback, read_feedback, create_asnwer


class RabbitMQManager:
    
    def __init__(self):
        pass
        
    async def run(self):
        # Запускаем все consumers параллельно
        await asyncio.gather(
            self.run_consumer('check_user', check_user),
            self.run_consumer('create_user', create_user),
            self.run_consumer('create_visit', create_visit),
            self.run_consumer('read_user_visits', read_user_visits),
            self.run_consumer('read_user_events', read_user_events),
            self.run_consumer('read_user_feedbacks', read_user_feedbacks),
            self.run_consumer('create_community', create_community),
            self.run_consumer('read_communityes', read_communityes),
            self.run_consumer('update_community', update_community),
            self.run_consumer('delete_community', delete_community),
            self.run_consumer('read_visits', read_visits),
            self.run_consumer('delete_visit', delete_visit),
            self.run_consumer('create_event', create_event),
            self.run_consumer('read_events', read_events),
            self.run_consumer('delete_event', delete_event),
            self.run_consumer('create_feedback', create_feedback),
            self.run_consumer('read_feedback', read_feedback),
            self.run_consumer('create_asnwer', create_asnwer),
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