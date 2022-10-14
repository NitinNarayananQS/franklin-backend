from fastapi import FastAPI, Depends
from app.routers import auth, jobs
from app.dependencies import get_db
from typing import List

app = FastAPI(dependencies=[Depends(get_db)])

app.include_router(auth.router)
app.include_router(jobs.router)

@app.get("/")
def default_path():
    return {"Error": "404 Page not found"}