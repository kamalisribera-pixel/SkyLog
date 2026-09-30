from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import User
from app.schemas.auth import RegisterRequest
from app.auth.hashing import hash_password

from app.schemas.auth import LoginRequest

from app.auth.hashing import verify_password

from app.auth.jwt_handler import create_access_token

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):

    existing_user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    user = User(
        name=request.name,
        email=request.email,
        password_hash=hash_password(request.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User registered successfully!",
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email
    }

@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if not verify_password(
        request.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    access_token = create_access_token(
        {
            "sub": str(user.user_id)
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

from app.auth.dependencies import get_current_user


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "message": "Authenticated!",
        "user": current_user
    }