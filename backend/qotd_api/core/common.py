from datetime import date
import random
import uuid

from fastapi import HTTPException
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession

from db import querys
from schemas import QuestionOut, CommentOut, CommentIn, DiscussionOut, UserOut, VoteOut
from utils.username_generation import create_username


async def _create_comment(session: AsyncSession, user: UserOut, comment: CommentIn) -> CommentOut:
    """Creates new comment."""
    row = await querys.create_comment(
        session,
        user_id=user.id_,
        question_id=comment.question_id,
        parent_id=comment.parent_id,
        comment_text=comment.text)
    await session.commit()
    return CommentOut(**row._asdict())


# async def get_discussion_today(session: AsyncSession) -> Discussion:
#     """Returns today's discussion."""
#     pass


# async def _get_discussion_for_date(session: AsyncSession, date: date) -> Discussion:
#     """Takes in date, returns discussion for this date."""
#     pass


async def _get_question_for_date(session: AsyncSession, date: date) -> QuestionOut:
    """Takes in date, returns question for this date."""
    row: Row | None = await querys.get_question_for_date(session, date)
    if not row:
        raise HTTPException(status_code=404, detail="Question not found")
    return QuestionOut(**row._asdict(), date=date.isoformat())


async def _get_comments_for_question(session: AsyncSession, question_id: int, user_id: str | None = None) -> list[CommentOut]:
    """Takes in question, returns tree os comments for this date."""
    rows: list[Row] | None = await querys.get_comments_for_question(session, question_id, user_id)
    if not rows:
        # raise HTTPException(status_code=404, detail="Comments not found")
        return []

    comments = [row._asdict() for row in rows]
    comment_dict = {comment['id']: CommentOut(**comment) for comment in comments}
    root_comments = []

    for comment in comments:
        if comment['parent_id'] is None:
            root_comments.append(comment_dict[comment['id']])
        else:
            parent_comment = comment_dict[comment['parent_id']]
            parent_comment.children.append(comment_dict[comment['id']])

    return root_comments


async def get_user_or_none(session: AsyncSession, user_id: str) -> UserOut | None:
    user = await querys.get_user(session, user_id)
    if not user:
        return None
    return UserOut(**user._asdict())


async def create_user(session: AsyncSession) -> UserOut:
    user_id = uuid.uuid4().hex
    username = create_username()

    user = await querys.create_user(session, user_id, username)
    await session.commit()
    user = UserOut(**user._asdict())
    return user


async def check_user_voted(session: AsyncSession, user_id: str, comment_id: int) -> bool:
    vote = await querys.check_user_voted(session, user_id, comment_id)
    return bool(vote)


async def vote_comment(session: AsyncSession, user_id: str, comment_id: int) -> VoteOut:
    vote = await querys.vote_comment(session, user_id, comment_id)
    return vote


async def unvote_comment(session: AsyncSession, user_id: str, comment_id: int) -> VoteOut:
    unvote = await querys.unvote_comment(session, user_id, comment_id)
    return unvote



# async def upvote_comment(session: AsyncSession, comment: Comment):
#     pass


# async def downvote_comment(session: AsyncSession, comment: Comment):
#     pass
