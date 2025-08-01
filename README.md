# py-depends

A lightweight and elegant Python dependency injection framework.

## Features

- 🚀 Simple and intuitive API
- 🔄 Support for both sync and async dependencies
- 🏭 Factory pattern support
- 🎯 Type-safe dependency resolution
- 📦 Zero external dependencies
- 🧪 Comprehensive test coverage

## Installation

```bash
pip install depends-tools
```

## Quick Start

```python
from depends_tools import Depends, inject

# Define a dependency
def get_database():
    return "database_connection"

# Use the dependency
@inject
def get_user(db=Depends(get_database)):
    return f"User from {db}"

# Resolve dependencies
result = get_user()
print(result)  # Output: User from database_connection
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/JokerCrying/py-depends-tools/issues) on GitHub.