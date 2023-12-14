import os
from copy import deepcopy

# from pprint import pprint as pp
from datetime import date

from codetiming import Timer
from icecream import ic

from utils import SESSIONS, get_data

# YEAR will be the current year, DAY will be the current file name.
YEAR = date.today().year
DAY = int(os.path.basename(__file__).split(".")[0])

# Used to overwrite the year and day
# YEAR = 2016
# DAY = 4

EXAMPLE = False
INFO = True
DEBUG = True

if DEBUG:
    ic.enable()
else:
    ic.disable()


def pprint(data: any) -> None:
    if INFO:
        print(data)


def rotate_ccw(grid: list) -> list:
    """
    Rotate the grid clockwise 90 degrees.
    """
    return list(reversed(list(zip(*grid))))


def rotate_cw(grid: list) -> list:
    """
    Yes, I know.
    """
    for _ in range(3):
        grid = list(reversed(list(zip(*grid))))
    return grid


def push(grid: list) -> list:
    """
    We push the rock left. We do this by making a string of every row, splitting it for #, ordering the substrings, put everything back.
    """
    new_grid = []

    for line in grid:
        line = "".join(line)
        split = line.split("#")

        new_line = []
        for i in split:
            i = list(i)
            i.sort(reverse=True)
            new_line.append("".join(i))

        new_grid.append(list("#".join(new_line)))

    return new_grid


def full_cycle(grid: list) -> list:
    """
    This is just a full cycle of pushing, rotating, pushing etc. We do the four directions: north, west, south, east.
    """

    # north
    grid = rotate_ccw(grid)
    grid = push(grid)
    grid = rotate_cw(grid)

    # west
    grid = push(grid)

    # south
    grid = rotate_cw(grid)
    grid = push(grid)
    grid = rotate_ccw(grid)

    # east
    grid = rotate_ccw(grid)
    grid = rotate_ccw(grid)
    grid = push(grid)
    grid = rotate_ccw(grid)
    grid = rotate_ccw(grid)

    return grid


def make_string(grid: list) -> str:
    """
    First world function to make a string of the grid.
    """
    string = ""
    for line in grid:
        string += "".join(line)
    return string


# Input parsing
print()
with Timer(name="Parsing", text="Parsing.....DONE: {milliseconds:.0f} ms"):
    """
    We'll parse the input line by line. We'll return the grid (a list of lists), the empty rows and the empty columns sets.
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=EXAMPLE)
    data = [list(line) for line in data]


# Part 1
@Timer(name="Part 1", text="Part 1......DONE: {milliseconds:.0f} ms")
def part1(data: any) -> int:
    """
    Ok, here is the deal: pushing up is hard. Pushing left is easy. So we rotate the grid, push left, rotate it back.

    Rotate the grid 90 CCW
    Make a string of every row. split for #.
    For each 'substring', make it a list and order so that O are on the left. Rebuild the row.
    rotate the whole grid 90 CW back
    """

    sol1 = 0

    grid = data
    # Rotate it
    grid = rotate_ccw(grid)

    # Push it
    new_grid = push(grid)

    # Rotate back.. it :/
    new_grid = rotate_cw(new_grid)

    # We calculate the value of north load something something
    value = len(new_grid)

    for line in new_grid:
        line = "".join(line)
        sol1 += line.count("O") * value
        value -= 1

    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2......DONE: {milliseconds:.0f} ms")
def part2(data: any) -> int:
    """
    Ok, 1_000_000_000 iteration of a 4 pushing cycle are just too much. We need to find a pattern.
    We'll cycle the grid until we find a pattern. Then we'll calculate the number of iteration needed to reach 1_000_000_000
    and we'll cycle the grid again for that number of iteration.
    """

    sol2 = 0

    # We save the 'initial grid' and we'll cycle that one after we found the period length.
    original_grid = deepcopy(data)

    # We search the period.
    grid = data
    found = False
    i = 0
    first_index = 0
    period = 0
    grids = []

    while found is False:  # we do until we found the period. Hopefully.
        grid = full_cycle(grid)  # This is the 4 pushing cycle: north, west, south, east
        gridstr = make_string(grid)  # We make a long string of the whole grid, it's just easier to store and compare.
        if gridstr in grids:
            found = True
            period = i - grids.index(gridstr)  # Length of the period
            first_index = grids.index(gridstr)  # Start of the period
            break
        else:
            grids.append(gridstr)
        i += 1

    # We calculate the total number of iteration needed to reach 1_000_000_000, shortened by the period cycles.
    total_iteration = first_index + ((1_000_000_000 - first_index) % period)

    # We pick it up from the original grid
    grid = original_grid

    for _ in range(total_iteration):
        grid = full_cycle(grid)

    # We calculate the value of north load something something
    value = len(grid)
    for line in grid:
        line = "".join(line)
        sol2 += line.count("O") * value
        value -= 1

    return sol2


s1 = part1(data)
s2 = part2(data)

print()
print(f"=========:: [DAY {DAY}] ::=========")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
