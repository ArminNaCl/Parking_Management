from fastapi import FastAPI, Depends

from src.auth.views import auth_api
from src.admin.views import admin_router
from src.routers.views import app_router
from src.config import oauth2_scheme
from src.auth.service import get_current_superuser

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
api.include_router(admin_router, prefix="/admin", tags=["Admin"],dependencies=[Depends(get_current_superuser),])
api.include_router(app_router, prefix="", tags=["App"],dependencies=[Depends(oauth2_scheme),])

app.mount("/api/v1/", app=api)
