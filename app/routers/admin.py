import re
from fastapi import Depends, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
import calendar
import datetime

router = APIRouter(
    prefix="/admin",
    tags=['Admin'])


@router.post("/admin_create", status_code=status.HTTP_201_CREATED, response_model=schemas.admin)
async def acreate(user: schemas.admin, db: Session = Depends(get_db)):
    # hast the password - user.password

    hasdhed_password = utils.hash(user.password)
    user.password = hasdhed_password

    new_user = models.admin(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/get_admins')
def get_admins(db: Session = Depends(get_db)):
    user = db.query(models.admin).all()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"admin not found")

    return user


@router.get('/get_admin{phone}', response_model=schemas.admin)
def get_admins(phone: int, db: Session = Depends(get_db)):
    user = db.query(models.admin).filter(
        models.admin.phone == phone).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"admin with phone: {phone} not found")

    return user


@router.delete("/admin_delete", status_code=status.HTTP_204_NO_CONTENT)
async def adelete(phone: int, db: Session = Depends(get_db)):
    post_q = db.query(models.admin).filter(models.admin.phone == phone)
    post = post_q.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")
    post_q.delete(synchronize_session=False)
    db.commit()
    return "successfully deleted"


@router.put("/admin{phone}", status_code=status.HTTP_202_ACCEPTED)
async def update_admin(phone: int, user: schemas.admin, db: Session = Depends(get_db)):
    bay_q = db.query(models.admin).filter(models.admin.phone == phone)
    bay = bay_q.first()

    if phone == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")

    bay_q.update(user.dict(), synchronize_session=False)
    db.commit()
    return bay_q
