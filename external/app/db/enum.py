from enum import Enum as PyEnum


class EventVisitStatus(PyEnum):
    CREATED='created'
    PENDING='pending'
    ACCEPTED='accepted'
    REJECTED='rejected'


class UserQuestionStatus(PyEnum):
    CREATED='created'
    ANSWERED='answered'