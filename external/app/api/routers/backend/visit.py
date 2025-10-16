from fastapi import APIRouter

from db.db_manager import db
from db.enum import UserQuestionStatus
from api.shemes import Response, Communityes, Visits, Visit


router = APIRouter()

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
    
@router.post('/api/v1/visit/delete', tags=['visit'], response_model=Response)
async def del_community(data: Visit):
    try:
        db.del_visit(data.visit_id)
        return Response(success=True)

    except Exception as e:
        return Response(success=False, err=f'{e}')