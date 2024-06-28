from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from core.common import check_user_voted, vote_comment, unvote_comment
from db import get_session
from dependencies.user import get_or_create_user
from schemas.vote import VoteOut, VoteIn
from schemas.user import UserOut


votes_router = APIRouter(
    prefix='/votes',
    tags=['Vote'],
)


@votes_router.post(
    '',
    status_code=status.HTTP_200_OK,
)
async def upvote_comment(
    vote: VoteIn,
    user: Annotated[UserOut, Depends(get_or_create_user)],
    session: AsyncSession = Depends(get_session)
) -> VoteOut:
    if not await check_user_voted(session, user.id_, vote.comment_id):
        vote = await vote_comment(session, user.id_, vote.comment_id)
    else:
        vote = await unvote_comment(session, user.id_, vote.comment_id)
    await session.commit()
    return vote