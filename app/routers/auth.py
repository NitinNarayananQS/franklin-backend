import os
from fastapi import HTTPException, Depends, APIRouter, status
from datetime import timedelta
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.schemas.token import Token
from app.schemas.user import ResetPass, User, UserCreate, ForgotPass
from app.controllers import user_controller as crud
from app.dependencies import get_db
from app.util.auth_util import authenticate_user, create_access_token, get_current_active_user, get_db, send_email

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/current_user", response_model=User)
async def get_logged_in_user(
    current_user: User = Depends(get_current_active_user),
):
    return current_user


@router.post("/register", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user_by_username = crud.get_user_by_username(db, username=user.username)
    db_user_by_email = crud.get_user_by_email(db, email=user.email)
    if db_user_by_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")        
    return crud.create_user(db=db, user=user)

# @router.post('/delete')
# def delete_user(username: str, db: Session = Depends(get_db)):
#     return crud.delete_user_by_username(db, username=username)

@router.get("/getall", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.post("/forgotpassword")
async def forgot_password(req: ForgotPass, db: Session = Depends(get_db)):
    email = req.email
    if not email:
        raise HTTPException(status_code=400, detail="Missing Email")
    user: User = crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=400, detail="A registered user with the provided email could not be found.")
  
    reset_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    reset_token = create_access_token(
        data={"username": user.username}, expires_delta=reset_token_expires
    )    
    await send_email(email=email, reset_token=reset_token)
    return {
        "message": "reset token was sent to the provided email"
    }
    
@router.post("/resetpassword")
async def reset_password(req: ResetPass, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(req.reset_token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
        username: str = payload.get("username")
        if username is None:
            raise HTTPException(status_code=404, detail="Invalid Reset Token")
        user = crud.get_user_by_username(db, username=username)
        if user is None:
            raise HTTPException(status_code=404, detail="Invalid Reset Token, a matching user was not found")
        res = crud.update_user_password(db, req.new_password, username)
        if res:
            return {
                "message": "password was reset"
            }
    except JWTError:
        raise HTTPException(status_code=400, detail="JWT decode error")
    return {
        "message": "an error occured during password reset"
    }
    