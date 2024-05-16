from pydantic import BaseModel
from datetime import datetime


class Project(BaseModel):
    title:str
    about:str
    imgUrl:str
    dateCreated:datetime
    lastDateUpdated:datetime

    @classmethod
    def from_dict(cls, data: dict):
        data['dateCreated']=datetime.strptime(data['dateCreated'], "%Y-%m-%d").date()
        data['lastDateUpdated']=datetime.strptime(data['lastDateUpdated'], "%Y-%m-%d").date()
        return cls(**data)
    
class ProjectIn(BaseModel):
    title:str
    about:str
    imgUrl:str
    dateCreated:str
    lastDateUpdated:str
