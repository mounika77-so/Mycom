from logging import exception
from sqlite3 import Cursor
from typing import Optional
from fastapi import Depends, FastAPI, Response, status, HTTPException, Request
from fastapi.params import Body
from pydantic import BaseModel, BaseSettings
from random import randrange

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi.middleware.cors import CORSMiddleware

from typing import Optional, List

import time
from sqlalchemy.orm import Session


from . import models
from . import schemas, utils
from .database import engine, get_db
from . routers import admin, auth, device, user, smartclass, smartpole
from .config import settings


import schedule
import time


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(device.router)
app.include_router(smartpole.router)
app.include_router(smartclass.router)


# app.include_router(vote.router)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")


templates = Jinja2Templates(directory="pages")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/smartpole", response_class=HTMLResponse)
async def read_item(request: Request, db: Session = Depends(get_db)):
    user = db.query(models.smartpole).first()
    smartpole = schemas.smartpole(polename=user.polename, Temperature=user.Temperature,
                                  Humidity=user.Humidity, Air_quality=user.Air_quality, Co2_emission=user.Co2_emission)
    return templates.TemplateResponse("smartpole.html", {"request": request, "smartpole": smartpole})


@app.get("/smartclass", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("smart-home.html", {"request": request})
