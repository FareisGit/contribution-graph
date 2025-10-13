#!/usr/bin/env python3
"""Rebuild the contribution grid from the dates actually present in git log."""
import datetime, sys

GRID_COLS, GRID_ROWS = 53, 7

days = set()
with open(sys.argv[1]) as fh:
    for line in fh:
        line = line.strip()
        if line:
            days.add(datetime.date.fromisoformat(line))

today = datetime.date.today()
last_sunday = today - datetime.timedelta(days=(today.weekday() + 1) % 7)
start = last_sunday - datetime.timedelta(weeks=GRID_COLS - 1)

grid = [[" "] * GRID_COLS for _ in range(GRID_ROWS)]
placed = 0
for d in sorted(days):
    delta = (d - start).days
    if delta < 0:
        print("OUT OF RANGE (too old): %s" % d); continue
    col, row = divmod(delta, 7)
    if col >= GRID_COLS:
        print("OUT OF RANGE (too new): %s" % d); continue
    grid[row][col] = "#"
    placed += 1

labels = "SMTWTFS"
print("    +" + "-" * GRID_COLS + "+")
for y in range(GRID_ROWS):
    print("  %s |%s|" % (labels[y], "".join(grid[y])))
print("    +" + "-" * GRID_COLS + "+")
print("\nplaced %d/%d days in grid" % (placed, len(days)))
print("future-dated days: %d" % sum(1 for d in days if d >= today))
