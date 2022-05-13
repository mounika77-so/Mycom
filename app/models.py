from sqlite3 import Timestamp
import string
from typing import Text
from sqlalchemy import Boolean, Column, Date, Integer, String, Time, column, ForeignKey, BigInteger, Float
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base


class admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    name = Column(String,  nullable=False)
    phone = Column(BigInteger, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


class user(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String,  nullable=False, unique=True)
    name = Column(String,  nullable=False)
    phone = Column(BigInteger, nullable=False)
    password = Column(String, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


class smartclass(Base):
    __tablename__ = "smartclass"
    id = Column(Integer, primary_key=True, nullable=False)
    classroom = Column(String,  nullable=False)
    power_consumption = Column(Float, nullable=False)
    Switchstatus = Column(Boolean,  nullable=False, server_default="False")
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


class smartpole(Base):
    __tablename__ = "smartpole"
    id = Column(Integer, primary_key=True, nullable=False)
    polename = Column(String,  nullable=False)
    Temperature = Column(Float, nullable=False)
    Humidity = Column(Float, nullable=False)
    Air_quality = Column(Float, nullable=False)
    Co2_emission = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


class device(Base):
    __tablename__ = "Devices"
    id = Column(Integer, primary_key=True, nullable=False)
    chip_id = Column(Integer, nullable=False)
    mac_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
