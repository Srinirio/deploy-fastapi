from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from core import settings


Base = declarative_base()

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)