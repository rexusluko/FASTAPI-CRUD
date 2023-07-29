from sqlalchemy import create_engine, MetaData,orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:12345@db/restaurant"
engine = create_engine(DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = orm.declarative_base()
metadata = MetaData()