from fastapi import APIRouter

from api.shemes import *
from rabbitmq.manager import rabbitmq


router = APIRouter()
tags = ['community']

@router.post('/api/v1/community/create', tags=tags, response_model=Response)
async def add_community(data: CreateCommunity):
    response = await rabbitmq.publish('create_community', data.model_dump())
    return Response(**response)
    
@router.get('/api/v1/communityes', tags=tags, response_model=Response)
async def read_communityes():
    response = await rabbitmq.publish('read_communityes')
    return Response(**response)
    
@router.post('/api/v1/community/update', tags=tags, response_model=Response)
async def update_community(data: UpdateCommunity):
    response = await rabbitmq.publish('update_community', data.model_dump())
    return Response(**response)
    
@router.post('/api/v1/community/delete', tags=tags, response_model=Response)
async def delete_community(data: CommunityId):
    response = await rabbitmq.publish('delete_community', data.model_dump())
    return Response(**response)