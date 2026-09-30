from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database.database import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False, index=True)

    password_hash = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


class Aircraft(Base):
    __tablename__ = "aircraft"

    aircraft_id = Column(Integer, primary_key=True, index=True)

    registration = Column(String, nullable=False)

    manufacturer = Column(String, nullable=False)

    model = Column(String, nullable=False)

    aircraft_type = Column(String, nullable=False)

    engine_type = Column(String, nullable=False)

    owner_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )