import asyncio
import unittest
from src.depends_tools.context import DependencyContext
from src.depends_tools.util import inject
from src.depends_tools.depends import Depends


async def get_db():
    await asyncio.sleep(0.1)
    yield 'DataBase<db_driver=mysql+pymysql host=localhost port=3306>'
    print('[get_db]Stop Generate')


async def get_driver():
    await asyncio.sleep(0.1)
    yield 'postgresql'
    print('[get_db]Stop Generate')


async def get_pg_db(driver: str = Depends(get_driver)):
    await asyncio.sleep(0.1)
    yield f'DataBase<db_driver={driver} host=localhost port=5678>'
    print('[get_db]Stop Generate')


class DBService:
    def __init__(
            self,
            db: str = Depends(get_db),
            pg_db: str = Depends(get_pg_db)
    ):
        self.db = db
        self.pg_db = pg_db

    def info(self):
        print(self.db)
        print(self.pg_db)
        return True


class TestSyncDeps(unittest.TestCase):
    def setUp(self):
        self.context = DependencyContext()
        self.context.cache.clear()
        self.context.overrides.clear()
        self.context.resolving.clear()

    def test_base_dep(self):
        @inject
        def main(db: str = Depends(get_db)):
            print('Using', db)
            return db

        result = main()
        self.assertEqual(result, get_db())

    def test_recursion_dep(self):
        @inject
        def main(db: set = Depends(get_pg_db)):
            print('Using', db)
            return db

        result = main()
        self.assertEqual(result, 'DataBase<db_driver=postgresql host=localhost port=5678>')

    def test_class(self):
        @inject
        def main(db_service: DBService = Depends(DBService)):
            return db_service.info()

        result = main()
        self.assertEqual(result, True)
