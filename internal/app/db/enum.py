from enum import Enum as PyEnum


class VisitStatus(PyEnum):
    CREATED='created'
    PENDING='pending'
    ACCEPTED='accepted'
    REJECTED='rejected'


class FeedbackStatus(PyEnum):
    CREATED='created'
    ANSWERED='answered'