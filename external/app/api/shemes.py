from pydantic import BaseModel

    
class Response(BaseModel):
    msg: str = ''
    success: bool
    data: list[dict] = []
    err: str = ''
    
    
class CreateUser(BaseModel):
    chat_id: str
    name: str
    last_name: str
    company: str
    work_in_spark_park: bool
    phone: str


class UserChatId(BaseModel):
    chat_id: str
    
    
class EventId(BaseModel):
    event_id: int


class CreateEvent(BaseModel):
    community_id: int
    name: str
    discription: str
    date: str
    
    
class VisitId(BaseModel):
    visit_id: int
    
    
class CreateVisit(BaseModel):
    user_chat_id: str
    event_id: int
    

class CommunityId(BaseModel):
    community_id: int
    
    
class CreateCommunity(BaseModel):
    name: str
    discription: str
    question: bool
     
     
class UpdateCommunity(BaseModel):
    community_id: int
    name: str
    discription: str
    question: bool
    
    
class CreateFeedback(BaseModel):
    chat_id: str
    text: str
    
    
class CreateAnswer(BaseModel):
    chat_id: str
    feedback_id: int
    text: str