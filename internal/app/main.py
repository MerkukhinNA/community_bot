import asyncio
from rabbitmq.manager import rabbitmq


asyncio.run(rabbitmq.run())