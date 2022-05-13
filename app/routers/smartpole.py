import re
from fastapi import Depends, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
import calendar
import datetime

router = APIRouter(
    prefix="/smartpole",
    tags=['smartpole'])


@router.post("/smartpole_create", status_code=status.HTTP_201_CREATED, response_model=schemas.smartpole)
async def smartpolecreate(user: schemas.smartpole, db: Session = Depends(get_db)):
    # hast the password - user.password

    #hasdhed_password = utils.hash(user.password)
    #user.password = hasdhed_password

    new_user = models.smartpole(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/get_smartpole')
def get_smartpole(db: Session = Depends(get_db)):
    user = db.query(models.smartpole).all()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found")

    return user


@router.get('/get_smartpole{phone}', response_model=schemas.smartpole)
def get_users(phone: int, db: Session = Depends(get_db)):
    user = db.query(models.smartpole).filter(
        models.smartpole == phone).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with phone: {phone} not found")

    return user


@router.delete("/smartpole_delete", status_code=status.HTTP_204_NO_CONTENT)
async def smartpoledelete(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_admin)):
    post_q = db.query(models.smartpole).filter(models.smartpole.id == id)
    post = post_q.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")
    post_q.delete(synchronize_session=False)
    db.commit()
    return "successfully deleted"


@router.put("/smartpole{phone}", status_code=status.HTTP_202_ACCEPTED)
async def update_smartpole(id: int, user: schemas.smartpole, db: Session = Depends(get_db)):
    bay_q = db.query(models.smartpole).filter(models.smartpole.id == id)
    bay = bay_q.first()

    if id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")

    bay_q.update(user.dict(), synchronize_session=False)
    db.commit()
    return bay_q
