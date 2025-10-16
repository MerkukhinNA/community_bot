import asyncio, os

from rabbitmq.manager import rabbitmq


asyncio.run(rabbitmq.run())