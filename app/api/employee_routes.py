from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.core.dependencies import get_current_user
from app.services.llm_service import call_llm
from app.services.logging_service import log_request
from app.schemas import LLMRequest

router = APIRouter(prefix="/employee", tags=["Employee"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/generate")
def generate(
    request: LLMRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    role = str(current_user.get("role", "")).strip().lower()
    if role not in {"employee", "admin"}:
        raise HTTPException(status_code=403, detail="Not authorized")

    output, tin, tout, cost, latency = call_llm(request.prompt, request.model_name)

    log_request(
        db,
        current_user["email"],
        request.model_name,
        request.prompt,
        output,
        tin,
        tout,
        cost,
        latency,
    )

    return {
        "response": output,
        "cost": cost,
        "latency": latency
    }
