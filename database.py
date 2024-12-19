from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///task_manager.db"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

def initialize_db():
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")
