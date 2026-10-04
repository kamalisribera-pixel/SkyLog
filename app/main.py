from fastapi import FastAPI

from app.database.database import engine
from app.database.models import Base
from app.routers.auth import router as auth_router
from app.routers.dashboard import router as dashboard_router

from app.routers.aircraft import router as aircraft_router

Base.metadata.create_all(bind=engine)
from app.routers.flights import router as flight_router
from app.routers.reports import router as reports_router

app = FastAPI(
    title="SkyLog API",
    description="Electronic Flight Logbook API for Private Pilots",
    version="1.0.0",
)
app.include_router(auth_router)
app.include_router(aircraft_router)
app.include_router(flight_router)
app.include_router(dashboard_router)
app.include_router(reports_router)


@app.get("/")
def root():
    return {"message": "Welcome to SkyLog API!"}
