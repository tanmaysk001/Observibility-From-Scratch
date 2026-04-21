from sqlalchemy.orm import Session
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def register_user(db: Session, name: str, email: str, password: str, role: str):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return None

    hashed_pw = hash_password(password)
    normalized_role = (role or "").strip().lower()

    new_user = User(
        name=name,
        email=email,
        hashed_password=hashed_pw,
        role=normalized_role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
