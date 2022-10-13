from pydantic import BaseModel

class UserBase(BaseModel):
    username: str


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
        