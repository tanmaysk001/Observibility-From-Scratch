from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON
from datetime import datetime
from app.database import Base

class LLMLog(Base):
    __tablename__ = "llm_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    model_name = Column(String)
    prompt = Column(Text)
    response = Column(Text)
    tokens_input = Column(Integer)
    tokens_output = Column(Integer)
    cost = Column(Float)
    latency = Column(Float)
    embedding = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
