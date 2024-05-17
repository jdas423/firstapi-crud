from fastapi import APIRouter,HTTPException,status,Response,Depends
from models.project import Project 
from models.project import ProjectIn
from config.db import conn 
from schemas.project import serializeDict, serializeList
from bson.objectid import ObjectId
from models.user import User
import oAuth2



project = APIRouter() 

@project.get('/project')
async def find_all_projects(response:Response,current_user: User = Depends(oAuth2.get_current_user)):
    try:
       response.status_code=status.HTTP_200_OK
       return serializeList(conn.project.project.find())
    except Exception as e:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="operation failed")

@project.get('/project/{id}')
async def find_one_user(id,response:Response,current_user: User = Depends(oAuth2.get_current_user)):
     try:
        id_obj = ObjectId(id)
     except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId format")
 
     try:
       proj=conn.project.project.find_one({"_id":id_obj})
       if proj is None:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Project not found")
       response.status_code=status.HTTP_200_OK
       return serializeDict(proj)
     except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="operation failed")

@project.post('/project')
async def create_project(project:ProjectIn,response:Response,current_user: User = Depends(oAuth2.get_current_user)):
    try:
        project = Project.from_dict(dict(project))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid input data")
    try:
       conn.project.project.insert_one(dict(project))
       response.status_code = status.HTTP_201_CREATED
       return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Project cann't be created")
    


@project.put('/project/{id}')
async def update_project(id,project:ProjectIn,response:Response,current_user: User = Depends(oAuth2.get_current_user)):
    print(id)
    try:
        id_obj = ObjectId(id)
        project = Project.from_dict(dict(project))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId format or invalid input data")
   
    try: 
       conn.project.project.find_one_and_update({"_id":id_obj},{
        "$set":dict(project)
        })
       response.status_code = status.HTTP_200_OK
       return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="operation failed")
   

@project.delete('/project/{id}')
async def delete_project(id,response:Response,current_user: User = Depends(oAuth2.get_current_user)):
    try:
        id_obj = ObjectId(id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId format")
 
    try:
        conn.project.project.find_one_and_delete({"_id":id_obj})
        response.status_code = status.HTTP_200_OK
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="operation failed")
  