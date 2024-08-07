from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    hashed_password: str
