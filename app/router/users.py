from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..db import models,database
from ..db.schemas import user_schema
from sqlalchemy.orm import Session
from .login import oauth2_scheme
from ..router.token_manager import verify_id_in_token

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
async def get_user_history(user_id: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if verify_id_in_token(user_id=user_id, token=token):
        user_parking_history = db.query(models.ParkingHistory).filter(models.ParkingHistory.user_id == user_id).all()
        if not user_parking_history:
            return "No Booking History"
        else:
            return user_parking_history
    else:
        raise HTTPException(status_code=404, detail="User_Id Mismatch Error")