from typing import Callable
from functools import wraps
from .injector import inject_call


# 创建透明调用的包装函数
def inject(func: Callable) -> Callable:
    """使函数支持透明依赖注入的装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return inject_call(func, *args, **kwargs)

    return wrapper
