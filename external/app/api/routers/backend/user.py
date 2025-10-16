from fastapi import APIRouter

from api.shemes import *
from rabbitmq.manager import rabbitmq


router = APIRouter()
tags = ['user']

@router.post('/api/v1/users/check', tags=tags, response_model=Response)
async def check_user(data: UserChatId):
    response = await rabbitmq.publish('check_user', data.model_dump())
    return Response(**response)

@router.post('/api/v1/users/create', tags=tags, response_model=Response)
async def create_user(data: CreateUser):
    response = await rabbitmq.publish('create_user', data.model_dump())
    return Response(**response)

@router.post('/api/v1/users/visits', tags=tags, response_model=Response)
async def read_user_visits(data: UserChatId):
    response = await rabbitmq.publish('read_user_visits', data.model_dump())
    return Response(**response)
    
@router.post('/api/v1/users/visits/create', tags=tags, response_model=Response)
async def create_visit(data: CreateVisit):
    response = await rabbitmq.publish('create_visit', data.model_dump())
    return Response(**response)
    
@router.post('/api/v1/users/visits/delete', tags=tags, response_model=Response)
async def delete_visit(data: VisitId):
    response = await rabbitmq.publish('delete_visit', data.model_dump())
    return Response(**response)
    
@router.post('/api/v1/users/events', tags=tags, response_model=Response)
async def read_user_events(data: UserChatId):
    response = await rabbitmq.publish('read_user_events', data.model_dump())
    return Response(**response)
    
@router.post('/api/v1/users/feedbacks', tags=tags, response_model=Response)
async def read_user_feedbacks(data: UserChatId):
    response = await rabbitmq.publish('read_user_feedbacks', data.model_dump())
    return Response(**response)