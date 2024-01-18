from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os
import logging

from utility import close_gunicorn

logger = logging.getLogger(__name__)
logging.basicConfig(level='DEBUG')


POSTGRES_LOGIN = os.getenv('POSTGRES_LOGIN')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

if not all((POSTGRES_LOGIN, POSTGRES_PASSWORD)):
    logger.error('Missing environment variables POSTGRES_LOGIN or POSTGRES_PASSWORD')
    close_gunicorn()

POSTGRES_URL = f'postgresql+psycopg2://{POSTGRES_LOGIN}:{POSTGRES_PASSWORD}@localhost'

engine = create_engine(POSTGRES_URL, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()

