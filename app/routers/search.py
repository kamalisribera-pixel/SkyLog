from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Flight
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/search", tags=["Search"])


@router.get("/flights")
def search_flights(
    departure_airport: str | None = Query(default=None),
    arrival_airport: str | None = Query(default=None),
    day_night: str | None = Query(default=None),
    aircraft_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):

    query = db.query(Flight).filter(Flight.owner_id == current_user)

    if departure_airport:
        query = query.filter(Flight.departure_airport == departure_airport)

    if arrival_airport:
        query = query.filter(Flight.arrival_airport == arrival_airport)

    if day_night:
        query = query.filter(Flight.day_night == day_night)

    if aircraft_id:
        query = query.filter(Flight.aircraft_id == aircraft_id)

    flights = query.order_by(Flight.flight_date.desc()).all()

    flight_data = []

    for flight in flights:
        flight_data.append(
            {
                "flight_id": flight.flight_id,
                "aircraft_id": flight.aircraft_id,
                "flight_date": flight.flight_date,
                "departure_airport": flight.departure_airport,
                "arrival_airport": flight.arrival_airport,
                "flight_time": flight.flight_time,
                "landings": flight.landings,
                "day_night": flight.day_night,
                "remarks": flight.remarks,
            }
        )

    return {"count": len(flight_data), "flights": flight_data}
