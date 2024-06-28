from pydantic import BaseModel, Field


class QuestionOut(BaseModel):
    id_: int = Field(alias='id')

    title: str
    text: str

    date: str