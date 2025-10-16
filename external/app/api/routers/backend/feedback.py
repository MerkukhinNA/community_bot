from fastapi import APIRouter

from db.db_manager import db
from db.enum import UserQuestionStatus
from api.shemes import Response, CreateQuestion, Question, FullQuestion, ShortQuestions, Answer


router = APIRouter()

@router.post('/api/v1/question/create', tags=['feedback'], response_model=Response)
async def add_question(data: CreateQuestion):
    try:
        db.add_question(data.user_chat_id, data.text)
        return Response(success=True)

    except Exception as e:
        return Response(success=False, err=f'{e}')
    
@router.post('/api/v1/question/full', tags=['feedback'], response_model=FullQuestion)
async def get_full_question(data: Question):
    try:
        db_question = db.get_question(data.question_id)
        data = FullQuestion.Data(
            text=db_question.text,
            user_chat_id=db_question.user.chat_id,
            date_create=str(db_question.date.strftime("%Y-%m-%d %H:%M:%S")),
            user_name=db_question.user.name + ' ' + db_question.user.last_name,
            user_contact=db_question.user.phone,
            answer=
                'УК еще не ответила' if not db_question.answer 
                else db_question.answer.text,
            date_answer=
                '-' if not db_question.answer 
                else str(db_question.answer.date.strftime("%Y-%m-%d %H:%M:%S"))
        )
        
        return FullQuestion(data=data, success=True)

    except Exception as e:
        return FullQuestion(success=False, err=f'{e}')

@router.post('/api/v1/question/shorts', tags=['feedback'], response_model=ShortQuestions)
async def get_short_questions():
    try:
        questions: list[ShortQuestions.Question] = []
        sorted_db_questions = sorted(db.get_questions(), key=lambda x: list(UserQuestionStatus).index(UserQuestionStatus(x.status)), reverse=False)  # По статусу
        # sorted_db_questions = sorted(db.get_questions(), key=lambda x: x.date, reverse=True). # По дате

        for question in sorted_db_questions:
            questions.append(
                ShortQuestions.Question(
                    question_id=question.question_id,
                    status=question.status,
                    text=question.text[:50],
                    date=str(question.date.strftime("%Y-%m-%d")),
                    user_name=question.user.name + ' ' + question.user.last_name
                )
            )
            
        return ShortQuestions(questions=questions, success=True)

    except Exception as e:
        return ShortQuestions(success=False, err=f'{e}')
    
@router.post('/api/v1/question/answer/create', tags=['feedback'], response_model=Response)
async def add_asnwer(data: Answer):
    try:
        db.add_asnwer(data.user_chat_id, data.question_id, data.text)
        return Response(success=True)

    except Exception as e:
        return Response(success=False, err=f'{e}')