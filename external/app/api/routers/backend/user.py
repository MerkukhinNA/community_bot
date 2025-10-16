import os, json
from fastapi import APIRouter

from db.db_manager import db
from rabbitmq.manager import rabbitmq
from api.shemes import AddUser, User, Responce, Events, CreateEventVisit, DeleteEventVisit, EventVisits,\
    CreateCommunity, Communityes, Community, Event, Visits, EventVisit, CreateEvent, UpdateCommunity,\
    CreateQuestion, UserQuestions, Question, FullQuestion, ShortQuestions, Answer


router = APIRouter()

@router.post('/api/v1/users/check', tags=['user'], response_model=Responce)
async def check_user(data: User):
    rabbitmq.publish('user_check', data.model_dump())

    return Responce(success=True if db.get_user_by_chat_id(data.chat_id) else False)
    
@router.post('/api/v1/users/create', tags=['user'], response_model=Responce)
async def add_user(data: AddUser):
    rabbitmq.publish('user_create', data.model_dump())

    try:
        db.add_user(data)
        return Responce(msg='auth is success', success=True)

    except Exception as e:
        return Responce(msg='auth is unsuccess', success=False, err=f'{e}')
    
@router.post('/api/v1/users/visits', tags=['user'], response_model=EventVisits)
async def get_user_visits(data: User):
    try:
        visits: list[EventVisits.Visit] = []
        for visit in db.get_user_visits(data.chat_id):
            visits.append(
                EventVisits.Visit(
                    visit_id=visit.visit_id,
                    event_id=visit.event_id,
                    event_name=visit.event.name,
                    event_date=str(visit.event.date),
                    event_community=visit.event.communiy.name,
                    event_discription=visit.event.discription
                )
            )
            
        return EventVisits(visits=visits, success=True)

    except Exception as e:
        return EventVisits(success=False, err=f'{e}')
    
@router.post('/api/v1/users/visits/create', tags=['user'], response_model=Responce)
async def add_event(data: CreateEventVisit):
    try:
        db.create_event_visit(data.user_chat_id, data.event_id)
        return Responce(success=True)

    except Exception as e:
        return Responce(success=False, err=f'{e}')
    
@router.post('/api/v1/users/visits/delete', tags=['user'], response_model=Responce)
async def del_visit(data: DeleteEventVisit):
    try:
        db.del_user_visit(data.user_chat_id, data.visit_id)
        return Responce(success=True)

    except Exception as e:
        return Responce(success=False, err=f'{e}')
        
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