from .context import DependencyContext


# 单例依赖解析器
# SINGLETON DEPENDENCY PARSER
class DependencyResolver:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.context = DependencyContext()
        return cls._instance

    @classmethod
    def get_context(cls) -> DependencyContext:
        if not cls._instance:
            cls._instance = cls()
        return cls._instance.context