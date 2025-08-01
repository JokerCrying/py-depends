import enum
from typing import TypeVar

T = TypeVar('T')


class DependsType(enum.Enum):
    sync_func = 'sync_func'
    sync_generate = 'sync_generate'
    async_func = 'async_func'
    async_generate = 'async_generate'
