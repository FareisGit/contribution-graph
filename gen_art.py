#!/usr/bin/env python3
"""
Generate a GitHub contribution-graph pixel-art commit plan.

The GitHub contribution graph is a 53-column x 7-row grid.
  - Column 0 is the week containing the Sunday 52 weeks before the most
    recent Sunday.
  - Row 0 is Sunday, row 6 is Saturday.

This script rasterises text into that grid with a variable-width 5-row
font and emits one (date, n_commits) pair per lit pixel.
"""

import datetime
import sys

# ---------------------------------------------------------------- font
# 5 rows tall, variable width. 1 = lit pixel.
FONT = {
    "H": ["1001", "1001", "1111", "1001", "1001"],
    "E": ["111", "100", "110", "100", "111"],
    "L": ["100", "100", "100", "100", "111"],
    "O": ["0110", "1001", "1001", "1001", "0110"],
    "W": ["10001", "10001", "10101", "11011", "10001"],
    "R": ["1110", "1001", "1110", "1010", "1001"],
    "D": ["1110", "1001", "1001", "1001", "1110"],
    "!": ["1", "1", "1", "0", "1"],
    " ": ["0", "0", "0", "0", "0"],
}

GRID_COLS = 53
GRID_ROWS = 7
TOP_PAD = 1          # leave row 0 (Sunday) blank so the art is vertically centred
CHAR_GAP = 1


def rasterise(text):
    """Return a list of columns, each a 7-char string of '0'/'1'."""
    cols = []
    for i, ch in enumerate(text.upper()):
        if ch not in FONT:
            raise SystemExit("No glyph for %r" % ch)
        glyph = FONT[ch]
        width = len(glyph[0])
        for x in range(width):
            col = ["0"] * GRID_ROWS
            for y in range(5):
                if glyph[y][x] == "1":
                    col[TOP_PAD + y] = "1"
            cols.append("".join(col))
        if i != len(text) - 1:
            cols.extend(["0" * GRID_ROWS] * CHAR_GAP)
    return cols


def graph_start_sunday(today):
    """The Sunday that column 0 of the contribution graph begins on."""
    # weekday(): Mon=0 .. Sun=6
    days_since_sunday = (today.weekday() + 1) % 7
    last_sunday = today - datetime.timedelta(days=days_since_sunday)
    return last_sunday - datetime.timedelta(weeks=GRID_COLS - 1)


def preview(cols, offset):
    grid = [[" "] * GRID_COLS for _ in range(GRID_ROWS)]
    for x, col in enumerate(cols):
        for y, bit in enumerate(col):
            if bit == "1":
                grid[y][offset + x] = "#"
    labels = "SMTWTFS"
    out = ["    +" + "-" * GRID_COLS + "+"]
    for y in range(GRID_ROWS):
        out.append("  %s |%s|" % (labels[y], "".join(grid[y])))
    out.append("    +" + "-" * GRID_COLS + "+")
    return "\n".join(out)


def main():
    text = sys.argv[1] if len(sys.argv) > 1 else "HELLO WORLD !"
    per_pixel = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    today = datetime.date.today()

    cols = rasterise(text)
    width = len(cols)
    usable = GRID_COLS - 1          # keep the final (partial) week clear
    if width > usable:
        raise SystemExit(
            "Art is %d columns wide; only %d fit in the graph." % (width, usable)
        )
    offset = (usable - width) // 2

    start = graph_start_sunday(today)

    sys.stderr.write("text        : %s\n" % text)
    sys.stderr.write("width       : %d columns (max %d)\n" % (width, usable))
    sys.stderr.write("offset      : %d columns\n" % offset)
    sys.stderr.write("graph begins: %s (Sunday)\n" % start)
    sys.stderr.write("commits/px  : %d\n\n" % per_pixel)
    sys.stderr.write(preview(cols, offset) + "\n\n")

    import random
    rng = random.Random(20261013)
    pool = [l.rstrip("\n") for l in open("messages.txt") if l.strip()]

    lit = 0
    emitted = 0
    recent = []
    for x, col in enumerate(cols):
        for y, bit in enumerate(col):
            if bit != "1":
                continue
            day = start + datetime.timedelta(days=(offset + x) * 7 + y)
            if day >= today:
                raise SystemExit("Computed a future date (%s); aborting." % day)
            lit += 1

            # a plausible working day: a few commits clustered, not a metronome
            minute = rng.randint(8 * 60 + 30, 15 * 60)
            for _ in range(per_pixel):
                minute += rng.randint(4, 40)
                msg = rng.choice(pool)
                while msg in recent:
                    msg = rng.choice(pool)
                recent.append(msg)
                if len(recent) > 12:
                    recent.pop(0)
                print("%sT%02d:%02d:%02d+00:00\t%s"
                      % (day.isoformat(), minute // 60, minute % 60,
                         rng.randint(0, 59), msg))
                emitted += 1

    sys.stderr.write("lit pixels  : %d\n" % lit)
    sys.stderr.write("commits     : %d\n" % emitted)


if __name__ == "__main__":
    main()
