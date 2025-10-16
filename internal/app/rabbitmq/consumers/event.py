import aio_pika, ast, sys
from aio_pika import IncomingMessage, RobustChannel

from db.manager import db
from rabbitmq.shemes import *
from utils.logger import logger, log_data_received, log_data_sent


async def create_event(msg: aio_pika.IncomingMessage, channel: RobustChannel):
    async with msg.process():
        if msg.reply_to:
            log_data_received(sys._getframe().f_code.co_name, msg)
            
            msg_body = ast.literal_eval(msg.body.decode())
     
            try:
                db.create_event(
                    int(msg_body['community_id']),
                    msg_body['name'],
                    msg_body['discription'],
                    msg_body['date']
                )
                body = Response(success=True)

            except Exception as e:
                body = Response(success=False, err=f'{e}')
    
            log_data_sent(sys._getframe().f_code.co_name, body)

            await channel.default_exchange.publish(
                message=aio_pika.Message(
                    body=str(body.model_dump()).encode(),
                    correlation_id=msg.correlation_id,
                ),
                routing_key=msg.reply_to,
            )
            
async def read_events(msg: aio_pika.IncomingMessage, channel: RobustChannel):
    async with msg.process():
        if msg.reply_to:
            log_data_received(sys._getframe().f_code.co_name, msg)
            
            try:
                data = db.get_events()
                body = Response(
                    success=True,
                    data=[
                        {
                            'event_id': item.event_id,
                            'name': item.name,
                            'community': item.communiy.name,
                            'discription': item.discription,
                            'date': item.date.strftime('%Y-%m-%d %H:%M:%S')
                        } 
                        for item in data
                    ]
                )

            except Exception as e:
                body = Response(success=False, err=f'{e}')
            
            log_data_sent(sys._getframe().f_code.co_name, body)

            await channel.default_exchange.publish(
                message=aio_pika.Message(
                    body=str(body.model_dump()).encode(),
                    correlation_id=msg.correlation_id,
                ),
                routing_key=msg.reply_to,
            )
            
async def delete_event(msg: aio_pika.IncomingMessage, channel: RobustChannel):
    async with msg.process():
        if msg.reply_to:
            log_data_received(sys._getframe().f_code.co_name, msg)
            
            msg_body = ast.literal_eval(msg.body.decode())
            
            try:
                db.delete_event(int(msg_body['event_id']))
                body = Response(success=True)

            except Exception as e:
                body = Response(success=False, err=f'{e}')
    
            log_data_sent(sys._getframe().f_code.co_name, body)

            await channel.default_exchange.publish(
                message=aio_pika.Message(
                    body=str(body.model_dump()).encode(),
                    correlation_id=msg.correlation_id,
                ),
                routing_key=msg.reply_to,
            )