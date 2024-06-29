from pydantic import BaseModel, Field


class VoteIn(BaseModel):
    comment_id: int


class VoteOut(BaseModel):
    id_: int = Field(alias='id')
    comment_id: int
    user_id: str
    username: str | None = None

    vote_type: bool
    is_new_user: bool = False