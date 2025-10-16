import aio_pika, ast
from functools import wraps

from db.db_manager import db
from utils.logger import logger
from rabbitmq.shemes import *


async def check_user(msg: aio_pika.IncomingMessage, channel: aio_pika.RobustChannel):
    async with msg.process():  # Используем контекстный менеджер для ack'а сообщения
        if msg.reply_to:  # Проверяем, требует ли сообщение ответа
            logger.info(f'\n\ncheck_user  |  Полученный msg.body  |  {msg.body.decode()}  |  {type(msg.body.decode())}\n\n')
            
            msg_body = ast.literal_eval(msg.body.decode())  # str to dict, изначально приходят вообще байты
            body = Response(success=True if db.get_user_by_chat_id(msg_body['chat_id']) else False)

            logger.info(f'\n\ncheck_user  |  Отправленный body  |  {str(body.model_dump())}  |  {type(str(body.model_dump()))}\n\n')

            await channel.default_exchange.publish(  # Отправляем ответ в default exchange
                message=aio_pika.Message(
                    body=str(body.model_dump()).encode(),  # Нужно отправлять байты 
                    correlation_id=msg.correlation_id,
                ),
                routing_key=msg.reply_to,  # самое важное
            )

async def create_user(msg: aio_pika.IncomingMessage, channel: aio_pika.RobustChannel):
    async with msg.process():
        if msg.reply_to:
            logger.info(f'\n\ncreate_user  |  Полученный msg.body  |  {msg.body.decode()}  |  {type(msg.body.decode())}\n\n')
            
            msg_body = ast.literal_eval(msg.body.decode())
            
            try:
                text, success = db.create_user(msg_body)
                body = Response(msg=text, success=success)


            except Exception as e:
                body = Response(success=False, err=f'{e}')
    
            logger.info(f'\n\ncreate_user  |  Отправленный body  |  {str(body.model_dump())}  |  {type(str(body.model_dump()))}\n\n')

            await channel.default_exchange.publish(
                message=aio_pika.Message(
                    body=str(body.model_dump()).encode(),
                    correlation_id=msg.correlation_id,
                ),
                routing_key=msg.reply_to,
            )
    
async def get_user_visits(msg: aio_pika.IncomingMessage, channel: aio_pika.RobustChannel):
    async with msg.process():
        if msg.reply_to:
            logger.info(f'\n\nget_user_visits  |  Полученный msg.body  |  {msg.body.decode()}  |  {type(msg.body.decode())}\n\n')
            
            msg_body = ast.literal_eval(msg.body.decode())
            
            try:
                data, success = db.get_user_visits(msg_body['chat_id'])
                body = Visits(data=data, success=success)

            except Exception as e:
                body = Visits(success=False, err=f'{e}')
            
            logger.info(f'\n\nget_user_visits  |  Отправленный body  |  {str(body.model_dump())}  |  {type(str(body.model_dump()))}\n\n')

            await channel.default_exchange.publish(
                message=aio_pika.Message(
                    body=str(body.model_dump()).encode(),
                    correlation_id=msg.correlation_id,
                ),
                routing_key=msg.reply_to,
            )
            
    # try:
    #     visits: list[EventVisits.Visit] = []
    #     for visit in db.get_user_visits(data.chat_id):
    #         visits.append(
    #             EventVisits.Visit(
    #                 visit_id=visit.visit_id,
    #                 event_id=visit.event_id,
    #                 event_name=visit.event.name,
    #                 event_date=str(visit.event.date),
    #                 event_community=visit.event.communiy.name,
    #                 event_discription=visit.event.discription
    #             )
    #         )
            
    #     return EventVisits(visits=visits, success=True)

    # except Exception as e:
    #     return EventVisits(success=False, err=f'{e}')
    
async def create_visit(msg: aio_pika.IncomingMessage, channel: aio_pika.RobustChannel):
    async with msg.process():
        if msg.reply_to:
            logger.info(f'\n\ncreate_visit  |  Полученный msg.body  |  {msg.body.decode()}  |  {type(msg.body.decode())}\n\n')
            
            msg_body = ast.literal_eval(msg.body.decode())
            
            try:
                text, success = db.create_visit(msg_body)
                body = Response(msg=text, success=success)

            except Exception as e:
                body = Response(success=False, err=f'{e}')
    
            logger.info(f'\n\ncreate_visit  |  Отправленный body  |  {str(body.model_dump())}  |  {type(str(body.model_dump()))}\n\n')

            await channel.default_exchange.publish(
                message=aio_pika.Message(
                    body=str(body.model_dump()).encode(),
                    correlation_id=msg.correlation_id,
                ),
                routing_key=msg.reply_to,
            )
    
# @router.post('/api/v1/users/visits/delete', tags=['user'], response_model=Response)
# async def del_visit(data: DeleteEventVisit):
#     try:
#         db.del_user_visit(data.user_chat_id, data.visit_id)
#         return Response(success=True)

#     except Exception as e:
#         return Response(success=False, err=f'{e}')
        
# @router.post('/api/v1/user/events', tags=['user'], response_model=Events)
# async def get_user_actual_events(data: User):
#     try:
#         events: list[Events.Event] = []
#         for event in db.get_user_actual_events(data.chat_id):
#             events.append(
#                 Events.Event(
#                     event_id=event.event_id,
#                     name=event.name,
#                     date=str(event.date),
#                     community=event.communiy.name,
#                     discription=event.discription
#                 )
#             )
        
#         return Events(events=events, success=True)

#     except Exception as e:
#         return Events(success=False, err=f'{e}')
    
# @router.post('/api/v1/user/questions', tags=['user'], response_model=UserQuestions)
# async def get_user_questions(data: User):
#     try:
#         questions: list[UserQuestions.Question] = []
#         sorted_db_questions = sorted(db.get_user_questions(data.chat_id), key=lambda x: x.date, reverse=True)
#         for question in sorted_db_questions:
#             questions.append(
#                 UserQuestions.Question(
#                     question_id=question.question_id,
#                     text=question.text[:50],
#                     date=str(question.date.strftime("%Y-%m-%d")),
#                     status=question.status,
#                 )
#             )
            
#         return UserQuestions(questions=questions, success=True)

#     except Exception as e:
#         return UserQuestions(success=False, err=f'{e}')