from typing import Union, Annotated
from pydantic import BaseModel

from fastapi import FastAPI, Query, Depends


from src.auth.views import auth_api, user_api
from src.config import oauth2_scheme
from src.record.views import record_api
app = FastAPI()



api = FastAPI(
    title="Armin",
    description="Welcome to Armin's API documentation! Here you will able to discover all of the ways you can interact with the Dispatch API.",
    root_path="/api/v1",
    openapi_url="/docs/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)






api.include_router(auth_api, prefix="", tags=["Auth"])
api.include_router(user_api, prefix="/users", tags=["User"],dependencies=[Depends(oauth2_scheme),])
api.include_router(record_api, prefix="/records", tags=["Record"],dependencies=[Depends(oauth2_scheme),])

app.mount("/api/v1/", app=api)
