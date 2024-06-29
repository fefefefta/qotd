from pydantic import BaseModel, Field


class UserOut(BaseModel):
    id_: str = Field(alias='id')
    username: str
    is_new_user: bool = False