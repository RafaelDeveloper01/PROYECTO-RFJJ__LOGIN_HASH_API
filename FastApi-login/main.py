from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import User, UserResponse
from database import user_collection, user_helper
from auth import get_password_hash, authenticate_user, create_access_token, verify_token

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/signup", response_model=UserResponse)
async def create_user(user: User):
    user_in_db = await user_collection.find_one({"email": user.email})
    if user_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password = get_password_hash(user.password)
    new_user = await user_collection.insert_one({
        "email": user.email,
        "hashed_password": hashed_password
    })
    created_user = await user_collection.find_one({"_id": new_user.inserted_id})
    return user_helper(created_user)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(token: str = Depends(oauth2_scheme)):
    email = verify_token(token)
    user = await user_collection.find_one({"email": email})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_helper(user)
