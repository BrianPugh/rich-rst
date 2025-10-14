"""Debug what renderables are generated for bullet lists."""

import docutils.io
import docutils.parsers.rst
import docutils.utils
import docutils.frontend
from rich.console import Console
from rich_rst import RSTVisitor

rst_content = """* Item 1
* Item 2
* Item 3"""

console = Console(width=60)

# Parse RST
if hasattr(docutils.frontend, 'get_default_settings'):
    settings = docutils.frontend.get_default_settings(docutils.parsers.rst.Parser)
else:
    settings = docutils.frontend.OptionParser(components=(docutils.parsers.rst.Parser,)).get_default_values()
settings.report_level = 69
source = docutils.io.StringInput(rst_content)
document = docutils.utils.new_document("<test>", settings)
rst_parser = docutils.parsers.rst.Parser()
rst_parser.parse(source.read(), document)

# Visit and render
visitor = RSTVisitor(document, console=console)
document.walkabout(visitor)

print("=" * 60)
print("RENDERABLES GENERATED:")
print("=" * 60)
for i, renderable in enumerate(visitor.renderables):
    print(f"{i}: {type(renderable).__name__}: {repr(renderable)}")
    if hasattr(renderable, 'plain'):
        print(f"   plain: {repr(renderable.plain)}")
    if hasattr(renderable, 'end'):
        print(f"   end: {repr(renderable.end)}")
print()

print("=" * 60)
print("RENDERED OUTSIDE TABLE:")
print("=" * 60)
for renderable in visitor.renderables:
    console.print(renderable, end="")
print("\n")

print("=" * 60)
print("RENDERED IN TABLE WITH overflow='fold':")
print("=" * 60)
from rich.table import Table
table = Table(show_header=False, box=None, padding=(0, 1, 0, 0), show_edge=False)
table.add_column("Col1", max_width=15)
table.add_column("Col2", overflow="fold")

# Try grouping all renderables
from rich.console import Group
table.add_row("rst", Group(*visitor.renderables))
console.print(table)
