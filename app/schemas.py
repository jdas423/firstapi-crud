from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr, constr
from bson.objectid import ObjectId


class UserBaseSchema(BaseModel):
    firstname: str
    lastname: str
    email:str
    dateCreated: datetime | None = None
    lastUpdatedDate: datetime | None = None
    password:str

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    confirmpassword: str


class LoginUserSchema(BaseModel):
    email: str
    password: str


class UserResponseSchema(UserBaseSchema):
    id: str
    pass


class UserResponse(BaseModel):
    status: str
    user: UserResponseSchema


class FilteredUserResponse(UserBaseSchema):
    id: str


class ProjectBaseSchema(BaseModel):
    title: str
    about: str
    imageUrl: str
    dateCreated: datetime | None = None
    lastUpdatedDate: datetime | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class CreateProjectSchema(ProjectBaseSchema):
    user: ObjectId | None = None
    pass


class ProjectResponse(ProjectBaseSchema):
    id: str
    user: FilteredUserResponse
    dateCreated: datetime
    lastUpdatedDate: datetime


class UpdateProjectSchema(BaseModel):
    title: str | None = None
    about: str | None = None
    imageUrl: str | None = None
    user: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ListProjectResponse(BaseModel):
    status: str
    results: int
    Projects: List[ProjectResponse]