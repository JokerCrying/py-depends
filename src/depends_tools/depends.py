import inspect
from typing import Callable, Optional
from functools import wraps
from .d_type import T
from .injector import inject_call


class Depends:
    """依赖声明类"""
    __slots__ = ("dependency", "use_cache", "cache")

    def __init__(self, dependency: Callable[..., T], use_cache: bool = True):
        self.dependency = dependency
        self.use_cache = use_cache
        self.cache: Optional[T] = None

        # 自动包装依赖函数
        if not hasattr(dependency, '_depends_wrapped'):
            self._wrap_dependency(dependency)

    @staticmethod
    def _wrap_dependency(func: Callable):
        """创建支持依赖注入的包装函数"""

        @wraps(func)
        def wrapped(*args, **kwargs):
            return inject_call(func, *args, **kwargs)

        # 标记为已包装
        func._depends_wrapped = True
        # 替换原始函数
        module = inspect.getmodule(func)
        setattr(module, func.__name__, wrapped)
        return wrapped

    def __call__(self, *args, **kwargs) -> T:
        """透明调用依赖函数"""
        return inject_call(self.dependency, *args, **kwargs)

    def __repr__(self) -> str:
        return f"Depends({self.dependency.__name__})"
