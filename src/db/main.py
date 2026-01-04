from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.config import Config

engine  = create_engine(Config.DATABASE_URL,
                        echo=True)

sessionlocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)
class Base(DeclarativeBase):
    pass

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

def create_table():
    Base.metadata.create_all(engine)
