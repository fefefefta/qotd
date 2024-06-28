import datetime

from sqlalchemy import text
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession

from .sql import (
    GET_QUESTION_FOR_DATE,
    GET_COMMENTS_FOR_QUESTION, CREATE_COMMENT,
    CREATE_USER, GET_USER,
    CHECK_USER_VOTED, VOTE_COMMENT, UNVOTE_COMMENT,
)


async def get_question_for_date(session: AsyncSession, date: datetime.date) -> Row | None:
    result = await session.execute(text(GET_QUESTION_FOR_DATE), {'date': date})
    return result.one_or_none()


async def get_comments_for_question(session: AsyncSession, question_id: int, user_id: str | None = None) -> list[Row]:
    result = await session.execute(text(GET_COMMENTS_FOR_QUESTION), {'question_id': question_id, 'user_id': user_id})
    return result.all()


async def create_user(session: AsyncSession, user_id, username) -> Row:
    result = await session.execute(text(CREATE_USER), {'user_id': user_id, 'username': username})
    return result.one()


async def get_user(session: AsyncSession, user_id) -> Row | None:
    result = await session.execute(text(GET_USER), {'user_id': user_id})
    return result.one_or_none()


async def check_user_voted(session: AsyncSession, user_id, comment_id) -> bool:
    result = await session.execute(text(CHECK_USER_VOTED), {'user_id': user_id, 'comment_id': comment_id})
    return result.scalar()

async def vote_comment(session: AsyncSession, user_id, comment_id) -> Row:
    result = await session.execute(text(VOTE_COMMENT), {'user_id': user_id, 'comment_id': comment_id})
    return result.one()

async def unvote_comment(session: AsyncSession, user_id, comment_id) -> Row:
    result = await session.execute(text(UNVOTE_COMMENT), {'user_id': user_id, 'comment_id': comment_id})
    return result.one()


async def create_comment(session: AsyncSession, user_id: str, question_id: int, parent_id: int, comment_text: str) -> Row:
    result = await session.execute(text(CREATE_COMMENT), {'user_id': user_id, 'question_id': question_id, 'parent_id': parent_id, 'text': comment_text})
    return result.one()