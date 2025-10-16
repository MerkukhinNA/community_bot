import sqlalchemy, os
import datetime, copy
from sqlalchemy.orm import Session
from sqlalchemy import and_

from db.models import Base, User, Community, Event, EventVisit, EventVisitStatus, Question, Answer
from db.enum import UserQuestionStatus


class DBManager:
    
    def __init__(self) -> None:
        self.engine = sqlalchemy.create_engine(os.environ['DB_URL'], echo=True)

    def create_session(self) -> Session:
        return Session(self.engine)
    
    def get_user_by_chat_id(self, chat_id: str) -> User | None:
        with self.create_session() as session:
            return session.query(User).filter_by(chat_id=chat_id).first()
    
    def create_user(self, data: dict[str, str]) -> tuple[str, bool]:
        with self.create_session() as session:
            if session.query(User).filter_by(chat_id=data['chat_id']).first():
                return 'user is already exist', False
            
            session.add(User(
                chat_id=data['chat_id'],
                name=data['name'],
                last_name=data['last_name'],
                company=data['company'],
                work_in_spark_park=bool(data['work_in_spark_park']),
                phone=data['phone'],
            ))
            session.commit()
            
            return '', True
    
    def get_user_visits(self, chat_id: str) -> tuple[list[dict], bool]:
        user_id = db.get_user_by_chat_id(chat_id).user_id
        
        with self.create_session() as session:
            visits = session.query(EventVisit).filter(
                and_(
                    EventVisit.user_id == user_id,
                    EventVisit.deleted == False,
                )
            ).all()
            visits = [visit.__dict__ for visit in visits if visit.event.date >= datetime.datetime.today()]
            # EventVisit
            return visits, True
    
    def del_user_visit(self, user_chat_id: str, visit_id: int) -> None:
        user_id = db.get_user_by_chat_id(user_chat_id).user_id
        
        with self.create_session() as session:
            visit = session.query(EventVisit).filter(
                and_(
                    EventVisit.visit_id == visit_id,
                    EventVisit.user_id == user_id,
                )
            ).first()
            visit.deleted = True
            session.commit()
            
    def get_user_actual_events(self, user_chat_id: str) -> list[Event]:
        user = db.get_user_by_chat_id(user_chat_id)
        
        with self.create_session() as session:
            db_events = session.query(Event).filter(
                and_(
                    Event.date >= datetime.datetime.today(),
                    Event.deleted == False,
                )
            ).all()
            
            actual_events = []
            for event in db_events:
                actual = True
                
                if not user.work_in_spark_park and event.communiy.for_spark_park:
                    actual = False
                
                for visit in event.visits:
                    if visit.user_id == user.user_id and visit.deleted == False:
                        actual = False
                        
                if actual:
                    actual_events.append(event)
             
            return actual_events
        
    def get_user_questions(self, user_chat_id: str) -> list[Question]:
        user = db.get_user_by_chat_id(user_chat_id)
        
        with self.create_session() as session:
            question = session.query(Question).filter(
                and_(
                    Question.user_id == user.user_id,
                    Question.deleted == False,
                )
            ).all()
            
            return question
    
    def get_questions(self) -> list[Question]:
        with self.create_session() as session:
            return session.query(Question).filter_by(deleted=False).all()
    
    def create_visit(self, data: dict[str, str]) -> tuple[str, bool]:
        with self.create_session() as session:
            if session.query(EventVisit).filter(
                and_(
                    EventVisit.event_id == data['event_id'],
                    EventVisit.user_id == data['user_chat_id']
                )
            ).first():
                return 'event visit is already exist', False
            
            session.add(
                EventVisit(
                    event_id=data['event_id'],
                    user_id=db.get_user_by_chat_id(data['user_chat_id']).user_id
                )
            )
            session.commit()
            
            return '', True
    
    def get_communityes(self) -> list[Community]:
        with self.create_session() as session:
            return session.query(Community).filter_by(deleted=False).all()
    
    def add_community(self, name: str, discription: str, question: bool) -> None:
        with self.create_session() as session:
            session.add(
                Community(
                    name=name,
                    discription=discription,
                    for_spark_park=question,
                )
            )
            session.commit()
    
    def update_community(self, community_id: int, name: str, discription: str, question: bool) -> None:
        with self.create_session() as session:
            community = session.query(Community).filter_by(community_id=community_id).first()
            community.name = name
            community.discription = discription
            community.for_spark_park = question
            session.commit()
    
    def del_community(self, community_id: int) -> None:
        with self.create_session() as session:
            community = session.query(Community).filter_by(community_id=community_id).first()
            community.deleted = True
            
            for event in community.events:
                event.deleted = True
                
                for visit in event.visits:
                    visit.deleted = True
                    
            session.commit()
            
    def get_events(self) -> list[Community]:
        with self.create_session() as session:
            return session.query(Event).filter_by(deleted=False).all()
    
    def add_event(self, community_id: int, name: str, discription: str, date: str) -> None:
        with self.create_session() as session:
            session.add(
                Event(
                    community_id=community_id,
                    name=name,
                    discription=discription,
                    date=datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S'),
                )
            )
            session.commit()
    
    def del_event(self, event_id: int) -> None:
        with self.create_session() as session:
            event = session.query(Event).filter_by(event_id=event_id).first()
            event.deleted = True
            
            for visit in event.visits:
                visit.deleted = True
                    
            session.commit()
            
    def get_all_visits(self) -> list[EventVisit]:
        with self.create_session() as session:
            return session.query(EventVisit).filter_by(deleted=False).all()
        
    def del_visit(self, visit_id: int) -> None:
        with self.create_session() as session:
            visit = session.query(EventVisit).filter_by(visit_id=visit_id).first()
            visit.deleted = True
            session.commit()
            
    def add_question(self, user_chat_id: str, text: str) -> None:
        with self.create_session() as session:
            session.add(
                Question(
                    user_id=db.get_user_by_chat_id(user_chat_id).user_id,
                    text=text,
                    date=datetime.datetime.now()
                )
            )
            session.commit()
            
    def add_asnwer(self, user_chat_id: str, question_id: int, text: str) -> None:
        with self.create_session() as session:
            answer = session.query(Answer).filter_by(question_id=question_id).first()
            
            if answer:
                answer.user_id = db.get_user_by_chat_id(user_chat_id).user_id
                answer.text = text
                answer.date = datetime.datetime.now()
            
            else:
                answer = Answer(
                    user_id=db.get_user_by_chat_id(user_chat_id).user_id,
                    question_id=question_id,
                    text=text,
                    date=datetime.datetime.now()
                )
                session.add(answer)
                session.commit()
                answer.question.status = UserQuestionStatus.ANSWERED
            
            session.commit()

    def get_question(self, question_id: id) -> Question:
        with self.create_session() as session:
            return session.query(Question).filter_by(question_id=question_id).first()
    
    def start_setup(self) -> None:
        Base.metadata.create_all(bind=self.engine)
        
        # with self.create_session() as session:
        #     session.add(Community(
        #         name='Настольные игры',
        #         discription='клуб любителей настольных игр'
        #     ))
        #     session.add(Community(
        #         name='Шахматы',
        #         discription='клуб любителей шахмат'
        #     ))
        #     session.add(Community(
        #         name='Книжный клуб',
        #         discription='клуб любителей книг'
        #     ))
        #     session.add(Community(
        #         name='Кибер клуб',
        #         discription='клуб любителей видеоигр'
        #     ))
        #     session.add(Community(
        #         name='Вокальный клуб',
        #         discription='клуб вокальных любителей'
        #     ))
        #     session.add(Community(
        #         name='Беговой клуб',
        #         discription='клуб любителей бега'
        #     ))
        #     session.commit()
    
    
db = DBManager()