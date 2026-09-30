from fastapi import FastAPI

from app.database.database import engine
from app.database.models import Base
from app.routers.auth import router as auth_router

from app.routers.aircraft import router as aircraft_router
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SkyLog API",
    description="Electronic Flight Logbook API for Private Pilots",
    version="1.0.0"
)
app.include_router(auth_router)
app.include_router(aircraft_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to SkyLog API!"
    }