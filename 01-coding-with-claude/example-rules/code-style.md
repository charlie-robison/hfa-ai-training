# Python Code Style

## Formatting
- Use 4-space indentation (no tabs)
- Maximum line length: 88 characters (Black formatter default)
- Use trailing commas in multi-line collections
- One blank line between functions, two between classes

## Imports
- Group imports: stdlib, third-party, local — separated by blank lines
- Use absolute imports, not relative
- Never use `from module import *`

## Naming
- Variables and functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: prefix with single underscore `_method_name`
- Avoid single-letter variables except in comprehensions (`x`, `i`, `k`)

## Type Hints
- All function signatures must have type hints
- Use `list[str]` not `List[str]` (Python 3.10+ syntax)
- Use `X | None` not `Optional[X]`
- Use `dict[str, Any]` for loosely-typed dicts, Pydantic models for domain objects
