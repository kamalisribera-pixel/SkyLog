from datetime import date

from pydantic import BaseModel


class FlightCreate(BaseModel):

    aircraft_id: int

    flight_date: date

    departure_airport: str

    arrival_airport: str

    flight_time: float

    landings: int

    day_night: str

    remarks: str | None = None