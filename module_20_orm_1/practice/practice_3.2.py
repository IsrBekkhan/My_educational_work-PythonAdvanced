from sqlalchemy import Column, Integer, String, Index
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

Base = declarative_base()
engine = create_engine('sqlite:///sqlite_python.db')
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
   __tablename__ = 'user'
   __table_args__ = (Index('email_index', 'email'),)

   id = Column(Integer, primary_key=True)
   name = Column(String(16), nullable=False)
   email = Column(String(60))
   login = Column(String(50), nullable=False)

   def __repr__(self):
       return f"{self.name}, {self.email}, {self.login}"

   @classmethod
   def get_all_users(cls):
       return session.query(User).all()

Base.metadata.create_all(engine)
users = User.get_all_users()
print(users)