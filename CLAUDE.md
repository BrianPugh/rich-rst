# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

rich-rst is a Python library that renders reStructuredText (RST) documents with rich formatting using the `rich` library. It supports 75 RST elements and provides both a Python API and CLI interface.

## Core Architecture

### Main Components

1. **RSTVisitor** (rich_rst/__init__.py:71): The central visitor pattern implementation that walks the docutils AST and converts RST nodes to Rich renderables. Each `visit_*` method handles a specific RST element type (paragraphs, titles, code blocks, lists, etc.).

2. **RestructuredText** (rich_rst/__init__.py:554): The main public class that implements Rich's rendering protocol (`__rich_console__`). It parses RST markup using docutils and delegates rendering to RSTVisitor.

3. **MLStripper** (rich_rst/__init__.py:48): HTML parser utility for stripping HTML tags from raw HTML sources.

### Rendering Flow

1. RST markup → docutils parser → document AST
2. RSTVisitor walks the AST via `document.walkabout(visitor)`
3. Each visited node is converted to Rich renderables (Text, Panel, Table, etc.)
4. Renderables are collected in `visitor.renderables` list
5. Rich console renders the final output

### Key Design Patterns

- **Visitor Pattern**: RSTVisitor extends docutils.nodes.SparseNodeVisitor to handle different RST node types
- **Deferred References**: `refname_to_renderable` dict maps reference names to their renderables for later URL assignment in `visit_target()`
- **Style Customization**: All styling uses `console.get_style()` with fallback defaults, allowing theme customization

## Development Commands

### Setup
```bash
pip install -e .
pip install pytest pytest-coverage
```

### Testing
```bash
# Run all tests with coverage
python -m pytest --cov=rich_rst --cov-report term --cov-report xml

# Run single test file
python -m pytest tests/test_main.py

# Run specific test
python -m pytest tests/test_main.py::test_main[tests/test_vectors/example.rst]
```

The test suite uses snapshot testing with HTML output comparison. Test vectors are in `tests/test_vectors/*.rst` with expected output in `*_expected.html` files.

### Running the CLI
```bash
# Render a file
python -m rich_rst path/to/file.rst

# From stdin
echo "**bold text**" | python -m rich_rst -

# With options
python -m rich_rst file.rst --code-theme dracula --guess-lexer --hide-errors
```

### Building Documentation
```bash
cd docs
make html
```

### Version Management

This project uses `setuptools_scm` for automatic version management from git tags. Version is written to `rich_rst/_version.py`.

## Code Organization

- `rich_rst/__init__.py`: Core library implementation (visitor, parser, renderer)
- `rich_rst/__main__.py`: CLI entry point with argparse interface
- `tests/test_main.py`: Snapshot-based HTML comparison tests
- `tests/test_vectors/`: RST test files and expected HTML outputs

## Important Implementation Details

### Lexer Detection for Code Blocks

The `_find_lexer()` method (rich_rst/__init__.py:99) determines syntax highlighting:
1. Check node classes (e.g., `.. code:: python`)
2. If `guess_lexer=True`, use pygments to guess from content
3. Fall back to `default_lexer` (usually "python")

### Reference Handling

References are two-pass:
1. `visit_reference()` creates styled text and stores position in `refname_to_renderable`
2. `visit_target()` updates the style with the actual URL

### Text Concatenation

Adjacent text elements are merged to maintain proper spacing. Check `isinstance(self.renderables[-1], Text)` before appending.

### Special Characters

- Superscript/subscript use Unicode translation tables (rich_rst/__init__.py:86-92)
- Newlines in text content are replaced with spaces to prevent layout breaks

## Testing Notes

Tests use parameterized fixtures that iterate over all `.rst` files in `tests/test_vectors/`. To add a test:
1. Create `tests/test_vectors/new_feature.rst`
2. Run test once to generate `new_feature_actual.html`
3. Verify output is correct
4. Rename to `new_feature_expected.html`
5. Test will now compare against expected output
