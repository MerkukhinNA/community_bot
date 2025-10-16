import aio_pika, ast, sys
from aio_pika import IncomingMessage, RobustChannel

from db.manager import db
from rabbitmq.shemes import *
from utils.logger import logger, log_data_received, log_data_sent


async def create_community(msg: aio_pika.IncomingMessage, channel: RobustChannel):
    async with msg.process():
        if msg.reply_to:
            log_data_received(sys._getframe().f_code.co_name, msg)
            
            msg_body = ast.literal_eval(msg.body.decode())
     
            try:
                db.create_community(msg_body['name'], msg_body['discription'], msg_body['question'])
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
            
async def read_communityes(msg: aio_pika.IncomingMessage, channel: RobustChannel):
    async with msg.process():
        if msg.reply_to:
            log_data_received(sys._getframe().f_code.co_name, msg)
            
            try:
                data = db.get_communityes()
                body = Response(
                    success=True,
                    data=[
                        {
                            'community_id': item.community_id,
                            'name': item.name,
                            'discription': item.discription,
                            'for_spark_part': item.for_spark_park,
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
    
async def update_community(msg: aio_pika.IncomingMessage, channel: RobustChannel):
    async with msg.process():
        if msg.reply_to:
            log_data_received(sys._getframe().f_code.co_name, msg)
            
            msg_body = ast.literal_eval(msg.body.decode())
            
            try:
                db.update_community(
                    int(msg_body['community_id']),
                    msg_body['name'],
                    msg_body['discription'],
                    bool(msg_body['question']),
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
    
async def delete_community(msg: aio_pika.IncomingMessage, channel: RobustChannel):
    async with msg.process():
        if msg.reply_to:
            log_data_received(sys._getframe().f_code.co_name, msg)
            
            msg_body = ast.literal_eval(msg.body.decode())
            
            try:
                db.delete_community(int(msg_body['community_id']))
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