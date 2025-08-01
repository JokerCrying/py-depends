import unittest


class TestImport(unittest.TestCase):
    def test_import(self):
        from src.depends_tools import Depends, inject
