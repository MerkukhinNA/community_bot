import aio_pika, ast, sys
from aio_pika import IncomingMessage, RobustChannel

from db.manager import db
from rabbitmq.shemes import *
from utils.logger import logger, log_data_received, log_data_sent


async def create_feedback(msg: IncomingMessage, channel: RobustChannel):
    async with msg.process():
        if msg.reply_to:
            log_data_received(sys._getframe().f_code.co_name, msg)
            
            msg_body = ast.literal_eval(msg.body.decode())
     
            try:
                db.create_feedback(msg_body['chat_id'], msg_body['text'])
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

async def read_feedback(msg: IncomingMessage, channel: RobustChannel):
    async with msg.process():
        if msg.reply_to:
            log_data_received(sys._getframe().f_code.co_name, msg)
            
            msg_body = ast.literal_eval(msg.body.decode())

            try:
                data = db.get_feedback(msg_body['feedback_id'])
                body = Response(
                    success=True,
                    data=[
                        {
                            'text': data.text,
                            'feedback_id': data.feedback_id,
                            'user_chat_id': data.user.chat_id,
                            'user_name': data.user.name + ' ' + data.user.last_name,
                            'user_contact': data.user.phone,
                            'status': data.status.value,
                            'answer':
                                'УК еще не ответила' if not data.answer 
                                else data.answer.text,
                            'date_create': data.date.strftime("%Y-%m-%d %H:%M:%S"),
                            'date_answer':
                                '-' if not data.answer 
                                else str(data.answer.date.strftime("%Y-%m-%d %H:%M:%S"))
                        } 
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

async def create_asnwer(msg: IncomingMessage, channel: RobustChannel):
    pass
    # try:
    #     db.add_asnwer(data.user_chat_id, data.feedback_id, data.text)
    #     return Response(success=True)

    # except Exception as e:
    #     return Response(success=False, err=f'{e}')