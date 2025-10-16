# from db.db_manager import db


# router = APIRouter()

# @router.get('/api/v1/events', tags=['event'], response_model=Events)
# async def get_events():
#     try:
#         events: list[Events.Event] = []
#         for event in db.get_events():
#             events.append(
#                 Events.Event(
#                     event_id=event.event_id,
#                     name=event.name,
#                     date=str(event.date),
#                     community=event.communiy.name,
#                     discription=event.discription
#                 )
#             )
        
#         return Events(events=events, success=True)

#     except Exception as e:
#         return Events(success=False, err=f'{e}')
    
# @router.post('/api/v1/event/create', tags=['event'], response_model=Response)
# async def add_event(data: CreateEvent):
#     try:
#         db.add_event(data.community_id, data.name, data.discription, data.date)
#         return Response(success=True)

#     except Exception as e:
#         return Response(success=False, err=f'{e}')
    
# @router.post('/api/v1/event/delete', tags=['event'], response_model=Response)
# async def del_event(data: Event):
#     try:
#         db.del_event(data.event_id)
#         return Response(success=True)

#     except Exception as e:
#         return Response(success=False, err=f'{e}')
    
