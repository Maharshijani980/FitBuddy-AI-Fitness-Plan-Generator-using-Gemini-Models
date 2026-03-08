from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

from app.database import create_tables
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):

    # runs when server starts
    create_tables()

    yield

    # runs when server shuts down
    print("Shutting down FitBuddy...")


app = FastAPI(lifespan=lifespan)

app.include_router(router)