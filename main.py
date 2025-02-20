from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.endpoints.respondents import respondent_router
from app.db.database import init_db, load_initial_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await load_initial_data()
    yield

app = FastAPI(lifespan=lifespan, title="Respondent API")

app.include_router(respondent_router)
