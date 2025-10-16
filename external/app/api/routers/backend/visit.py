from fastapi import APIRouter

from api.shemes import *
from rabbitmq.manager import rabbitmq


router = APIRouter()
tags = ['visit']

@router.get('/api/v1/visits', tags=tags, response_model=Response)
async def read_visits():
    response = await rabbitmq.publish('read_visits')
    return Response(**response)
    
@router.post('/api/v1/visit/delete', tags=tags, response_model=Response)
async def delete_visit(data: VisitId):
    response = await rabbitmq.publish('delete_visit', data.model_dump())
    return Response(**response)