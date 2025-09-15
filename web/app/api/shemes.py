from pydantic import BaseModel


class AddUser(BaseModel):
    chat_id: str
    name: str
    last_name: str
    company: str
    work_in_spark_park: bool
    phone: str


class User(BaseModel):
    chat_id: str
    
    
class Responce(BaseModel):
    msg: str = ''
    success: bool
    err: str = ''
    
    
class Event(BaseModel):
    event_id: int


class CreateEvent(BaseModel):
    community_id: int
    name: str
    discription: str
    date: str
    
    
class EventVisit(BaseModel):
    visit_id: int
    
    
class EventVisits(BaseModel):
    
    class Visit(BaseModel):
        visit_id: int
        event_id: int
        event_name: str
        event_date: str
        event_community: str
        event_discription: str
    
    msg: str = ''
    success: bool
    visits: list[Visit] | list
    err: str = ''
    
    
class Events(BaseModel):
    
    class Event(BaseModel):
        event_id: int
        name: str
        date: str
        community: str
        discription: str
    
    msg: str = ''
    success: bool
    events: list[Event] | list
    err: str = ''
    
    
class CreateEventVisit(BaseModel):
    user_chat_id: str
    event_id: int
    
    
class DeleteEventVisit(BaseModel):
    user_chat_id: str
    visit_id: int
    
    
class Communityes(BaseModel):
    
    class Community(BaseModel):
        community_id: int
        name: str
        discription: str
        for_spark_part: bool
    
    msg: str = ''
    success: bool
    communityes: list[Community] | list
    err: str = ''

    
class Visits(BaseModel):
    
    class Visit(BaseModel):
        visit_id: int
        user_name: str
        user_last_name: str
        user_phone: str
        community_name: str
        event_name: str
        event_discription: str
        event_date: str
    
    msg: str = ''
    success: bool
    visits: list[Visit] | list
    err: str = ''

    
class CreateCommunity(BaseModel):
    name: str
    discription: str
    for_spark_part: bool
    
    
class Community(BaseModel):
    community_id: int