import requests, os
from io import BytesIO
from fastapi import APIRouter

from db.db_manager import db
from api.shemes import AddUser, User, Responce, Events, CreateEventVisit, DeleteEventVisit, EventVisits, CreateCommunity, Communityes, Community, Event, Visits, EventVisit, CreateEvent


router = APIRouter()

@router.post('/api/v1/users/check', tags=['user'], response_model=Responce)
async def check_user(data: User):
    return Responce(success=True if db.get_user_by_chat_id(data.chat_id) else False)
    
@router.post('/api/v1/users/create', tags=['user'], response_model=Responce)
async def add_user(data: AddUser):
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
    
@router.get('/api/v1/events', tags=['event'], response_model=Events)
async def get_events():
    try:
        events: list[Events.Event] = []
        for event in db.get_events():
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
    
@router.post('/api/v1/event/create', tags=['event'], response_model=Responce)
async def add_event(data: CreateEvent):
    try:
        db.add_event(data.community_id, data.name, data.discription, data.date)
        return Responce(success=True)

    except Exception as e:
        return Responce(success=False, err=f'{e}')
    
@router.post('/api/v1/event/delete', tags=['event'], response_model=Responce)
async def del_event(data: Event):
    try:
        db.del_event(data.event_id)
        return Responce(success=True)

    except Exception as e:
        return Responce(success=False, err=f'{e}')
    
@router.get('/api/v1/communityes', tags=['community'], response_model=Communityes)
async def get_communityes():
    try:
        communityes: list[Communityes.Community] = []
        for community in db.get_communityes():
            communityes.append(
                Communityes.Community(
                    community_id=community.communiy_id,
                    name=community.name,
                    discription=community.discription,
                    for_spark_part=community.for_spark_park,
                )
            )
        
        return Communityes(communityes=communityes, success=True)

    except Exception as e:
        return Communityes(success=False, err=f'{e}')
    
@router.post('/api/v1/community/create', tags=['community'], response_model=Responce)
async def add_community(data: CreateCommunity):
    try:
        db.add_community(data.name, data.discription, data.for_spark_part)
        return Responce(success=True)

    except Exception as e:
        return Responce(success=False, err=f'{e}')
    
@router.post('/api/v1/community/delete', tags=['community'], response_model=Responce)
async def del_community(data: Community):
    try:
        db.del_community(data.community_id)
        return Responce(success=True)

    except Exception as e:
        return Responce(success=False, err=f'{e}')
    
@router.get('/api/v1/visits', tags=['visit'], response_model=Visits)
async def get_visits():
    try:
        visits: list[Communityes.Community] = []
        for visit in db.get_visits():
            visits.append(
                Visits.Visit(
                    visit_id=visit.visit_id,
                    user_name=visit.user.name,
                    user_last_name=visit.user.last_name,
                    user_phone=visit.user.phone,
                    community_name=visit.event.communiy.name,
                    event_name=visit.event.name,
                    event_discription=visit.event.discription,
                    event_date=str(visit.event.date),
                )
            )
        
        return Visits(visits=visits, success=True)

    except Exception as e:
        return Visits(success=False, err=f'{e}')
    
@router.post('/api/v1/visit/delete', tags=['visit'], response_model=Responce)
async def del_community(data: EventVisit):
    try:
        db.del_visit(data.visit_id)
        return Responce(success=True)

    except Exception as e:
        return Responce(success=False, err=f'{e}')