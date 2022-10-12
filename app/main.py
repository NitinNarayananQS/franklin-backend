from fastapi import FastAPI, Depends
from .routers import auth, jobs
from .dependencies import get_db
from sqlalchemy.orm import Session
from typing import List
from .util import crud, schemas

app = FastAPI(dependencies=[Depends(get_db)])

app.include_router(auth.router)
app.include_router(jobs.router)

@app.get("/")
def default_path():
    return {"Error": "404 Page not found"}