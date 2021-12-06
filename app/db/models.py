from sqlalchemy import Boolean, Column, ForeignKey, String, DATE, DECIMAL, CHAR, DATETIME,Float,Integer
from sqlalchemy.orm import relationship

from .database import Base

class Users(Base):
    __tablename__ = "users"

    user_id = Column(String,ForeignKey("login.id"), primary_key=True, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    dob = Column(DATE)
    contact_number = Column(DECIMAL)
    gender = Column(CHAR)

    def get_json(self):
        return {'user_id': self.user_id, 'email': self.email, 'dob': self.dob}

class Login(Base):
    __tablename__ = "login"

    id = Column(String, primary_key=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

class ParkingSpots(Base):
    __tablename__ = "parking_spots"

    spot_id = Column(String, primary_key=True, index=True)
    parking_type_id = Column(String, index=True)
    city = Column(String,index=True)
    address = Column(String)
    location = Column(String)
    is_available = Column(Boolean)
    is_functional = Column(Boolean)

class ParkingHistory(Base):
    __tablename__ = "parking_history"

    parking_id = Column(String, primary_key=True, index=True)
    spot_id = Column(String, index=True)
    user_id = Column(String, index=True)
    booking_start = Column(DATETIME)
    booking_end = Column(DATETIME)
    transaction_id = Column(String)
    amount_paid = Column(Float)
    mode_of_payment = Column(Integer)

class ParkingTypes(Base):
    __tablename__ = "parking_types"

    type_id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    parking_charge = Column(Boolean)
