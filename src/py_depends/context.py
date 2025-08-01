import threading
from typing import Dict, Callable, Any, Set


# 线程局部的依赖解析上下文
# THREAD LOCAL DEPENDENCY PARSING CONTEXT
class DependencyContext(threading.local):
    __slots__ = ("cache", "overrides", "resolving")

    def __init__(self):
        self.cache: Dict[Callable, Any] = {}
        self.overrides: Dict[Callable, Any] = {}
        self.resolving: Set[Callable] = set()
