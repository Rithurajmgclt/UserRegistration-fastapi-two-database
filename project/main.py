from fastapi import FastAPI
from users.routers import user_router
from users.database import initialize_database
from starlette.staticfiles import StaticFiles
from dotenv import load_dotenv
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router)

initialize_database()