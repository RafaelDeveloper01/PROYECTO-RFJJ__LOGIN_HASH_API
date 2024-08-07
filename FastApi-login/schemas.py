from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    email: EmailStr

class UserInDBSchema(UserSchema):
    hashed_password: str
