from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings


# db_url = 'postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/instagram_service'
# engine = create_engine(db_url)

engine = create_engine(settings.db_url)


Session = sessionmaker(engine)


def get_db_session():
    return Session
