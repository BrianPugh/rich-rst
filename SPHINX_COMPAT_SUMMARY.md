# Sphinx Role Compatibility - Implementation Summary

## Problem

The user reported an error when rendering RST markup that contained Sphinx-specific roles:

```rst
:func:`Plotter.screenshot <pyvista.Plotter.screenshot>`
```

This resulted in the error:
```
Unknown interpreted text role "func".
```

## Root Cause

Sphinx roles like `:func:`, `:meth:`, `:class:`, etc. are **extremely common** in Python docstrings across the ecosystem (numpy, scipy, matplotlib, pandas, etc.), but they are **not available in standard docutils**. When rich-rst encountered these roles, it would show scary red ERROR panels.

This is poor UX since these roles are essentially standard Python documentation conventions.

## Solution

Added a `sphinx_compat` parameter (default `True`) to the `RestructuredText` class that:

1. Registers common Sphinx roles (func, meth, class, mod, attr, obj, data, const, exc, var, type, etc.)
2. Renders them as inline code/literal text instead of throwing errors
3. Registers them in both the canonical role registry and the language module to avoid INFO messages

## Usage

### Default Behavior (Sphinx Compatible)

```python
from rich_rst import RestructuredText
from rich.console import Console

docstring = '''
See :func:`numpy.array` and :class:`numpy.ndarray` for details.
'''

console = Console()
rst = RestructuredText(docstring)  # sphinx_compat=True by default
console.print(rst)
```

Output: Roles render cleanly as inline code without errors.

### Disable Sphinx Compatibility

```python
rst = RestructuredText(docstring, sphinx_compat=False, show_errors=True)
console.print(rst)
```

Output: Shows "Unknown interpreted text role" errors as before.

## Implementation Details

### Registered Sphinx Roles

- **Python Domain**: func, function, meth, method, class, mod, module, attr, attribute
- **Generic**: obj, object, data, const, constant, exc, exception, var, variable, type
- **Prefixed**: py:func, py:meth, py:class, py:mod, py:attr, py:obj, py:data, py:const, py:exc

### Code Location

- `rich_rst/__init__.py:70-131` - `_register_sphinx_roles()` function
- `rich_rst/__init__.py:628-631` - `sphinx_compat` parameter documentation
- `rich_rst/__init__.py:655-656` - Role registration on render

## Test Coverage

Created two complementary test files:

### 1. `tests/test_vectors/sphinx_roles_compat.rst` (NEW)
**Configuration:** `sphinx_compat=True` (the default)

Demonstrates the **clean rendering** that users see by default:
- All common Sphinx roles (:func:, :meth:, :class:, :mod:, etc.)
- Python domain roles (:py:func:, :py:class:, etc.)
- Mixed content with other RST markup
- Realistic Python docstring example

**Output:** Sphinx roles render as inline code without any errors.

### 2. `tests/test_vectors/unknown_role_func.rst` (UPDATED)
**Configuration:** `sphinx_compat=False`

Demonstrates the **error behavior** for troubleshooting:
1. How Sphinx roles appear with `sphinx_compat=False` (shows errors)
2. Edge case: malformed markup without backticks (parsed as field list)
3. Comparison with normal inline code blocks

**Output:** Sphinx roles show "Unknown interpreted text role" errors.

### Test Comparison

| Aspect | sphinx_roles_compat.rst | unknown_role_func.rst |
|--------|------------------------|----------------------|
| Purpose | Show clean rendering | Show error behavior |
| Config | `sphinx_compat=True` | `sphinx_compat=False` |
| Output | Inline code | Error panels |
| Use Case | Default user experience | Troubleshooting |

## Benefits

1. **Better UX**: Python docstrings with Sphinx markup render cleanly by default
2. **No Breaking Changes**: Existing code continues to work
3. **Opt-Out Available**: Users can disable with `sphinx_compat=False` if needed
4. **Common Patterns Supported**: Covers all major Sphinx roles used in Python documentation

## Example Output

Before (with `sphinx_compat=False`):
```
:func:`test_function`
╭──────────────── System Message: Problematic Element ─────────────────╮
│ :func:`test_function`                                                │
╰───────────────────────────────────────────────────────────────────────╯
╭─────────── System Message: ERROR/3 (<rst-document>, line 1) ─────────╮
│ Unknown interpreted text role "func".                                │
╰───────────────────────────────────────────────────────────────────────╯
```

After (with `sphinx_compat=True`, the default):
```
test_function  ← rendered as inline code, no errors
```
