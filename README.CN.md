# py-depends

一个轻量级且优雅的Python依赖注入框架。

## 特性

- 🚀 简单直观的API
- 🔄 支持同步和异步依赖
- 🏭 支持工厂模式
- 🎯 类型安全的依赖解析
- 📦 零外部依赖
- 🧪 全面的测试覆盖

## 安装

```bash
pip install py-depends
```

## 快速开始

```python
from py_depends import Depends, inject

# 定义一个依赖
def get_database():
    return "database_connection"

# 使用依赖
@inject
def get_user(db=Depends(get_database)):
    return f"User from {db}"

# 解析依赖
result = get_user()
print(result)  # 输出: User from database_connection
```

## 许可证

本项目采用MIT许可证 - 详情请查看[LICENSE](LICENSE)文件。

## 支持

如果您遇到任何问题或有疑问，请在GitHub上[提交issue](https://github.com/JokerCrying/py-depends/issues)。