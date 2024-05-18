
from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import Project
from app.oauth import require_user
from app.serializers.projectSerializers import projectEntity, projectListEntity
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

router = APIRouter()


@router.get('/')
def get_projects(limit: int = 10, page: int = 1, search: str = '', user_id: str = Depends(require_user)):
    skip = (page - 1) * limit
    print(user_id)
    pipeline = [
        {'$match': {'user': ObjectId(user_id)}},  # Filter by user_id
        {'$lookup': {'from': 'users', 'localField': 'user',
                     'foreignField': '_id', 'as': 'user'}},
        {'$unwind': '$user'},
        {
            '$skip': skip
        }, {
            '$limit': limit
        }
    ]
    projects = projectListEntity(Project.find({"user":ObjectId(user_id)}))
    print(projects)
    return {'status': 'success', 'results': len(projects), 'projects': projects}

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_project(project: schemas.CreateProjectSchema, user_id: str = Depends(require_user)):
    project.user = ObjectId(user_id)
    project.dateCreated = datetime.utcnow()
    project.lastUpdatedDate = project.dateCreated
    try:
        result = Project.insert_one(project.dict())
        inserted_id = result.inserted_id
        return {"message": "Project created successfully", "project_id": str(inserted_id)}
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"project with title: '{project.title}' already exists")


@router.put('/{id}')
def update_project(id: str, payload: schemas.UpdateProjectSchema, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    updated_project = Project.find_one_and_update(
        {'_id': ObjectId(id)}, {'$set': payload.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if not updated_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No project with this id: {id} found')
    return projectEntity(updated_project)


@router.get('/{id}')
def get_project(id: str, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    pipeline = [
        {'$match': {'_id': ObjectId(id)}},
        {'$lookup': {'from': 'users', 'localField': 'user',
                     'foreignField': '_id', 'as': 'user'}},
        {'$unwind': '$user'},
    ]
    db_cursor = Project.aggregate(pipeline)
    results = list(db_cursor)

    if len(results) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No project with this id: {id} found")

    project = projectListEntity(results)[0]
    return project


@router.delete('/{id}')
def delete_project(id: str, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    project = Project.find_one_and_delete({'_id': ObjectId(id)})
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No project with this id: {id} found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)