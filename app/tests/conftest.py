import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..database import Base
from ..main import app, get_db

TEST_DATABASE_URL = "postgresql://postgres:12345@db/restaurant"

test_engine = create_engine(TEST_DATABASE_URL, )
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base.metadata.create_all(bind=test_engine)

# Очистка всех таблиц после каждого теста
@pytest.fixture(scope="session",autouse=True)
def clear_tables():
    metadata = MetaData()
    metadata.reflect(bind=test_engine)

    with TestingSessionLocal() as db:
        for table in reversed(metadata.sorted_tables):
            db.query(table).delete()
        db.commit()

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
