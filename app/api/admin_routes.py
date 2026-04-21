from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.llm_log import LLMLog
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/logs")
def get_all_logs(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    role = str(current_user.get("role", "")).strip().lower()
    if role not in {"admin", "employee"}:
        raise HTTPException(status_code=403, detail="Not authorized")

    if role == "admin":
        logs = db.query(LLMLog).all()
    else:
        logs = db.query(LLMLog).filter(LLMLog.user_id == current_user["email"]).all()

    return [
        {
            "user_id": log.user_id,
            "cost": log.cost,
            "latency": log.latency,
            "created_at": log.created_at,
        }
        for log in logs
    ]
