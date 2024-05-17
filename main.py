from fastapi import FastAPI
from routes.project import project
from routes.user import user
import os
import uvicorn

app = FastAPI()
app.include_router(user)
app.include_router(project)


uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
