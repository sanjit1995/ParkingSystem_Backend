from fastapi import APIRouter, HTTPException, Depends
from ..db import models, database
from ..db.schemas import parking_schema
from sqlalchemy.orm import Session
from .login import oauth2_scheme
from datetime import datetime
from ..router.token_manager import get_user_id_from_token

parking_router = APIRouter()


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@parking_router.get("/parking/available_slots", tags=["parking"])
async def available_slots(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    parking_slots = db.query(models.ParkingSpots).filter(models.ParkingSpots.is_available).all()
    if not parking_slots:
        return "No Slots Available. Please try again later."
    else:
        return parking_slots

@parking_router.post("/parking/book_start/{spot_id}", tags=["parking"])
async def book_start(parking_slot: parking_schema.ParkingHistoryStart, spot_id: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_parking_slot = db.query(models.ParkingSpots).filter(models.ParkingSpots.spot_id == spot_id).first()
    if db_parking_slot.is_available:
        db_parking_slot.is_available = False
        db.merge(db_parking_slot)

        user_id = token.split("_")[0]
        db_parking_history_start = models.ParkingHistory(parking_id=parking_slot.parking_id,
                                                         spot_id=spot_id,
                                                         user_id=user_id,
                                                         booking_start=datetime.now())
        db.add(db_parking_history_start)
        db.commit()
        db.refresh(db_parking_slot)
        db.refresh(db_parking_history_start)
        return db_parking_history_start
    else:
        return "No Slots Available"

@parking_router.post("/parking/book_end/{parking_id}", tags=["parking"])
async def book_end(parking_slot: parking_schema.ParkingHistoryEnd, parking_id: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_parking_booking = db.query(models.ParkingHistory).filter(models.ParkingHistory.parking_id == parking_id, models.ParkingHistory.user_id == get_user_id_from_token(token)).first()
    if not db_parking_booking:
        return "No such booking available"
    db_booked_spot_id = db_parking_booking.spot_id
    db_parking_slot = db.query(models.ParkingSpots).filter(models.ParkingSpots.spot_id == db_booked_spot_id).first()
    if db_parking_slot.is_available:
        return "Cannot end booking.Slot is not booked yet"
    else:
        db_parking_booking.booking_end = datetime.now()
        db_parking_booking.transaction_id = parking_slot.transaction_id
        db_parking_booking.amount_paid = parking_slot.amount_paid
        db_parking_booking.mode_of_payment = parking_slot.mode_of_payment
        db.merge(db_parking_booking)
        db.commit()
        db.refresh(db_parking_booking)

        db_parking_slot.is_available = True
        db.merge(db_parking_slot)
        db.commit()
        db.refresh(db_parking_slot)

        return "Thanks for using our service. We look forward to serving you again"

@parking_router.post("/parking/get_price", tags=["parking"])
async def calculate_price_for_slot(parking_slot: parking_schema.ParkingPrice, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    parking_id_valid = db.query(models.ParkingHistory).filter(models.ParkingHistory.parking_id == parking_slot.parking_id).first()
    if parking_id_valid:
        if not parking_id_valid.booking_end:
            spot_type_id = db.query(models.ParkingSpots).filter(models.ParkingSpots.spot_id == parking_slot.spot_id).first().parking_type_id
            price_per_hour = db.query(models.ParkingTypes).filter(models.ParkingTypes.type_id == spot_type_id).first().parking_charge
            total_price = ((parking_slot.booking_end - parking_slot.booking_start).total_seconds() / 3600) * price_per_hour
            parking_slot.to_be_paid = total_price
            return parking_slot
        else:
            raise HTTPException(status_code=404, detail="Parking_Id Booking has ended already")
    else:
        raise HTTPException(status_code=404, detail="Parking_Id Mismatch Error")


