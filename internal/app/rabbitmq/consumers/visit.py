import aio_pika, ast, sys
from aio_pika import IncomingMessage, RobustChannel

from db.manager import db
from rabbitmq.shemes import *
from utils.logger import logger, log_data_received, log_data_sent


async def read_visits(msg: IncomingMessage, channel: RobustChannel):
    async with msg.process():
        if msg.reply_to:
            log_data_received(sys._getframe().f_code.co_name, msg)
            
            try:
                data = db.get_all_visits()
                body = Response(
                    success=True,
                    data=[
                        {
                            'visit_id': item.visit_id,
                            'user_name': item.user.name,
                            'user_last_name': item.user.last_name,
                            'user_phone': item.user.phone,
                            'community_name': item.event.communiy.name,
                            'event_name': item.event.name,
                            'event_discription': item.event.discription,
                            'date': item.event.date.strftime('%Y-%m-%d %H:%M:%S')
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
         
async def delete_visit(msg: aio_pika.IncomingMessage, channel: RobustChannel):
    async with msg.process():
        if msg.reply_to:
            log_data_received(sys._getframe().f_code.co_name, msg)
            
            msg_body = ast.literal_eval(msg.body.decode())
            
            try:
                db.delete_visit(int(msg_body['visit_id']))
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