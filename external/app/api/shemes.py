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
    
    
class Response(BaseModel):
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
    
    
class Visit(BaseModel):
    visit_id: int
    
    
class Visits(BaseModel):
    msg: str = ''
    success: bool
    data: list = []
    err: str = ''
    
    
class Events(BaseModel):
    msg: str = ''
    success: bool
    data: list = []
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


class CreateCommunity(BaseModel):
    name: str
    discription: str
    question: bool
     
     
class UpdateCommunity(BaseModel):
    community_id: int
    name: str
    discription: str
    question: bool
    
    
class Community(BaseModel):
    community_id: int
    
    
class CreateQuestion(BaseModel):
    user_chat_id: str
    text: str
    
    
class UserQuestions(BaseModel):
    
    class Question(BaseModel):
        question_id: int
        text: str
        date: str
        status: str
    
    msg: str = ''
    success: bool
    questions: list[Question] | list
    err: str = ''
    
    
class Question(BaseModel):
    question_id: int
    
    
class Answer(BaseModel):
    user_chat_id: str
    question_id: int
    text: str

    
class FullQuestion(BaseModel):
    
    class Data(BaseModel):
        text: str
        user_chat_id: str
        date_create: str
        user_name: str
        user_contact: str
        answer: str
        date_answer: str
    
    msg: str = ''
    success: bool
    data: Data | None
    err: str = ''

    
class ShortQuestions(BaseModel):
    
    class Question(BaseModel):
        question_id: int
        status: str
        text: str
        date: str
        user_name: str
    
    msg: str = ''
    success: bool
    questions: list[Question] | list
    err: str = ''