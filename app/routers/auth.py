from typing import Dict
from urllib import response
from fastapi import Depends, FastAPI, Response, status, HTTPException, Depends, APIRouter, Request, Form
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2
from fastapi.responses import HTMLResponse, RedirectResponse

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_login import LoginManager
from ..config import settings
from datetime import timedelta
from ..database import get_db
#from ..main import app

# router.mount("/assets", StaticFiles(directory="assets"), name="assets")


templates = Jinja2Templates(directory="pages")

router = APIRouter(tags=["Authentication"])

manager = LoginManager(
    secret=settings.secret_key_admin, token_url="/login", use_cookie=True)
manager.cookie_name = "auth"


@manager.user_loader()
async def get_user_data(email: str):
    return email


@router.get("/login", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("sign-in.html", {"request": request})


@router.post('/login')
async def login(request: Request, user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.user).filter(
        models.user.email == user_cred.username).first()

    if not user:
        return templates.TemplateResponse(
            "sign-in.html", {"request": request, "invalid": True}, status_code=status.HTTP_401_UNAUTHORIZED)

    if not utils.verify(user_cred.password, user.password):
        return templates.TemplateResponse(
            "sign-in.html", {"request": request, "invalid": True}, status_code=status.HTTP_401_UNAUTHORIZED)

    # access_token = oauth2.create_access_token_subadmin(
    #     data={"user_id": user.id})
    # return {"access_token": access_token, "token_type": "Bearer"}
    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)
    access_token = manager.create_access_token(
        data={"sub": user_cred.username},
        expires=access_token_expires
    )
    token = str(access_token)
    # print(access_token)
    # print(token[2:-1])
    resp = RedirectResponse("/user/profile", status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp, token[2:-1])
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    return resp


@ router.post('/slogin', response_model=schemas.Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.subadmin).filter(
        models.subadmin.phone == user_cred.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid")

    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="wrong password")

    access_token = oauth2.create_access_token_subadmin(
        data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "Bearer"}


@ router.post('/ulogin', response_model=schemas.Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.user).filter(
        models.user.phone == user_cred.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid")

    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="wrong password")

    access_token = oauth2.create_access_token_user(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "Bearer"}
