def serializeDict(a) -> dict:
    return {
        **{i: str(a[i]) for i in a if i == '_id'},
        **{i: a[i].isoformat() for i in a if i == 'dateCreated' or i == 'dateUpdated'},
        **{i: a[i] for i in a if i not in ('_id', 'dateCreated', 'dateUpdated')}
    }

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]
