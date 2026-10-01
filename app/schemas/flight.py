from datetime import date

from pydantic import BaseModel, ConfigDict


class FlightCreate(BaseModel):

    aircraft_id: int

    flight_date: date

    departure_airport: str

    arrival_airport: str

    flight_time: float

    landings: int

    day_night: str

    remarks: str | None = None


class FlightResponse(BaseModel):

    flight_id: int

    owner_id: int

    aircraft_id: int

    flight_date: date

    departure_airport: str

    arrival_airport: str

    flight_time: float

    landings: int

    day_night: str

    remarks: str | None

    model_config = ConfigDict(
        from_attributes=True
    )

class FlightListResponse(BaseModel):

    page: int

    size: int

    total_flights: int

    returned: int

    flights: list[FlightResponse]
