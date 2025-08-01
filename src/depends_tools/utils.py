import inspect
from typing import Callable, Any, Dict
from functools import wraps
from .depends import Depends
from .resolver import DependencyResolver
from .context import DependencyContext
from .d_type import DependsType
from .call_factory import CallDependsFactory


def inject_call(func: Callable, *args, **kwargs) -> Any:
    """
    执行函数并自动解析依赖

    Args:
        func: 目标函数
        *args: 位置参数
        **kwargs: 关键字参数

    Returns:
        函数执行结果
    """
    context = DependencyResolver.get_context()

    # 如果是Depends实例，获取实际依赖函数
    dependency_func = func
    if isinstance(func, Depends):
        dependency_func = func.dependency

    # 检查循环依赖
    if dependency_func in context.resolving:
        call_stack = [f.__name__ for f in context.resolving]
        call_stack.append(dependency_func.__name__)
        raise RuntimeError(f"循环依赖: {' -> '.join(call_stack)}")

    context.resolving.add(dependency_func)
    try:
        # 获取函数签名
        signature = inspect.signature(dependency_func)

        # 绑定参数
        try:
            bound_args = signature.bind(*args, **kwargs)
        except TypeError:
            # 使用部分绑定处理参数不完整的情况
            bound_args = signature.bind_partial(*args, **kwargs)
        bound_args.apply_defaults()
        final_kwargs = bound_args.arguments.copy()

        # 解析参数依赖
        for param_name, param_value in list(final_kwargs.items()):
            # 处理依赖项参数
            if isinstance(param_value, Depends):
                # 确保依赖函数被包装
                if not hasattr(param_value.dependency, '_depends_wrapped'):
                    Depends(param_value.dependency)
                # 解析依赖值
                resolved = _resolve_dependency(param_value.dependency, context)
                final_kwargs[param_name] = resolved

        # 处理未提供的依赖项默认值
        for param_name, param in signature.parameters.items():
            if (param_name not in final_kwargs and
                    isinstance(param.default, Depends)):
                # 确保依赖函数被包装
                if not hasattr(param.default.dependency, '_depends_wrapped'):
                    Depends(param.default.dependency)
                # 解析依赖值
                resolved = _resolve_dependency(param.default.dependency, context)
                final_kwargs[param_name] = resolved

        # 调用目标函数
        factory = _call_dependency(dependency_func)
        return factory.get_result(dependency_func, final_kwargs)

    finally:
        # 从解析集合中移除
        if dependency_func in context.resolving:
            context.resolving.remove(dependency_func)


def _call_dependency(dependency_func: Callable):
    if inspect.isasyncgenfunction(dependency_func):
        func_type = DependsType.async_generate
    elif inspect.iscoroutinefunction(dependency_func):
        func_type = DependsType.async_func
    elif inspect.isgeneratorfunction(dependency_func):
        func_type = DependsType.sync_generate
    else:
        func_type = DependsType.sync_func
    return CallDependsFactory.get(func_type)()


def _resolve_dependency(depends_func: Callable, context: DependencyContext) -> Any:
    """解析单个依赖项"""
    # 1. 检查是否有覆盖值
    if depends_func in context.overrides:
        return context.overrides[depends_func]

    # 2. 检查缓存
    if depends_func in context.cache:
        return context.cache[depends_func]

    # 3. 递归解析依赖函数
    result = inject_call(depends_func)

    # 4. 缓存结果
    context.cache[depends_func] = result

    return result


# 创建透明调用的包装函数
def inject(func: Callable) -> Callable:
    """使函数支持透明依赖注入的装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return inject_call(func, *args, **kwargs)

    return wrapper
