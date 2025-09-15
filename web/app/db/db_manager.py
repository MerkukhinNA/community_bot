import sqlalchemy, os
import datetime, copy
from sqlalchemy.orm import Session
from sqlalchemy import and_

from db.models import Base, User, Community, Event, EventVisit, EventVisitStatus


class DBManager:
    
    def __init__(self) -> None:
        self.engine = sqlalchemy.create_engine(os.environ['DB_URL'], echo=True)

    def create_session(self) -> Session:
        return Session(self.engine)
    
    def get_user_by_chat_id(self, chat_id: str) -> User | None:
        with self.create_session() as session:
            return session.query(User).filter_by(chat_id=chat_id).first()
    
    def add_user(self, user: User):
        with self.create_session() as session:
            print(f'\n\n{type(user)} {user}\n\n')
            
            session.add(User(
                chat_id=user.chat_id,      
                name=user.name,
                last_name=user.last_name,      
                company=user.company,     
                work_in_spark_park=user.work_in_spark_park,     
                phone=user.phone,     
            ))
            session.commit()
    
    def get_user_visits(self, user_chat_id: str) -> list[EventVisit]:
        user_id = db.get_user_by_chat_id(user_chat_id).user_id
        
        with self.create_session() as session:
            visits = session.query(EventVisit).filter(
                and_(
                    EventVisit.user_id == user_id,
                    EventVisit.deleted == False,
                )
            ).all()
            visits = [visit for visit in visits if visit.event.date >= datetime.datetime.today()]
            
            return visits
    
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
        user_id = db.get_user_by_chat_id(user_chat_id).user_id
        
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
                
                for visit in event.visits:
                    if visit.user_id == user_id and visit.deleted == False:
                        actual = False
                        
                if actual:
                    actual_events.append(event)
             
            return actual_events
    
    def create_event_visit(self, user_chat_id: str, event_id: int) -> None:
        with self.create_session() as session:
            session.add(
                EventVisit(
                    event_id=event_id,
                    user_id=db.get_user_by_chat_id(user_chat_id).user_id
                )
            )
            session.commit()
    
    def get_communityes(self) -> list[Community]:
        with self.create_session() as session:
            return session.query(Community).filter_by(deleted=False).all()
    
    def add_community(self, name: str, discription: str, for_spark_park: bool) -> None:
        with self.create_session() as session:
            session.add(
                Community(
                    name=name,
                    discription=discription,
                    for_spark_park=for_spark_park,
                )
            )
            session.commit()
    
    def del_community(self, community_id: int) -> None:
        with self.create_session() as session:
            community = session.query(Community).filter_by(communiy_id=community_id).first()
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
                    communiy_id=community_id,
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
            
    def get_visits(self) -> list[EventVisit]:
        with self.create_session() as session:
            return session.query(EventVisit).filter_by(deleted=False).all()
        
    def del_visit(self, visit_id: int) -> None:
        with self.create_session() as session:
            visit = session.query(EventVisit).filter_by(visit_id=visit_id).first()
            visit.deleted = True
            session.commit()
            
    def start_setup(self) -> None:
        Base.metadata.create_all(bind=self.engine)
        
        with self.create_session() as session:
            session.add(Community(
                name='Настольные игры',
                discription='клуб любителей настольных игр'
            ))
            session.add(Community(
                name='Шахматы',
                discription='клуб любителей шахмат'
            ))
            session.add(Community(
                name='Книжный клуб',
                discription='клуб любителей книг'
            ))
            session.add(Community(
                name='Кибер клуб',
                discription='клуб любителей видеоигр'
            ))
            session.add(Community(
                name='Вокальный клуб',
                discription='клуб вокальных любителей'
            ))
            session.add(Community(
                name='Беговой клуб',
                discription='клуб любителей бега'
            ))
            session.commit()
    
    
db = DBManager()