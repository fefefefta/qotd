from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from core.common import _get_comments_for_question, _create_comment
from dependencies import get_or_create_user
from db import get_session
from schemas import CommentIn, CommentOut, UserOut


comments_router = APIRouter(
    prefix='/comment',
    tags=['Comment'],
)


@comments_router.get(
    '/{question_id}',
    status_code=status.HTTP_200_OK,
)
async def get_comments_for_question(
    question_id: int,
    session: AsyncSession = Depends(get_session),
    user: UserOut = Depends(get_or_create_user),
) -> list[CommentOut]:
    """Returns comments for provided question id."""
    comments = await _get_comments_for_question(session, question_id, user.id_)
    return comments

@comments_router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
)
async def create(
    _: Request,
    comment: CommentIn,
    user: UserOut = Depends(get_or_create_user),
    session: AsyncSession = Depends(get_session),
) -> CommentOut:
    """Creates new comment."""
    new_comment_data = CommentIn(**comment.model_dump(by_alias=True))
    new_comment = await _create_comment(session, user, new_comment_data)
    new_comment.is_new_user = user.is_new_user
    return new_comment


