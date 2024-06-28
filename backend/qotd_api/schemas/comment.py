from datetime import datetime

from pydantic import BaseModel, Field


class CommentIn(BaseModel):
    text: str
    username: str | None = None

    question_id: int
    parent_id: int | None = None


class CommentOut(CommentIn):
    id_: int = Field(alias='id')

    upvotes: int
    voted: bool
    pub_ts: int | datetime
    children: list['CommentOut'] | None = []
