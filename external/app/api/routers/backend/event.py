from fastapi import APIRouter

from api.shemes import *
from rabbitmq.manager import rabbitmq


router = APIRouter()
tags = ['event']

@router.post('/api/v1/event/create', tags=tags, response_model=Response)
async def create_event(data: CreateEvent):
    response = await rabbitmq.publish('create_event', data.model_dump())
    return Response(**response)

@router.get('/api/v1/events', tags=tags, response_model=Response)
async def read_events():
    response = await rabbitmq.publish('read_events')
    return Response(**response)

@router.post('/api/v1/event/delete', tags=tags, response_model=Response)
async def delete_event(data: EventId):
    response = await rabbitmq.publish('delete_event', data.model_dump())
    return Response(**response)