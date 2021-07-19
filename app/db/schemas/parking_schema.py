from datetime import datetime
from pydantic import BaseModel

class ParkingSpots(BaseModel):
    spot_id: str
    parking_type_id: str
    city: str
    address: str
    location: str
    is_functional: bool
    is_available: bool

class ParkingTypes(BaseModel):
    parking_type_id: str
    description: str
    charge: float

class ParkingHistoryStart(BaseModel):
    parking_id: str
    booking_start: datetime

class ParkingHistoryEnd(BaseModel):
    booking_end: datetime
    transaction_id: str
    amount_paid: float
    mode_of_payment: int

class ParkingPrice(ParkingHistoryStart):
    booking_end: datetime
    spot_id: str
    to_be_paid: str