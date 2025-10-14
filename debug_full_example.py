"""Debug the full example with text before bullets."""

import sys
sys.path.insert(0, '/Users/brianpugh/projects/rich-rst')

import docutils.io
import docutils.parsers.rst
import docutils.utils
import docutils.frontend
from rich.console import Console
from rich_rst import RSTVisitor

rst_content = """Enable or disable anti-aliasing. If ``True``, uses ``"msaa"``. If False,
disables anti_aliasing. If a string, should be one of the following:

* ``"ssaa"`` - Super-Sample Anti-Aliasing
* ``"msaa"`` - Multi-Sample Anti-Aliasing
* ``"fxaa"`` - Fast Approximate Anti-Aliasing"""

console = Console(width=70)

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

print("=" * 70)
print("RENDERABLES GENERATED:")
print("=" * 70)
for i, renderable in enumerate(visitor.renderables):
    print(f"{i}: {type(renderable).__name__}")
    if hasattr(renderable, 'plain'):
        print(f"   plain: {repr(renderable.plain)[:80]}...")
    if hasattr(renderable, 'end'):
        print(f"   end: {repr(renderable.end)}")
print()

print("=" * 70)
print("RENDERED OUTSIDE TABLE:")
print("=" * 70)
for renderable in visitor.renderables:
    console.print(renderable, end="")
print("\n")

print("=" * 70)
print("RENDERED IN TABLE WITH overflow='fold':")
print("=" * 70)
from rich.table import Table
from rich.console import Group
table = Table(show_header=False, box=None, padding=(0, 2, 0, 0), show_edge=False)
table.add_column("Col1", max_width=25)
table.add_column("Col2", overflow="fold")
table.add_row("option", Group(*visitor.renderables))
console.print(table)
