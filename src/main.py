from typing import Union, Annotated
from pydantic import BaseModel

from fastapi import FastAPI, Query, Depends


from src.auth.router import auth_router
from src.auth.views import auth_model_api
from src.config import oauth2_scheme

app = FastAPI()



api = FastAPI(
    title="Armin",
    description="Welcome to Armin's API documentation! Here you will able to discover all of the ways you can interact with the Dispatch API.",
    root_path="/api/v1",
    openapi_url="/docs/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    dependencies= [Depends(oauth2_scheme),],
)


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: Union[float, None] = None


# @api.get("/")
# async def read_root():
#     return {"Hello": "World"}


@api.get("/items/{item_id}")
async def read_item(
    token: Annotated[str, Depends(oauth2_scheme)],
    item_id: int,
    tax: Annotated[float | None, Query(ge=0, le=1)] = ...,
    names : Annotated[list, Query()] = [],
    full: Annotated[str|None, Query(title="title", alias="full_query", description="some words", regex="")] =  None ,
    q: Annotated[str | None, Query(max_length=50)] = None,
):
    return {"item_id": item_id, "q": q, "tax": tax}


@api.post("/items/")
async def create_item(item: Item):
    return item


@api.put("/item/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_name": item.name, "item_id": item_id}
    if q:
        result.update({"q": q})
    return result


# api.include_router(auth_router, prefix="/users", tags=["users"])
api.include_router(auth_model_api, prefix="/users", tags=["users2"])

app.mount("/api/v1/", app=api)
