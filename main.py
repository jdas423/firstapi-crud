from fastapi import FastAPI
from routes.project import project
from routes.user import user
import uvicorn

app = FastAPI()
app.include_router(user)
app.include_router(project)



# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000)

