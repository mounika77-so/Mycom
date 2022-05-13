from fastapi import Depends, FastAPI, Response, status, HTTPException, Depends, APIRouter, Request, Form
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2
from fastapi.responses import HTMLResponse, RedirectResponse
from ..database import get_db
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .auth import manager

# router.mount("/assets", StaticFiles(directory="assets"), name="assets")


templates = Jinja2Templates(directory="pages")


router = APIRouter(
    prefix="/user",
    tags=['User'])


@router.get("/create", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("sign-up.html", {"request": request})


@router.post('/create')
async def login(name=Form(...), email=Form(...), phone=Form(...), password=Form(...), db: Session = Depends(database.get_db)):
    # print(name)
    # print(username)
    # print(phone)
    # print(password)
    hasdhed_password = utils.hash(password)

    test_keys = ['name', 'email', 'phone', 'password']
    res = dict(zip(test_keys, [name, email, phone, hasdhed_password]))
    print(res)
    new_user = models.user(**res)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/profile")
def home(request: Request, email=Depends(manager), db: Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.email == email).first()
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})


@router.get('/get_users')
def get_users(db: Session = Depends(get_db)):
    user = db.query(models.user).all()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found")

    return user


@router.get('/get_user{phone}', response_model=schemas.user)
def get_users(phone: int, db: Session = Depends(get_db)):
    user = db.query(models.user).filter(
        models.admin.phone == phone).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with phone: {phone} not found")

    return user


@router.delete("/user_delete", status_code=status.HTTP_204_NO_CONTENT)
async def udelete(phone: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_admin)):
    post_q = db.query(models.user).filter(models.user.phone == phone)
    post = post_q.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")
    post_q.delete(synchronize_session=False)
    db.commit()
    return "successfully deleted"


@router.put("/admin{phone}", status_code=status.HTTP_202_ACCEPTED)
async def update_admin(phone: int, user: schemas.admin, db: Session = Depends(get_db)):
    bay_q = db.query(models.user).filter(models.user.phone == phone)
    bay = bay_q.first()

    if phone == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")

    bay_q.update(user.dict(), synchronize_session=False)
    db.commit()
