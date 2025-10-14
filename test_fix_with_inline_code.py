"""Test the fix with the full cyclopts example (inline code in bullets)."""

import sys
sys.path.insert(0, '/Users/brianpugh/projects/rich-rst')

from rich.console import Console
from rich.table import Table
from rich_rst import RestructuredText

rst_content = """Enable or disable anti-aliasing. If ``True``, uses ``"msaa"``. If False,
disables anti_aliasing. If a string, should be one of the following:

* ``"ssaa"`` - Super-Sample Anti-Aliasing
* ``"msaa"`` - Multi-Sample Anti-Aliasing
* ``"fxaa"`` - Fast Approximate Anti-Aliasing"""

console = Console(width=70)

print("=" * 70)
print("CONTROL: RST rendered outside table (works correctly)")
print("=" * 70)
console.print(RestructuredText(rst_content, show_errors=False))

print("\n" + "=" * 70)
print("FIX: RST in table with overflow='fold' (should now work)")
print("=" * 70)
table = Table(show_header=False, box=None, padding=(0, 2, 0, 0), show_edge=False)
table.add_column("Option", style="cyan", max_width=25)
table.add_column("Description", overflow="fold")
table.add_row(
    "--anti-aliasing\n  --no-anti-aliasing",
    RestructuredText(rst_content, show_errors=False)
)
console.print(table)
print()
