from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Flight
from app.auth.dependencies import get_current_user
from sqlalchemy import func

import csv
from io import StringIO

router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"]
)

@router.get("/export/csv")
def export_csv(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    flights = (
        db.query(Flight)
        .filter(
            Flight.owner_id == current_user
        )
        .order_by(
            Flight.flight_date.desc()
        )
        .all()
    )

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Date",
        "Departure",
        "Arrival",
        "Flight Time",
        "Landings",
        "Day/Night",
        "Remarks"
    ])

    for flight in flights:
        writer.writerow([
            flight.flight_date,
            flight.departure_airport,
            flight.arrival_airport,
            flight.flight_time,
            flight.landings,
            flight.day_night,
            flight.remarks
        ])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=flight_log.csv"
        }
    )
@router.get("/statistics")
def get_statistics(
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
    average_flight_time = (
        db.query(func.avg(Flight.flight_time))
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
    longest_flight = (
        db.query(func.max(Flight.flight_time))
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

    return {
        "total_flights": total_flights or 0,
        "total_hours": total_hours or 0,
        "average_flight_time": round(average_flight_time or 0, 2),
        "longest_flight": longest_flight or 0,
        "total_landings": total_landings or 0
    }