from fastapi import APIRouter

from db.db_manager import db
from api.shemes import Response, CreateCommunity, Communityes, Community, UpdateCommunity


router = APIRouter()

@router.get('/api/v1/communityes', tags=['community'], response_model=Communityes)
async def get_communityes():
    try:
        communityes: list[Communityes.Community] = []
        for community in db.get_communityes():
            communityes.append(
                Communityes.Community(
                    community_id=community.community_id,
                    name=community.name,
                    discription=community.discription,
                    for_spark_part=community.for_spark_park,
                )
            )
        
        return Communityes(communityes=communityes, success=True)

    except Exception as e:
        return Communityes(success=False, err=f'{e}')
    
@router.post('/api/v1/community/create', tags=['community'], response_model=Response)
async def add_community(data: CreateCommunity):
    try:
        db.add_community(data.name, data.discription, data.question)
        return Response(success=True)

    except Exception as e:
        return Response(success=False, err=f'{e}')
    
@router.post('/api/v1/community/update', tags=['community'], response_model=Response)
async def update_community(data: UpdateCommunity):
    try:
        db.update_community(data.community_id, data.name, data.discription, data.question)
        return Response(success=True)

    except Exception as e:
        return Response(success=False, err=f'{e}')
    
@router.post('/api/v1/community/delete', tags=['community'], response_model=Response)
async def del_community(data: Community):
    try:
        db.del_community(data.community_id)
        return Response(success=True)

    except Exception as e:
        return Response(success=False, err=f'{e}')
    