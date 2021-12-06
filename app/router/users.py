import io
import json
from fastapi import APIRouter, HTTPException, Depends, Response
from pydantic import BaseModel
from ..db import models,database
from ..db.schemas import user_schema
from sqlalchemy.orm import Session
from .login import oauth2_scheme
from ..router.token_manager import verify_id_in_token
import qrcode
from fastapi.responses import FileResponse, StreamingResponse

users_router = APIRouter()

class User(BaseModel):
    id: str
    password: str

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@users_router.get("/users/hello", tags=["hello"])
async def read_user_me():
    return {"username":"fake_me"}

@users_router.get("/users/user/{user_id}", tags=["user"])
async def get_user_details(user_id: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if verify_id_in_token(user_id=user_id, token=token):
        return db.query(models.Users).filter(models.Users.user_id == user_id).first()
    else:
        raise HTTPException(status_code=404, detail="User_Id Mismatch Error")

@users_router.get("/users/user/{user_id}/parking_history", tags=["user"])
async def get_user_parking_history(user_id: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if verify_id_in_token(user_id=user_id, token=token):
        user_parking_history = db.query(models.ParkingHistory).filter(models.ParkingHistory.user_id == user_id).all()
        if not user_parking_history:
            return "No Booking History"
        else:
            return user_parking_history
    else:
        raise HTTPException(status_code=404, detail="User_Id Mismatch Error")

@users_router.post("/users/user/{user_id}/edit", tags=["user"])
async def edit_user(orig_user: user_schema.UserBase, user_id: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if verify_id_in_token(user_id=user_id, token=token):
        user = db.query(models.Users).filter(models.Users.user_id == user_id).first()

        user.email = orig_user.email
        user.first_name = orig_user.first_name
        user.last_name = orig_user.last_name
        user.address = orig_user.address
        user.dob = orig_user.dob
        user.contact_number = orig_user.contact_number
        user.gender = orig_user.gender

        db.merge(user)
        db.commit()
        db.refresh(user)

        return "Action Successful"
    else:
        raise HTTPException(status_code=404, detail="User_Id Mismatch Error")

@users_router.post("/users/user/{user_id}/delete", tags=["user"])
async def delete_user(user_id: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if verify_id_in_token(user_id=user_id, token=token):
        user = db.query(models.Users).filter(models.Users.user_id == user_id).first()
        db.delete(user)
        db.commit()

        login = db.query(models.Login).filter(models.Login.id == user_id).first()
        db.delete(login)
        db.commit()

        del oauth2_scheme
        return "Delete action successful"
    else:
        raise HTTPException(status_code=404, detail="User_Id Mismatch Error")

@users_router.get("/users/user/{user_id}/get_qr", tags=["user"])
async def get_qr_code(user_id: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if verify_id_in_token(user_id=user_id, token=token):
        user = db.query(models.Users).filter(models.Users.user_id == user_id).first()
        img = qrcode.make(str(user.get_json()))

        b = io.BytesIO()
        img.save(b, 'jpeg')
        return Response(content=b.getvalue(), media_type="image/jpeg")
    else:
        raise HTTPException(status_code=404, detail="User_Id Mismatch Error")