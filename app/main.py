from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api.auth_routes import router as auth_router
from app.api.employee_routes import router as employee_router
from app.api.admin_routes import router as admin_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Company AI Governance System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(admin_router)
