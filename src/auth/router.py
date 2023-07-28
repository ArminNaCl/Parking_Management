from typing import Union

from fastapi import APIRouter

from src.auth.models import Item

auth_router = APIRouter()


@auth_router.get("/me")
async def read_user_me():
    return {"user_id": "the current user"}


@auth_router.get("/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
