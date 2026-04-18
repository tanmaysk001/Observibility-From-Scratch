from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str


class UserLogin(BaseModel):
    email: str
    password: str


class LLMRequest(BaseModel):
    prompt: str
    model_name: str = "gpt-4o-mini"
    user_id: str | None = None
