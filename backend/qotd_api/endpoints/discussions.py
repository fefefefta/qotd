from datetime import date

from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from core.common import _get_comments_for_question, _get_question_for_date
from db import get_session
from dependencies import get_or_create_user, get_user_or_none
from schemas import DiscussionOut, UserOut


discussion_router = APIRouter(
    prefix='/discussion',
    tags=['Discussion'],
)


@discussion_router.get(
    '',
    status_code=status.HTTP_200_OK,
    # response_model=,
    # responses={

    # },
)
async def get_discussion_for_date(
    date: date = date.today(),
    session: AsyncSession = Depends(get_session),
    user: UserOut | None = Depends(get_user_or_none),
) -> DiscussionOut:
    """Returns comments for provided question id."""
    question = await _get_question_for_date(session, date)
    comments = await _get_comments_for_question(session, question.id_, user.id_ if user else None)
    return DiscussionOut(question=question, comments=comments)