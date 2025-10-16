import sqlalchemy, os
import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from db.models import Base, User, Community, Event, Visit, VisitStatus, Feedback, Answer
from db.enum import FeedbackStatus


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
    
    def get_user_visits(self, chat_id: str) -> list[Visit]:
        user_id = db.get_user_by_chat_id(chat_id).user_id
        
        with self.create_session() as session:
            visits = session.query(Visit).filter(
                and_(
                    Visit.user_id == user_id,
                    Visit.deleted == False,
                )
            ).all()
            visits = [visit for visit in visits if visit.event.date >= datetime.datetime.today()]
            
            return visits
    
    def get_user_events(self, chat_id: str) -> list[Event]:
        user = db.get_user_by_chat_id(chat_id)
        
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
        
    def get_user_feedbacks(self, user_chat_id: str) -> list[Feedback]:
        user = db.get_user_by_chat_id(user_chat_id)
        
        with self.create_session() as session:
            feedback = session.query(Feedback).filter(
                and_(
                    Feedback.user_id == user.user_id,
                    Feedback.deleted == False,
                )
            ).all()
            
            return feedback
    
    def get_feedbacks(self) -> list[Feedback]:
        with self.create_session() as session:
            return session.query(Feedback).filter_by(deleted=False).all()
    
    def create_visit(self, data: dict[str, str]) -> tuple[str, bool]:
        with self.create_session() as session:
            if session.query(Visit).filter(
                and_(
                    Visit.event_id == data['event_id'],
                    Visit.user_id == data['user_chat_id']
                )
            ).first():
                return 'event visit is already exist', False
            
            session.add(
                Visit(
                    event_id=data['event_id'],
                    user_id=db.get_user_by_chat_id(data['user_chat_id']).user_id
                )
            )
            session.commit()
            
            return '', True
    
    def delete_visit(self, visit_id: int) -> None:
        with self.create_session() as session:
            visit = session.query(Visit).filter_by(visit_id=visit_id).first()
            visit.deleted = True
            session.commit()
        
    def get_communityes(self) -> list[Community]:
        with self.create_session() as session:
            return session.query(Community).filter_by(deleted=False).all()
    
    def create_community(self, name: str, discription: str, feedback: bool) -> None:
        with self.create_session() as session:
            session.add(
                Community(
                    name=name,
                    discription=discription,
                    for_spark_park=feedback,
                )
            )
            session.commit()
    
    def update_community(self, community_id: int, name: str, discription: str, feedback: bool) -> None:
        with self.create_session() as session:
            community = session.query(Community).filter_by(community_id=community_id).first()
            community.name = name
            community.discription = discription
            community.for_spark_park = feedback
            session.commit()
    
    def delete_community(self, community_id: int) -> None:
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
    
    def create_event(self, community_id: int, name: str, discription: str, date: str) -> None:
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
    
    def delete_event(self, event_id: int) -> None:
        with self.create_session() as session:
            event = session.query(Event).filter_by(event_id=event_id).first()
            event.deleted = True
            
            for visit in event.visits:
                visit.deleted = True
                    
            session.commit()
            
    def get_all_visits(self) -> list[Visit]:
        with self.create_session() as session:
            return session.query(Visit).filter_by(deleted=False).all()
        
    def create_feedback(self, chat_id: str, text: str) -> None:
        with self.create_session() as session:
            session.add(
                Feedback(
                    user_id=db.get_user_by_chat_id(chat_id).user_id,
                    text=text,
                    date=datetime.datetime.now()
                )
            )
            session.commit()
            
    def create_asnwer(self, user_chat_id: str, feedback_id: int, text: str) -> None:
        with self.create_session() as session:
            answer = session.query(Answer).filter_by(feedback_id=feedback_id).first()
            
            if answer:
                answer.user_id = db.get_user_by_chat_id(user_chat_id).user_id
                answer.text = text
                answer.date = datetime.datetime.now()
            
            else:
                answer = Answer(
                    user_id=db.get_user_by_chat_id(user_chat_id).user_id,
                    feedback_id=feedback_id,
                    text=text,
                    date=datetime.datetime.now()
                )
                session.add(answer)
                session.commit()
                answer.feedback.status = FeedbackStatus.ANSWERED
            
            session.commit()

    def get_feedback(self, feedback_id: id) -> Feedback:
        with self.create_session() as session:
            return session.query(Feedback).filter_by(feedback_id=feedback_id).first()
    
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