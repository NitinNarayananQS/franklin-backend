from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    full_name: str
    password: str
    
class User(UserBase):
    id: int
    is_active: bool
    hashed_password: str
    role: str

    class Config:
        orm_mode = True

class ForgotPass(BaseModel):
    email: str