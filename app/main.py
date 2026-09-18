from contextlib import asynccontextmanager
from app.database.connection import Base, engine
from app.models.user_model import User

from fastapi import FastAPI, Request

from app.config import settings
from app.routes.user_routes import user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    lifespan=lifespan,
    title=f"{settings.APP_NAME} API",
    description="API REST para la gestión de usuarios del sistema device_systems",
    version=settings.APP_VERSION,
    contact={"name": "Samir Acosta Peña"},
    openapi_tags=[{"name": "Users", "description": "CRUD de usuarios persistidos en SQLite"}],
)


@app.middleware("http")
async def add_app_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = settings.APP_NAME
    response.headers["X-API-Version"] = settings.APP_VERSION
    return response


@app.get("/", summary="Consultar información de la API",
         description="Muestra el nombre, la versión y el acceso a Swagger.",
         response_description="Información de device_systems")
def root():
    return {"app": settings.APP_NAME, "version": settings.APP_VERSION, "docs": "/docs"}


app.include_router(user_router)
