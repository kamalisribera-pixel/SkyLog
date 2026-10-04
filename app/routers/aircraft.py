from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Aircraft
from app.schemas.aircraft import AircraftCreate
from app.auth.dependencies import get_current_user
from fastapi import HTTPException

router = APIRouter(prefix="/api/aircraft", tags=["Aircraft"])


from fastapi import status


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_aircraft(
    request: AircraftCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):

    aircraft = Aircraft(
        registration=request.registration,
        manufacturer=request.manufacturer,
        model=request.model,
        aircraft_type=request.aircraft_type,
        engine_type=request.engine_type,
        owner_id=current_user,
    )

    db.add(aircraft)
    db.commit()
    db.refresh(aircraft)

    return aircraft


@router.get("/")
def get_aircraft(
    db: Session = Depends(get_db), current_user: int = Depends(get_current_user)
):

    aircraft = db.query(Aircraft).filter(Aircraft.owner_id == current_user).all()

    return aircraft


@router.get("/{aircraft_id}")
def get_aircraft_by_id(
    aircraft_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):

    aircraft = (
        db.query(Aircraft)
        .filter(Aircraft.aircraft_id == aircraft_id, Aircraft.owner_id == current_user)
        .first()
    )

    if aircraft is None:
        raise HTTPException(status_code=404, detail="Aircraft not found.")

    return aircraft


@router.put("/{aircraft_id}")
def update_aircraft(
    aircraft_id: int,
    request: AircraftCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):

    aircraft = (
        db.query(Aircraft)
        .filter(Aircraft.aircraft_id == aircraft_id, Aircraft.owner_id == current_user)
        .first()
    )

    if aircraft is None:
        raise HTTPException(status_code=404, detail="Aircraft not found.")

    aircraft.registration = request.registration
    aircraft.manufacturer = request.manufacturer
    aircraft.model = request.model
    aircraft.aircraft_type = request.aircraft_type
    aircraft.engine_type = request.engine_type

    db.commit()
    db.refresh(aircraft)

    return aircraft


@router.delete("/{aircraft_id}")
def delete_aircraft(
    aircraft_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):

    aircraft = (
        db.query(Aircraft)
        .filter(Aircraft.aircraft_id == aircraft_id, Aircraft.owner_id == current_user)
        .first()
    )

    if aircraft is None:
        raise HTTPException(status_code=404, detail="Aircraft not found.")

    db.delete(aircraft)
    db.commit()

    return {"message": "Aircraft deleted successfully."}
