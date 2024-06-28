from datetime import date

from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from core.common import _get_question_for_date
from db import get_session
from schemas.question import QuestionOut


questions_router = APIRouter(
    prefix='/question',
    tags=['Question'],
)


@questions_router.get(
    '',
    status_code=status.HTTP_200_OK,
    # response_model=,
    # responses={

    # },
)
async def get_question_for_date(
    date: date = date.today(),
    session: AsyncSession = Depends(get_session)
) -> QuestionOut:
    """Returns question for provided date."""
    question = await _get_question_for_date(session, date)
    return question