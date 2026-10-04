from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database.database import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, DateTime, Date, Float, Text, ForeignKey
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False, index=True)

    password_hash = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Aircraft(Base):
    __tablename__ = "aircraft"

    aircraft_id = Column(Integer, primary_key=True, index=True)

    registration = Column(String, nullable=False)

    manufacturer = Column(String, nullable=False)

    model = Column(String, nullable=False)

    aircraft_type = Column(String, nullable=False)

    engine_type = Column(String, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)


class Flight(Base):
    __tablename__ = "flights"

    flight_id = Column(Integer, primary_key=True, index=True)

    owner_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    aircraft_id = Column(Integer, ForeignKey("aircraft.aircraft_id"), nullable=False)

    flight_date = Column(Date, nullable=False)

    departure_airport = Column(String, nullable=False)

    arrival_airport = Column(String, nullable=False)

    flight_time = Column(Float, nullable=False)

    landings = Column(Integer, nullable=False)

    day_night = Column(String, nullable=False)

    remarks = Column(Text)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
