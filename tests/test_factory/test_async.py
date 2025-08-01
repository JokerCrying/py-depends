import asyncio
import unittest
from src.py_depends.call_factory import AsyncDepends, AsyncGenerateDepends


async def async_func():
    await asyncio.sleep(0.1)
    return 'Hello'


async def async_generate():
    await asyncio.sleep(0.1)
    yield 'Hello'
    print('[async_generate]Generate Stop')


class TestAsyncDepends(unittest.TestCase):
    def test_async_func(self):
        fac = AsyncDepends()
        result = fac.get_result(async_func, {})
        self.assertEqual(result, 'Hello')

    def test_async_generate(self):
        fac = AsyncGenerateDepends()
        result = fac.get_result(async_generate, {})
        self.assertEqual(result, 'Hello')
