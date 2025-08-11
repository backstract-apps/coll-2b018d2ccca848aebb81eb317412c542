from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, or_
from typing import *
from fastapi import Request, UploadFile, HTTPException
import models, schemas
import boto3
import jwt
import datetime
import requests
import math
import random
import asyncio
from pathlib import Path


async def get_users(db: Session):

    query = db.query(models.Users)

    users_all = query.all()
    users_all = (
        [new_data.to_dict() for new_data in users_all] if users_all else users_all
    )
    res = {
        "users_all": users_all,
    }
    return res


async def get_users_id(db: Session, id: int):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))

    users_one = query.first()

    users_one = (
        (users_one.to_dict() if hasattr(users_one, "to_dict") else vars(users_one))
        if users_one
        else users_one
    )

    res = {
        "users_one": users_one,
    }
    return res


async def post_users(db: Session, raw_data: schemas.PostUsers):
    username: str = raw_data.username
    email: str = raw_data.email
    password_hash: str = raw_data.password_hash

    record_to_be_added = {
        "email": email,
        "username": username,
        "password_hash": password_hash,
    }
    new_users = models.Users(**record_to_be_added)
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    users_inserted_record = new_users.to_dict()

    res = {
        "users_inserted_record": users_inserted_record,
    }
    return res


async def put_users_id(db: Session, raw_data: schemas.PutUsersId):
    id: int = raw_data.id
    username: str = raw_data.username
    email: str = raw_data.email
    password_hash: str = raw_data.password_hash

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))
    users_edited_record = query.first()

    if users_edited_record:
        for key, value in {
            "id": id,
            "email": email,
            "username": username,
            "password_hash": password_hash,
        }.items():
            setattr(users_edited_record, key, value)

        db.commit()
        db.refresh(users_edited_record)

        users_edited_record = (
            users_edited_record.to_dict()
            if hasattr(users_edited_record, "to_dict")
            else vars(users_edited_record)
        )
    res = {
        "users_edited_record": users_edited_record,
    }
    return res


async def delete_users_id(db: Session, id: int):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        users_deleted = record_to_delete.to_dict()
    else:
        users_deleted = record_to_delete
    res = {
        "users_deleted": users_deleted,
    }
    return res


async def post_students(db: Session, raw_data: schemas.PostStudents):
    id: int = raw_data.id
    name: str = raw_data.name

    record_to_be_added = {"id": id, "name": name}
    new_students = models.Students(**record_to_be_added)
    db.add(new_students)
    db.commit()
    db.refresh(new_students)
    add_a_records = new_students.to_dict()

    res = {
        "status": 201,
        "message": "The request was successful and the server responded with the requested resource.",
        "data": {},
    }
    return res


async def get_test(db: Session):

    zccas = aliased(models.Students)
    query = db.query(models.Students, zccas)

    query = query.join(zccas, and_(models.Students.id == zccas.name))

    sfdsagsad = query.all()
    sfdsagsad = (
        [
            {
                "sfdsagsad_1": s1.to_dict() if hasattr(s1, "to_dict") else s1.__dict__,
                "sfdsagsad_2": s2.to_dict() if hasattr(s2, "to_dict") else s2.__dict__,
            }
            for s1, s2 in sfdsagsad
        ]
        if sfdsagsad
        else sfdsagsad
    )
    res = {
        "status": 200,
        "message": "The request was successful and the server responded with the requested resource.",
        "data": {},
    }
    return res


async def post_file_upload(db: Session, file_upload: UploadFile):

    bucket_name = "backstract-testing"
    region_name = "ap-south-1"
    file_path = "resources"

    s3_client = boto3.client(
        "s3",
        aws_access_key_id="AKIATET5D5CPSTHVVX25",
        aws_secret_access_key="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",
        aws_session_token=None,  # Optional, can be removed if not used
        region_name="ap-south-1",
    )

    # Read file content
    file_content = await file_upload.read()

    name = file_upload.filename
    file_path = file_path + "/" + name

    import mimetypes

    file_upload.file.seek(0)

    content_type = mimetypes.guess_type(name)[0] or "application/octet-stream"
    s3_client.upload_fileobj(
        file_upload.file, bucket_name, name, ExtraArgs={"ContentType": content_type}
    )

    file_type = Path(file_upload.filename).suffix
    file_size = 200

    file_url = f"https://{bucket_name}.s3.amazonaws.com/{name}"

    xcvb = file_url
    res = {
        "status": 200,
        "message": "The request was successful and the server responded with the requested resource.",
        "file_upload": {"rfjbknjh": "xcvb"},
    }
    return res
