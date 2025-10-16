from fastapi import APIRouter

from db.db_manager import db
from rabbitmq.manager import rabbitmq
from utils.logger import logger
from api.shemes import AddUser, User, Response, Events, CreateEventVisit, DeleteEventVisit,\
    Visits, UserQuestions


router = APIRouter()

@router.post('/api/v1/users/check', tags=['user'], response_model=Response)
async def check_user(data: User):
    response = await rabbitmq.publish('check_user', data.model_dump())
    logger.info(f'\n\nuser_check response   |  {response}  |  {type(response)}\n\n')
    
    return Response(**response)

@router.post('/api/v1/users/create', tags=['user'], response_model=Response)
async def create_user(data: AddUser):
    response = await rabbitmq.publish('create_user', data.model_dump())
    logger.info(f'\n\nuser_create response   |  {response}  |  {type(response)}\n\n')
    
    return Response(**response)

@router.post('/api/v1/users/visits', tags=['user'], response_model=Visits)
async def get_user_visits(data: User):
    response = await rabbitmq.publish('get_user_visits', data.model_dump())
    logger.info(f'\n\nget_user_visits response   |  {response}  |  {type(response)}\n\n')
    
    return Visits(**response)
    
@router.post('/api/v1/users/visits/create', tags=['user'], response_model=Response)
async def create_visit(data: CreateEventVisit):
    response = await rabbitmq.publish('create_visit', data.model_dump())
    logger.info(f'\n\nvisit_create response   |  {response}  |  {type(response)}\n\n')
    
    return Response(**response)
    
@router.post('/api/v1/users/visits/delete', tags=['user'], response_model=Response)
async def del_visit(data: DeleteEventVisit):
    try:
        db.del_user_visit(data.user_chat_id, data.visit_id)
        return Response(success=True)

    except Exception as e:
        return Response(success=False, err=f'{e}')
        
@router.post('/api/v1/user/events', tags=['user'], response_model=Events)
async def get_user_actual_events(data: User):
    try:
        events: list[Events.Event] = []
        for event in db.get_user_actual_events(data.chat_id):
            events.append(
                Events.Event(
                    event_id=event.event_id,
                    name=event.name,
                    date=str(event.date),
                    community=event.communiy.name,
                    discription=event.discription
                )
            )
        
        return Events(events=events, success=True)

    except Exception as e:
        return Events(success=False, err=f'{e}')
    
@router.post('/api/v1/user/questions', tags=['user'], response_model=UserQuestions)
async def get_user_questions(data: User):
    try:
        questions: list[UserQuestions.Question] = []
        sorted_db_questions = sorted(db.get_user_questions(data.chat_id), key=lambda x: x.date, reverse=True)
        for question in sorted_db_questions:
            questions.append(
                UserQuestions.Question(
                    question_id=question.question_id,
                    text=question.text[:50],
                    date=str(question.date.strftime("%Y-%m-%d")),
                    status=question.status,
                )
            )
            
        return UserQuestions(questions=questions, success=True)

    except Exception as e:
        return UserQuestions(success=False, err=f'{e}')