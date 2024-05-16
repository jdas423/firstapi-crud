from fastapi import FastAPI
from routes.project import project
app = FastAPI()
app.include_router(project)
