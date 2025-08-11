from pydantic import BaseModel,Field,field_validator

import datetime

import uuid

from typing import Any, Dict, List,Optional,Tuple

import re

class Users(BaseModel):
    username: Optional[str]=None
    email: Optional[str]=None
    password_hash: Optional[str]=None


class ReadUsers(BaseModel):
    username: Optional[str]=None
    email: Optional[str]=None
    password_hash: Optional[str]=None
    class Config:
        from_attributes = True


class Students(BaseModel):
    name: Optional[str]=None


class ReadStudents(BaseModel):
    name: Optional[str]=None
    class Config:
        from_attributes = True


class Name(BaseModel):
    pass


class ReadName(BaseModel):
    class Config:
        from_attributes = True




class PostUsers(BaseModel):
    username: Optional[str]=None
    email: Optional[str]=None
    password_hash: Optional[str]=None

    class Config:
        from_attributes = True



class PutUsersId(BaseModel):
    id: Optional[int]=None
    username: Optional[str]=None
    email: Optional[str]=None
    password_hash: Optional[str]=None

    class Config:
        from_attributes = True



class PostStudents(BaseModel):
    id: int = Field(...)
    name: str = Field(..., max_length=100)

    class Config:
        from_attributes = True

