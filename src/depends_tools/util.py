from functools import wraps
from .injector import inject_call
from .d_type import F


# 创建透明调用的包装函数
def inject(func: F) -> F:
    """使函数支持透明依赖注入的装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return inject_call(func, *args, **kwargs)  # type: ignore

    return wrapper  # type: ignore
