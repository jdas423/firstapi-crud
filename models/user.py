from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Form

class User(BaseModel):
    firstname:str
    lastname:str
    email:str
    password:str
    confirmpassword:str



class Login(BaseModel):
    email:str
    password:str


def OAuth2ExtendedForm(
    email: str = Form(...), 
    password: str = Form(...)
):
    return {"email": email, "password": password}