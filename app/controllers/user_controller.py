import email
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.models import User
from app.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password) 
    db_user = User(username=user.username, hashed_password=hashed_password, full_name=user.full_name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user_by_username(db: Session, username: str):
    res = db.query(User).filter(User.username == username).delete()
    db.commit()
    return res

def update_user_password(db: Session, new_password: str, username: str):
    new_hashed_password = get_password_hash(new_password)
    res = db.query(User).filter(User.username == username).update({User.hashed_password: new_hashed_password})
    db.commit()
    return res