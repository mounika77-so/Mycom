import re
from fastapi import Depends, FastAPI, Response, status, HTTPException, Depends, APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
import calendar
import datetime
from fastapi.templating import Jinja2Templates
from typing import Optional
templates = Jinja2Templates(directory="pages")
router = APIRouter(
    prefix="/smartclass",
    tags=['smartclass'])


@router.get("/control")
async def acreate(request: Request,  db: Session = Depends(get_db)):
    user = db.query(models.smartpole).first()
    smartpole = schemas.smartpole(polename=user.polename, Temperature=user.Temperature,
                                  Humidity=user.Humidity, Air_quality=user.Air_quality, Co2_emission=user.Co2_emission)

    list1 = ["class1", "class2", "class3", "class4", "class5", "class6", "class7",
             "class8", "class9", "class10", "class11", "class12", "class13", "class14"]
    list2 = []
    list3 = []
    for i in list1:
        class1 = db.query(models.smartclass).filter(
            models.smartclass.classroom == i).first()
        list2.append(class1.Switchstatus)
        list3.append(class1.power_consumption)

    power_consumption = schemas.power_consumption(
        class1=list3[0],
        class2=list3[1],
        class3=list3[2],
        class4=list3[3],
        class5=list3[4],
        class6=list3[5],
        class7=list3[6],
        class8=list3[7],
        class9=list3[8],
        class10=list3[9],
        class11=list3[10],
        class12=list3[11],
        class13=list3[12],
        class14=list3[13])

    Switchstatus = schemas.switches(
        class1=list2[0],
        class2=list2[1],
        class3=list2[2],
        class4=list2[3],
        class5=list2[4],
        class6=list2[5],
        class7=list2[6],
        class8=list2[7],
        class9=list2[8],
        class10=list2[9],
        class11=list2[10],
        class12=list2[11],
        class13=list2[12],
        class14=list2[13])

    return templates.TemplateResponse(
        "smart-home.html", {"request": request, "status": Switchstatus, "p": power_consumption, "smartpole": smartpole}, status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/control")
async def acreate(request: Request, classstatus: Optional[str] = Form(False), classroom=Form(...), db: Session = Depends(get_db)):
    # print(classroom)
    classupdate = db.query(models.smartclass).filter(
        models.smartclass.classroom == classroom).first()
    # print(classstatus)
    classupdate.Switchstatus = bool(classstatus)
    db.add(classupdate)
    db.commit()
    db.refresh(classupdate)
    return RedirectResponse("/smartclass/control", status_code=status.HTTP_302_FOUND)


@router.post("/smartclass_create", status_code=status.HTTP_201_CREATED)
async def acreate(user: schemas.smartclass, db: Session = Depends(get_db)):
    # hast the password - user.password

    #hasdhed_password = utils.hash(user.password)
    #user.password = hasdhed_password

    new_user = models.smartclass(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/get_smartclass')
def get_smartclass(db: Session = Depends(get_db)):
    user = db.query(models.smartclass).all()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found")

    return user


@router.get('/get_smartclass{phone}', response_model=schemas.smartclass)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.smartclass).filter(
        models.smartclass.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"smartclass with id: {id} not found")

    return user


@router.delete("/smartclass_delete", status_code=status.HTTP_204_NO_CONTENT)
async def smart_classdelete(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_admin)):
    post_q = db.query(models.user).filter(models.smartclass.id == id)
    post = post_q.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")
    post_q.delete(synchronize_session=False)
    db.commit()
    return "successfully deleted"


@router.put("/smartclass{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_smartclass(id: int, user: schemas.smartclass, db: Session = Depends(get_db)):
    bay_q = db.query(models.smartclass).filter(models.smartclass.id == id)
    bay = bay_q.first()

    if id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")

    bay_q.update(user.dict(), synchronize_session=False)
    db.commit()
    return bay_q
