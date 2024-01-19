from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os
import logging

from utility import close_gunicorn

logger = logging.getLogger(__name__)
logging.basicConfig(level='DEBUG')


POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

logging.debug(f"User: {POSTGRES_USER}")
logging.debug(f"Password: {POSTGRES_PASSWORD}")

if not all((POSTGRES_USER, POSTGRES_PASSWORD)):
    logger.error('Missing environment variables POSTGRES_USER or POSTGRES_PASSWORD')
    close_gunicorn()

POSTGRES_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost'

engine = create_engine(POSTGRES_URL, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()

