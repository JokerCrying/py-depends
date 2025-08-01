import abc
import asyncio
from contextlib import contextmanager
from typing import Dict, Callable
from .d_type import DependsType


class CallDependsInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    @contextmanager
    def call_depends(self, dependency_func: Callable, final_kwargs: Dict):
        raise NotImplemented

    def get_result(self, dependency_func: Callable, final_kwargs: Dict):
        with self.call_depends(dependency_func, final_kwargs) as result:
            return result


class SyncDepends(CallDependsInterface):
    @contextmanager
    def call_depends(self, dependency_func: Callable, final_kwargs: Dict):
        result = dependency_func(**final_kwargs)
        yield result


class AsyncDepends(CallDependsInterface):
    def __init__(self):
        self._loop = asyncio.get_event_loop()

    @contextmanager
    def call_depends(self, dependency_func: Callable, final_kwargs: Dict):
        yield self._loop.run_until_complete(dependency_func(**final_kwargs))
        if self._loop.is_running():
            self._loop.close()


class SyncGenerateDepends(CallDependsInterface):
    @contextmanager
    def call_depends(self, dependency_func: Callable, final_kwargs: Dict):
        yield from dependency_func(**final_kwargs)


class AsyncGenerateDepends(CallDependsInterface):
    def __init__(self):
        self._loop = asyncio.get_event_loop()

    @contextmanager
    def call_depends(self, dependency_func: Callable, final_kwargs: Dict):
        async_gen = dependency_func(**final_kwargs)

        def async_generate_to_sync():
            try:
                while True:
                    try:
                        future = async_gen.__anext__()
                        value = self._loop.run_until_complete(future)
                        yield value
                    except StopAsyncIteration:
                        break
            finally:
                self._loop.run_until_complete(async_gen.aclose())

        yield from async_generate_to_sync()
        if self._loop.is_running():
            self._loop.close()


class CallDependsFactory:
    fac = {
        DependsType.sync_func: SyncDepends,
        DependsType.async_func: AsyncDepends,
        DependsType.sync_generate: SyncGenerateDepends,
        DependsType.async_generate: AsyncGenerateDepends
    }

    @staticmethod
    def get(dep_type: DependsType):
        if dep_type not in CallDependsFactory.fac:
            raise ValueError(f'The type {dep_type} has no factory for run call depends.')
        return CallDependsFactory.fac[dep_type]
