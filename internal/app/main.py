import aio_pika, asyncio, json, os

from db.db_manager import db
from utils.logger import logger
from rabbitmq.manager import rabbitmq
from rabbitmq.handler.user import check_user


async def main():
    rabbitmq.create_consumer_tasks(
        {
            'user_check': check_user,
        }
    )
    await asyncio.gather(*rabbitmq.consumer_tasks)  # Ждем завершения всех задач 

asyncio.run(main())