import aio_pika, os, ast, asyncio

from utils.logger import logger


class RabbitMQManager:

    def __init__(self):
        pass
    
    async def publish(self, queue_name: str, body: dict [str, str]) -> dict[str, str]:
        connection = await aio_pika.connect_robust(
            host=os.environ['RABBITMQ_HOST_EXTERNAL'],
            port=int(os.environ['RABBITMQ_PORT_EXTERNAL']),
            login=os.environ['RABBITMQ_USER_EXTERNAL'],
            password=os.environ['RABBITMQ_PASSWORD_EXTERNAL'],
        )

        async with connection:
            channel = await connection.channel()
            callback_queue = await channel.get_queue(os.environ['RABBITMQ_REPLY'])

            # Создаем asyncio.Queue для ответа
            rq = asyncio.Queue(maxsize=1)

            # Сначала подписываемся
            consumer_tag = await callback_queue.consume(
                callback=rq.put,  # помещаем сообщение в asyncio.Queue
                no_ack=True,  # еще один важный нюанс
            )

            # Потом публикуем
            await channel.default_exchange.publish(
                message=aio_pika.Message(
                    body=str(body).encode(),
                    reply_to=os.environ['RABBITMQ_REPLY']  # Указываем очередь для ответа
                ),
                routing_key=queue_name
            )

            response = await rq.get()  # Получаем ответ из asyncio.Queue
            await callback_queue.cancel(consumer_tag)  # освобождаем RABBITMQ_REPLY
            return ast.literal_eval(response.body.decode())  # str to dict, изначально приходят вообще байты
    
rabbitmq = RabbitMQManager()