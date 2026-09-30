from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db
from app.database.models import Flight, Aircraft
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):

    total_flights = (
        db.query(func.count(Flight.flight_id))
        .filter(
            Flight.owner_id == current_user
        )
        .scalar()
    )

    total_hours = (
        db.query(func.sum(Flight.flight_time))
        .filter(
            Flight.owner_id == current_user
        )
        .scalar()
    )

    total_landings = (
        db.query(func.sum(Flight.landings))
        .filter(
            Flight.owner_id == current_user
        )
        .scalar()
    )

    aircraft_owned = (
        db.query(func.count(Aircraft.aircraft_id))
        .filter(
            Aircraft.owner_id == current_user
        )
        .scalar()
    )

    recent_flights = (
        db.query(Flight)
        .filter(
            Flight.owner_id == current_user
        )
        .order_by(
            Flight.flight_date.desc()
        )
        .limit(5)
        .all()
    )

    recent_flights_data = []

    for flight in recent_flights:
        recent_flights_data.append(
            {
                "flight_id": flight.flight_id,
                "flight_date": flight.flight_date,
                "departure_airport": flight.departure_airport,
                "arrival_airport": flight.arrival_airport,
                "flight_time": flight.flight_time,
                "landings": flight.landings
            }
        )

    return {
        "total_flights": total_flights or 0,
        "total_hours": total_hours or 0,
        "total_landings": total_landings or 0,
        "aircraft_owned": aircraft_owned or 0,
        "recent_flights": recent_flights_data
    }