from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.hybrid import hybrid_property
from typing import List, Any, Dict
from threading import Lock

engine = create_engine('sqlite:///subscribes.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

LOCK = Lock()


class Subscription(Base):
    __tablename__ = 'subscriptions'

    email = Column(String, primary_key=True)

    def to_list(self) -> List[Any]:
        return getattr(self, self.__table__.columns[0].name)

    @classmethod
    def subscribe(cls, email):
        session.add(Subscription(email=email))
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            return "Вы уже были подписаны."
        session.close()
        return f"Ваша почта {email} добавлена в список рассылки!"

    @classmethod
    def unsubscribe(cls, email):
        if session.query(Subscription).one_or_none() is None:
            return "Такой почты нет в списке рассылки!"

        session.query(Subscription) \
            .filter(Subscription.email.like(email)) \
            .delete(synchronize_session=False)
        session.commit()
        session.close()
        return "Вы отписаны от рассылки!"

    @classmethod
    def all_subscribers(cls):
        result = session.query(Subscription).all()
        return [subscriber.to_list() for subscriber in result]


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(String, primary_key=True)
    processed_images = Column(Integer, default=0)
    total_images = Column(Integer, default=0)
    status = Column(String, default='')
    email = Column(String, nullable=False)

    @hybrid_property
    def progress(self):
        return round((self.processed_images / self.total_images * 100), 2)

    def to_json(self) -> Dict[str, Any]:
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}

    @classmethod
    def add_task(cls, task_id: str, total_images: int, status: str, email: str):
        task = Task(
            id=task_id,
            total_images=total_images,
            status=status,
            email=email
        )
        session.add(task)
        session.commit()

    @classmethod
    def update_progress(cls, task_id: str):
        global LOCK
        with LOCK:
            task: Task = session.query(Task).filter(Task.id == task_id).one()
            task.processed_images += 1
            if task.processed_images == task.total_images:
                task.status = 'обработано'
            session.commit()

    @classmethod
    def is_done(cls, task_id: str):
        task: Task = session.query(Task).filter(Task.id == task_id).one()
        if task.progress == 100:
            task.status = 'отправлено на почту'
            session.commit()
            return True
        return False

    @classmethod
    def get_task_by_task_id(cls, task_id: str):
        return session.query(Task).filter(Task.id == task_id).one()

