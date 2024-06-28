from pydantic import BaseModel, Field

from .comment import CommentOut
from .question import QuestionOut


class DiscussionOut(BaseModel):
    question: QuestionOut
    comments: list[CommentOut]
