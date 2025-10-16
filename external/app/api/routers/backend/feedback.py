from fastapi import APIRouter

from api.shemes import *
from rabbitmq.manager import rabbitmq


router = APIRouter()
tags = ['feedback']

@router.post('/api/v1/feedback/create', tags=tags, response_model=Response)
async def create_feedback(data: CreateFeedback):
    response = await rabbitmq.publish('create_feedback', data.model_dump())
    return Response(**response)
    
@router.post('/api/v1/feedback', tags=tags, response_model=Response)
async def read_feedback():
    response = await rabbitmq.publish('read_feedback')
    return Response(**response)
    
@router.post('/api/v1/feedback/answer/create', tags=tags, response_model=Response)
async def create_answer(data: CreateAnswer):
    response = await rabbitmq.publish('create_answer')
    return Response(**response)