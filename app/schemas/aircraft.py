from pydantic import BaseModel


class AircraftCreate(BaseModel):
    registration: str
    manufacturer: str
    model: str
    aircraft_type: str
    engine_type: str
