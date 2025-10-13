# contribution-graph

The GitHub contribution graph is just a 53x7 grid of dates, so you can treat it
as a very slow, very low-resolution display. This repo draws on it.

```
#  # ### #   #    ##    #   #  ##  ###  #   ###    #
#  # #   #   #   #  #   #   # #  # #  # #   #  #   #
#### ##  #   #   #  #   # # # #  # ###  #   #  #   #
#  # #   #   #   #  #   ## ## #  # # #  #   #  #
#  # ### ### ###  ##    #   #  ##  #  # ### ###    #
```

## How it works

Columns are weeks, rows are days, and column 0 starts on the Sunday 52 weeks
before the most recent Sunday. So every cell maps to exactly one date:

```
date = start_sunday + 7 * column + row  (in days)
```

`gen_art.py` rasterises text through a 5-row variable-width font and writes out
one timestamped line per commit. `build_art_repo.sh` replays that into a git
history with `git commit-tree`, which builds the objects directly instead of
staging a file a thousand times over. `verify.py` then reads the dates back out
of the finished repo and redraws the grid, because getting the Sunday offset
wrong is very easy and very invisible.

A fixed-width font will not fit — "HELLO WORLD !" needs all 52 usable columns
even with variable widths, and the W is the whole problem.

## A caveat worth knowing

Shading is relative to your own busiest day, so a uniform number of commits per
cell gives a uniform colour. It also means a genuinely busy week later on will
wash the drawing out.

The graph is a sliding window too, so this erodes from the left by one column a
week. `refresh.sh` regenerates and re-centres it.

## Honesty note

These commits are decorative. They contain no work and are not meant to imply
any was done on those dates — the dates *are* the drawing. Real projects live in
the other repos here.

## Running it

```bash
python3 gen_art.py "HELLO WORLD !" 10 > plan.txt
./build_art_repo.sh ./out plan.txt "Your Name" "you@example.com"
```
