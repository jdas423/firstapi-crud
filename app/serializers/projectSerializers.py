from app.serializers.userSerializers import embeddedUserResponse


def projectEntity(project) -> dict:
    return {
        "id": str(project["_id"]),
        "title": project["title"],
        "about": project["about"],
        "imageUrl": project["imageUrl"],
        "user": str(project["user"]),
        "dateCreated": project["dateCreated"],
        "lastUpdatedDate": project["lastUpdatedDate"]
    }


def populatedprojectEntity(project) -> dict:
    return {
        "id": str(project["_id"]),
        "title": project["title"],
        "about": project["about"],
        "imageUrl": project["imageUrl"],
        "dateCreated": project["dateCreated"],
        "lastUpdatedDate": project["lastUpdatedDate"]
    }


def projectListEntity(projects) -> list:
    return [populatedprojectEntity(project) for project in projects]