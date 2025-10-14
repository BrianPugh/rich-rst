"""Test the fix with local rich-rst."""

import sys
sys.path.insert(0, '/Users/brianpugh/projects/rich-rst')

from rich.console import Console
from rich.table import Table
from rich_rst import RestructuredText

console = Console(width=60)

rst_bullets = """* Item 1
* Item 2
* Item 3"""

print("=" * 60)
print("Test with overflow='fold' (should now work)")
print("=" * 60)
table = Table(show_header=False, box=None, padding=(0, 1, 0, 0), show_edge=False)
table.add_column("Col1", max_width=15)
table.add_column("Col2", overflow="fold")
table.add_row("rst", RestructuredText(rst_bullets, show_errors=False))
console.print(table)
print()
