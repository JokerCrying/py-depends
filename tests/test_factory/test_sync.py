import unittest
from src.depends_tools.call_factory import SyncDepends, SyncGenerateDepends


def sync_gene():
    yield 'Hello'
    print('[sync_gene]Sync Generate Stop.')


def sync_func():
    return 'Hello'


class TestFactory(unittest.TestCase):
    def test_sync_func(self):
        fac = SyncDepends()
        result = fac.get_result(sync_func, {})
        self.assertEqual(result, 'Hello')

    def test_sync_generate(self):
        fac = SyncGenerateDepends()
        result = fac.get_result(sync_gene, {})
        self.assertEqual(result, 'Hello')
