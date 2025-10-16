import aio_pika, ast, sys
from aio_pika import IncomingMessage, RobustChannel

from db.manager import db
from rabbitmq.shemes import *
from utils.logger import logger, log_data_received, log_data_sent


async def check_user(msg: IncomingMessage, channel: RobustChannel):
    async with msg.process():  # Используем контекстный менеджер для ack'а сообщения
        if msg.reply_to:  # Проверяем, требует ли сообщение ответа
            log_data_received(sys._getframe().f_code.co_name, msg)
            
            msg_body = ast.literal_eval(msg.body.decode())  # str to dict, изначально приходят вообще байты
            user = db.get_user_by_chat_id(msg_body['chat_id'])
            body = Response(success=True if user else False)

            log_data_sent(sys._getframe().f_code.co_name, body)

            await channel.default_exchange.publish(  # Отправляем ответ в default exchange
                message=aio_pika.Message(
                    body=str(body.model_dump()).encode(),  # Нужно отправлять байты 
                    correlation_id=msg.correlation_id,
                ),
                routing_key=msg.reply_to,  # самое важное
            )

async def create_user(msg: aio_pika.IncomingMessage, channel: RobustChannel):
    async with msg.process():
        if msg.reply_to:
            log_data_received(sys._getframe().f_code.co_name, msg)
            
            msg_body = ast.literal_eval(msg.body.decode())
            
            try:
                message, success = db.create_user(msg_body)
                body = Response(msg=message, success=success)

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
    
async def read_user_visits(msg: aio_pika.IncomingMessage, channel: RobustChannel):
    async with msg.process():
        if msg.reply_to:
            log_data_received(sys._getframe().f_code.co_name, msg)
            
            msg_body = ast.literal_eval(msg.body.decode())
            
            try:
                data = db.get_user_visits(msg_body['chat_id'])
                body = Response(
                    success=True,
                    data=[
                        {
                            'visit_id': item.visit_id,
                            'event_id': item.event_id,
                            'user_id': item.user_id,
                            'status': item.status.value,
                            'deleted': item.deleted,
                            'event_name': item.event.name,
                            'event_discription': item.event.discription,
                            'date': item.event.date.strftime('%Y-%m-%d %H:%M:%S'),
                            'community_name': item.event.communiy.name,
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
    
async def create_visit(msg: aio_pika.IncomingMessage, channel: RobustChannel):
    async with msg.process():
        if msg.reply_to:
            log_data_received(sys._getframe().f_code.co_name, msg)
            
            msg_body = ast.literal_eval(msg.body.decode())
            
            try:
                message, success = db.create_visit(msg_body)
                body = Response(msg=message, success=success)

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
    
async def read_user_events(msg: aio_pika.IncomingMessage, channel: RobustChannel):
    async with msg.process():
        if msg.reply_to:
            log_data_received(sys._getframe().f_code.co_name, msg)
            
            msg_body = ast.literal_eval(msg.body.decode())
            
            try:
                data = db.get_user_events(msg_body['chat_id'])
                body = Response(
                    success=True,
                    data=[
                        {
                            'event_id': item.event_id,
                            'name': item.name,
                            'date': item.date.strftime('%Y-%m-%d %H:%M:%S'),
                            'discription': item.discription,
                            'community_name': item.communiy.name
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
       
async def read_user_feedbacks(msg: aio_pika.IncomingMessage, channel: RobustChannel):
    async with msg.process():
        if msg.reply_to:
            log_data_received(sys._getframe().f_code.co_name, msg)
            
            msg_body = ast.literal_eval(msg.body.decode())
            
            try:
                data = db.get_user_feedbacks(msg_body['chat_id'])
                body = Response(
                    success=True,
                    data=[
                        {
                            'feedback_id': feedback.feedback_id,
                            'text': feedback.text[:50],
                            'date': str(feedback.date.strftime("%Y-%m-%d")),
                            'status': feedback.status.value
                        }
                        for feedback in sorted(data, key=lambda x: x.date, reverse=True)
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