import pytest
import sys
print(sys.path)
import asyncpg
from httpx import AsyncClient
from fastapi import status
# from utils.common.hostname import get_app
from app import get_app
from schemas import CommentOut, DiscussionOut, QuestionOut
from config.utils import get_settings

@pytest.mark.asyncio
async def test_get_discussion():
    async with AsyncClient(app=get_app(), base_url="http://test") as ac:
        response = await ac.get("/api/v1/discussion")
    assert response.status_code == status.HTTP_200_OK
    assert "user_id" in response.cookies
    discussion = DiscussionOut(**response.json())
    assert isinstance(discussion, DiscussionOut)


# @pytest.mark.asyncio
# async def test_get_question():
#     async with AsyncClient(app=get_app(), base_url="http://test") as ac:
#         response = await ac.get("/api/v1/question")
#     assert response.status_code == status.HTTP_200_OK
#     question = QuestionOut(**response.json())
#     assert isinstance(question, QuestionOut)


@pytest.mark.asyncio
async def test_get_comments():
    async with AsyncClient(app=get_app(), base_url="http://test") as ac:
        response = await ac.get("/api/v1/comment/1/")
    assert response.status_code == status.HTTP_200_OK
    assert "user_id" in response.cookies
    comments = [CommentOut(**comment) for comment in response.json()]
    assert isinstance(comments, CommentOut)


DATABASE_URL = get_settings().database_uri

@pytest.mark.asyncio
async def test_post_comment():
    async with AsyncClient(app=get_app(), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/comment",
            json={"text": "Test comment", "question_id": 1, "parent_id": None},
            cookies={"user_id": "test_user_id"}
        )
    assert response.status_code == status.HTTP_201_CREATED
    comment = CommentOut(**response.json())
    assert isinstance(comment, CommentOut)

    # Проверяем, что комментарий добавлен в базу данных
    conn = await asyncpg.connect(DATABASE_URL)
    result = await conn.fetchrow("SELECT * FROM Comment WHERE id = $1", comment.id)
    assert result is not None
    assert result["text"] == "Test comment"
    await conn.close()