from sqlalchemy import Column, String, Integer

from database import Base

class Book(Base):
    __tablename__ = 'Book'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
