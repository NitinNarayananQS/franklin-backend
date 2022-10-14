import json
from fastapi.testclient import TestClient
from app import SessionLocal
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import Base
from app.dependencies import get_db
from app.main import app
from app.controllers.user_controller import delete_user_by_username


SQLALCHEMY_DATABASE_URL = "postgresql://nitin:nitin@db:5432/dagster_test"
# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://nitin:nitin@localhost:5432/dagster_test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_read_users_from_db():
    response = client.get("/auth/getall?skip=0&limit=100")
    assert response.status_code == 200
    assert type(response.json()) == type([])


def test_register_and_login():
    db = TestingSessionLocal()
    response = client.post(
        "/auth/register",
        json.dumps({
            "username": "testdev",
            "email": "testdev@gmail.com",
            "full_name": "testdev",
            "password": "testdev",
        }),
    )
    assert response.json()['username'] == "testdev"
    response = client.post(
        "auth/login",
        {
            "username": "testdev",
            "password": "testdev"
        }
    )
    assert len(response.json()['access_token']) > 0
    assert delete_user_by_username(db, username="testdev") == 1

