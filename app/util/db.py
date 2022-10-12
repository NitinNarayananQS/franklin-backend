from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://nitin:nitin@db:5432/dagster"
# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://nitin:nitin@localhost:5432/dagster"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()