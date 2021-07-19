from fastapi import APIRouter, Depends, HTTPException
from ..db import models,database
from ..db.schemas import login_schema
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..router.token_manager import generate_token

login_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@login_router.post("/login", tags=["login"])
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user_logged = db.query(models.Login).filter(models.Login.id == form_data.username, models.Login.password == form_data.password).first()
    if user_logged is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user_logged.is_active:
        raise HTTPException(status_code=401, detail="User not active")
    else:
        return {"access_token": generate_token(user_id=form_data.username, password=form_data.password)}


@login_router.post("/signup", tags=["signup"])
async def signup(user: login_schema.Signup, db: Session = Depends(get_db)):
    db_login = models.Login(id=user.id, password=user.password, is_active=True)
    db.add(db_login)
    db.commit()
    db.refresh(db_login)

    db_signup = models.Users(user_id=user.id, email=user.email, first_name=user.first_name,
                            last_name=user.last_name, address=user.address, dob=user.dob,
                            contact_number=user.contact_number, gender=user.gender)
    db.add(db_signup)
    db.commit()
    db.refresh(db_signup)
    return "User Created"