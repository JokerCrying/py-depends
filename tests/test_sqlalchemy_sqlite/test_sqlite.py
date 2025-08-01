import random
import unittest
from src.depends_tools.context import DependencyContext
from src.depends_tools.util import inject
from src.depends_tools.depends import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///test.db')
session_local = sessionmaker(engine)
Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), comment='name')

    def __repr__(self):
        return f'Student<id={self.id} name={self.name}>'


Base.metadata.create_all(bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


class DBService:
    def __init__(
            self,
            db: Session = Depends(get_db)
    ):
        self.db = db

    def add_user(self):
        t_id = random.randint(100000, 999999)
        model = Student(name=f'student-{t_id}')
        self.db.add(model)
        self.db.commit()
        return 'success'

    def users(self):
        query = self.db.query(Student).all()
        return query


class TestSASqliteDeps(unittest.TestCase):
    def setUp(self):
        self.context = DependencyContext()
        self.context.cache.clear()
        self.context.overrides.clear()
        self.context.resolving.clear()

    def test_add_user(self):
        @inject
        def main(db_service: DBService = Depends(DBService)):
            db_service.add_user()
            return 'success'

        result = main()
        self.assertEqual(result, 'success')

    def test_user_list(self):
        @inject
        def main(db_service: DBService = Depends(DBService)):
            print(db_service.users())
            return 'success'

        result = main()
        self.assertEqual(result, 'success')
