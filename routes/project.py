from fastapi import APIRouter
from models.project import Project 
from models.project import ProjectIn
from config.db import conn 
from schemas.project import serializeDict, serializeList
from bson import ObjectId
project = APIRouter() 

@project.get('/')
async def find_all_projects():
    print(conn)
    return serializeList(conn.project.project.find())

@project.get('/{id}')
async def find_one_user(id):
    return serializeDict(conn.project.project.find_one({"_id":ObjectId(id)}))

@project.post('/')
async def create_project(project:ProjectIn):
    project = Project.from_dict(project.dict())
    print(project)
    try:
       conn.project.project.insert_one(project.dict())
       return {"status": "success"}
    except Exception as e:
        print(e)
        return {"status": "fail"}
    

@project.put('/{id}')
async def update_project(id,project:ProjectIn):
    conn.local.user.find_one_and_update({"_id":ObjectId(id)},{
        "$set":project.dict()
    })
    return {"status": "success"}

@project.delete('/{id}')
async def delete_project(id):
   conn.project.project.find_one_and_delete({"_id":ObjectId(id)})
   return {"status": "success"}