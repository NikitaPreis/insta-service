from settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.db_url)


Session = sessionmaker(engine)


def get_db_session():
    return Session
