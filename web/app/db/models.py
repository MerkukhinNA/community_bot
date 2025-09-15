from datetime import date, datetime as dt
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import  Column, Integer, String, Text, Boolean, TIMESTAMP, Date, ForeignKey, Identity, BigInteger, Enum
from enum import Enum as PyEnum


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Identity(), primary_key=True, index=True)
    chat_id: Mapped[str] = mapped_column(Text(), nullable=True)
    phone: Mapped[str] = mapped_column(Text(), nullable=True)
    name: Mapped[str] = mapped_column(Text(), nullable=True)
    last_name: Mapped[str] = mapped_column(Text(), nullable=True)
    work_in_spark_park: Mapped[bool] = mapped_column(Boolean(), nullable=True, default=False)
    company: Mapped[str] = mapped_column(Text(), nullable=True)

    event_visits: Mapped[list['EventVisit']] = relationship('EventVisit', back_populates='user') 


class Log(Base):
    __tablename__ = "logs"
    
    log_id: Mapped[int] = mapped_column(Identity(), primary_key=True, index=True)
    datetime: Mapped[dt] = mapped_column(TIMESTAMP(), nullable=True)
    level: Mapped[str] = mapped_column(Text(), nullable=True)
    user_id: Mapped[int] = mapped_column(BigInteger(), nullable=True)
    service: Mapped[str] = mapped_column(Text(), nullable=True)
    text: Mapped[str] = mapped_column(Text(), nullable=True)


class Community(Base):
    __tablename__ = "communities"
    
    communiy_id: Mapped[int] = mapped_column(Identity(), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(Text(), nullable=True)
    discription: Mapped[str] = mapped_column(Text(), nullable=True)
    for_spark_park: Mapped[bool] = mapped_column(Boolean(), nullable=True, default=False)
    deleted: Mapped[bool] = mapped_column(Boolean(), nullable=True, default=False)
    
    events: Mapped[list['Event']] = relationship('Event', back_populates='communiy') 


class Event(Base):
    __tablename__ = "event"
    
    event_id: Mapped[int] = mapped_column(Identity(), primary_key=True, index=True)
    communiy_id: Mapped[int] = mapped_column(Integer(), ForeignKey('communities.communiy_id'), nullable=True)
    name: Mapped[str] = mapped_column(Text(), nullable=True)
    discription: Mapped[str] = mapped_column(Text(), nullable=True)
    date: Mapped[dt] = mapped_column(TIMESTAMP(), nullable=True)
    deleted: Mapped[bool] = mapped_column(Boolean(), nullable=True, default=False)

    communiy: Mapped['Community'] = relationship('Community', back_populates='events', lazy='joined') 
    visits: Mapped[list['EventVisit']] = relationship('EventVisit', back_populates='event') 
    
    
class EventVisitStatus(PyEnum):
    CREATED='created'
    PENDING='pending'
    ACCEPTED='accepted'
    REJECTED='rejected'


class EventVisit(Base):
    __tablename__ = "event_visits"
        
    visit_id: Mapped[int] = mapped_column(Identity(), primary_key=True, index=True)
    event_id: Mapped[int] = mapped_column(Integer(), ForeignKey('event.event_id'), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer(), ForeignKey('users.user_id'), nullable=True)
    status: Mapped[EventVisitStatus] = mapped_column(Enum(EventVisitStatus), nullable=False, default=EventVisitStatus.CREATED)
    deleted: Mapped[bool] = mapped_column(Boolean(), nullable=True, default=False)

    event: Mapped['Event'] = relationship('Event', back_populates='visits', lazy='joined') 
    user: Mapped['User'] = relationship('User', back_populates='event_visits', lazy='joined') 