from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Flight, Aircraft
from app.schemas.flight import (
    FlightCreate,
    FlightResponse,
    FlightListResponse
)
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/api/flights",
    tags=["Flights"]
)


@router.post(
    "/",
    response_model=FlightResponse,
    status_code=status.HTTP_201_CREATED
)
def create_flight(
    request: FlightCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):

    aircraft = (
        db.query(Aircraft)
        .filter(
            Aircraft.aircraft_id == request.aircraft_id,
            Aircraft.owner_id == current_user
        )
        .first()
    )

    if aircraft is None:
        raise HTTPException(
            status_code=404,
            detail="Aircraft not found."
        )

    flight = Flight(
        owner_id=current_user,
        aircraft_id=request.aircraft_id,
        flight_date=request.flight_date,
        departure_airport=request.departure_airport,
        arrival_airport=request.arrival_airport,
        flight_time=request.flight_time,
        landings=request.landings,
        day_night=request.day_night,
        remarks=request.remarks
    )

    db.add(flight)
    db.commit()
    db.refresh(flight)

    return flight


@router.get(
    "/",
    response_model=FlightListResponse
)
def get_flights(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):

    offset = (page - 1) * size

    total_flights = (
        db.query(Flight)
        .filter(
            Flight.owner_id == current_user
        )
        .count()
    )

    flights = (
        db.query(Flight)
        .filter(
            Flight.owner_id == current_user
        )
        .order_by(
            Flight.flight_date.desc()
        )
        .offset(offset)
        .limit(size)
        .all()
    )

    return {
        "page": page,
        "size": size,
        "total_flights": total_flights,
        "returned": len(flights),
        "flights": flights
    }


@router.get(
    "/{flight_id}",
    response_model=FlightResponse
)
def get_flight(
    flight_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):

    flight = (
        db.query(Flight)
        .filter(
            Flight.flight_id == flight_id,
            Flight.owner_id == current_user
        )
        .first()
    )

    if flight is None:
        raise HTTPException(
            status_code=404,
            detail="Flight not found."
        )

    return flight


@router.put(
    "/{flight_id}",
    response_model=FlightResponse
)
def update_flight(
    flight_id: int,
    request: FlightCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):

    flight = (
        db.query(Flight)
        .filter(
            Flight.flight_id == flight_id,
            Flight.owner_id == current_user
        )
        .first()
    )

    if flight is None:
        raise HTTPException(
            status_code=404,
            detail="Flight not found."
        )

    aircraft = (
        db.query(Aircraft)
        .filter(
            Aircraft.aircraft_id == request.aircraft_id,
            Aircraft.owner_id == current_user
        )
        .first()
    )

    if aircraft is None:
        raise HTTPException(
            status_code=404,
            detail="Aircraft not found."
        )

    flight.aircraft_id = request.aircraft_id
    flight.flight_date = request.flight_date
    flight.departure_airport = request.departure_airport
    flight.arrival_airport = request.arrival_airport
    flight.flight_time = request.flight_time
    flight.landings = request.landings
    flight.day_night = request.day_night
    flight.remarks = request.remarks

    db.commit()
    db.refresh(flight)

    return flight


@router.delete("/{flight_id}")
def delete_flight(
    flight_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):

    flight = (
        db.query(Flight)
        .filter(
            Flight.flight_id == flight_id,
            Flight.owner_id == current_user
        )
        .first()
    )

    if flight is None:
        raise HTTPException(
            status_code=404,
            detail="Flight not found."
        )

    db.delete(flight)
    db.commit()

    return {
        "message": "Flight deleted successfully."
    }