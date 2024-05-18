def userEntity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "firstname": user["firstname"],
        "lastname": user["lastname"],
        "email": user["email"],
        "password": user["password"],
    }


def userResponseEntity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "firstname": user["firstname"],
        "lastname": user["lastname"],
        "email": user["email"],
    }


def embeddedUserResponse(user) -> dict:
    return {
        "id": str(user["_id"]),
        "firstname": user["firstname"],
        "lastname": user["lastname"],
        "email": user["email"],
    }


def userListEntity(users) -> list:
    return [userEntity(user) for user in users]