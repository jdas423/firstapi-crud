from fastapi import APIRouter,HTTPException,Response,status,Depends
from models.user import User,Login,OAuth2ExtendedForm
from config.db import conn 
from bson.objectid import ObjectId
from passlib.context import CryptContext
import logging
import fortoken
from fastapi.security import OAuth2PasswordRequestForm

logging.getLogger('passlib').setLevel(logging.ERROR)

user = APIRouter() 

pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")

@user.post("/register/user")
async def register(userReq:User,response:Response):
     if userReq.password!=userReq.confirmpassword:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="passwords don't match")
     try:
         hashedPassword=pwd_cxt.hash(userReq.password)
         userReq.password=hashedPassword
         userReq = userReq.dict(exclude={"confirmpassword"})
         conn.user.user.insert_one(userReq)
         response.status_code = status.HTTP_201_CREATED
         return {"status": "success"}
     except Exception as e:
         print(e)
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="operation failed")



# Function to verify password
async def verify_password(plain_password, hashed_password):
    return pwd_cxt.verify(plain_password, hashed_password)

# Function to authenticate user
async def authenticate_user(email: str, password: str):
    user = conn.user.user.find_one({"email": email})
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user


# Login route
@user.post("/login/user")
async def login(login: dict = Depends(OAuth2ExtendedForm)):
    user = await authenticate_user(login["email"], login["password"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    access_token = fortoken.create_access_token( data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
   


