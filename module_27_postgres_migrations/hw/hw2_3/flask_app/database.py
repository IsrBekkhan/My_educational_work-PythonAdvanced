from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')


POSTGRES_URL = f'postgresql+psycopg2://admin:admin@localhost:5432/skillbox_db'

engine = create_engine(POSTGRES_URL, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()

