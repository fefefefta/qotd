import json
from typing import Annotated

from fastapi import Depends, Request, Response, Cookie, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.common import get_user_or_none as _get_user_or_none, create_user
from db import get_session
from schemas import UserOut


async def get_or_create_user(
    response: Response,
    session: AsyncSession = Depends(get_session),
    current_user: Annotated[str | None, Cookie()] = None,
) -> UserOut:
    if current_user:
        user = UserOut(**json.loads(current_user.replace("|", ",")))
        user = await _get_user_or_none(session, user.id_)
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        current_user = await create_user(session)
        print(current_user.model_dump_json(by_alias=True).replace(",", "|"))
        response.set_cookie(
            key="current_user",
            value=current_user.model_dump_json(by_alias=True).replace(",", "|"),
            domain=".onrender.com",
            secure=True,
            samesite="none",
            httponly=False,
        )
        return current_user


async def get_user_or_none(
    response: Response,
    session: AsyncSession = Depends(get_session),
    current_user: Annotated[str | None, Cookie()] = None,
) -> UserOut:
    if current_user:
        user = UserOut(**json.loads(current_user.replace("|", ",")))
        user = await _get_user_or_none(session, user.id_)
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
