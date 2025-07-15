from fastapi import FastAPI
from src.api import chat

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request



app = FastAPI()
app.include_router(chat.router, prefix="/api")


app.mount("/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
