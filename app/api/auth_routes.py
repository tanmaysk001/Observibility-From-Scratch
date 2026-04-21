from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.auth_service import register_user, authenticate_user
from app.core.security import create_access_token
from app.schemas import UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(request: UserCreate, db: Session = Depends(get_db)):
    normalized_role = (request.role or "").strip().lower()
    if normalized_role not in {"admin", "employee"}:
        raise HTTPException(status_code=400, detail="Role must be admin or employee")

    user = register_user(
        db,
        request.name,
        request.email,
        request.password,
        normalized_role,
    )
    if not user:
        raise HTTPException(status_code=400, detail="Email already exists")

    return {"message": "User created"}


@router.post("/login")
def login(request: UserLogin, db: Session = Depends(get_db)):

    user = authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user.email,
        "role": user.role
    })

    return {"access_token": token}
