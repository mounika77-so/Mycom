#from msilib import schema
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl='slogin')
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl='ulogin')


SECRET_KEY_ADMIN = settings.secret_key_admin
SECRET_KEY_SUBADMIN = settings.secret_key_subadmin
SECRET_KEY_USER = settings.secret_key_user
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token_admin(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_ADMIN, algorithm=ALGORITHM)

    return encoded_jwt


def create_access_token_subadmin(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY_SUBADMIN, algorithm=ALGORITHM)

    return encoded_jwt


def create_access_token_user(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_USER, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token_admin(token: str, Credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY_ADMIN, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise Credentials_exception

        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise Credentials_exception

    return token_data


def verify_access_token_subadmin(token: str, Credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY_SUBADMIN,
                             algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise Credentials_exception

        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise Credentials_exception

    return token_data


def verify_access_token_user(token: str, Credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY_USER, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise Credentials_exception

        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise Credentials_exception

    return token_data


def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    Credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate ",
        headers={"www-Authenticate": "Bearer"})
    token = verify_access_token_admin(token, Credentials_exception)
    user = db.query(models.admin).filter(models.admin.id == token.id).first()

    return user


def get_current_subadmin(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    Credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate ",
        headers={"www-Authenticate": "Bearer"})
    token = verify_access_token_subadmin(token, Credentials_exception)
    user = db.query(models.subadmin).filter(
        models.subadmin.id == token.id).first()

    return user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    Credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate ",
        headers={"www-Authenticate": "Bearer"})
    token = verify_access_token_user(token, Credentials_exception)
    user = db.query(models.user).filter(models.user.id == token.id).first()

    return user
