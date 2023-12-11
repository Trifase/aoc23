import os
from datetime import date
from itertools import combinations
# from pprint import pprint as pp

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


def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)


def intersecting_rows(x1: int, y1: int, x2: int, y2: int, empty_rows: set[int]) -> int:
    """
    Returns the number of empty rows crossed between the two points
    """
    if x1 == x2:
        return 0
    elif x1 > x2:
        x1, x2 = x2, x1
    return len([x for x in empty_rows if x1 < x < x2])


def intersecting_columns(x1: int, y1: int, x2: int, y2: int, empty_columns: set[int]) -> int:
    """
    Returns the number of empty columns crossed between the two points
    """
    if y1 == y2:
        return 0
    elif y1 > y2:
        y1, y2 = y2, y1
    return len([y for y in empty_columns if y1 < y < y2])


def get_galaxies(grid: list[list[str]]) -> tuple[set[tuple[int, int]], list[list[str]]]:
    galaxies = set()
    i = 1
    new_grid = []
    for y in range(len(grid)):
        new_line = list(grid[y])
        for x in range(len(grid[y])):
            if new_line[x] == "#":
                galaxies.add((y, x))
                new_line[x] = str(i)
                i += 1
        new_grid.append(new_line)
    return galaxies, new_grid


def calculate_distancies(
    grid: list[list[str]], galaxies: set[tuple[int, int]], empty_rows: set[int], empty_columns: set[int], expansion: int, debug: bool = False
) -> int:
    s = 0
    for pair in combinations(galaxies, 2):
        x1, y1 = pair[0]
        x2, y2 = pair[1]
        man_dist = manhattan_distance(x1, y1, x2, y2)
        rows = intersecting_rows(x1, y1, x2, y2, empty_rows)
        columns = intersecting_columns(x1, y1, x2, y2, empty_columns)

        if debug:
            print(
                f"{pair}\t{grid[x1][y1]}-{grid[x2][y2]} → {man_dist} ({rows} rows, {columns} columns) = {man_dist + (rows * expansion) + (columns * expansion)}"
            )

        s += man_dist + (rows * expansion) + (columns * expansion)
    return s


# Input parsing
print()
with Timer(name="Parsing", text="Parsing.....DONE: {milliseconds:.0f} ms"):
    """
    We'll parse the input line by line.
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=EXAMPLE)
    empty_rows = set()
    empty_columns = set()

    # We need to expand the empty rows
    new_data = []
    for index, line in enumerate(data):
        if all(x == "." for x in line):
            empty_rows.add(index)

    # for line in data:
    #     new_data.append(list(line))
    #     if all(x == '.' for x in line):
    #         new_data.append(list(line))

    # if a column is empty, we need to duplicate it
    # there is probably an easier way to do this
    for col_number in range(len(data[0])):
        col = [row[col_number] for row in data]
        if all(x == "." for x in col):
            empty_columns.add(col_number)
    # duplicate_columns = set()

    # for col_number in range(len(new_data[0])):
    #     col = [row[col_number] for row in new_data]
    #     if all(x == '.' for x in col):
    #         duplicate_columns.add(col_number)

    # for index in sorted(duplicate_columns, reverse=True):
    #     for row in new_data:
    #         row.insert(index, '.')

    data = [data, empty_rows, empty_columns]


# Part 1
@Timer(name="Part 1", text="Part 1......DONE: {milliseconds:.0f} ms")
def part1(data: any) -> int:
    data, empty_rows, empty_columns = data
    sol1 = 0

    galaxies, new_grid = get_galaxies(data)
    expansion = 1
    sol1 = calculate_distancies(new_grid, galaxies, empty_rows, empty_columns, expansion, debug=False)

    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2......DONE: {milliseconds:.0f} ms")
def part2(data: any) -> int:
    sol2 = 0

    data, empty_rows, empty_columns = data

    galaxies, new_grid = get_galaxies(data)
    expansion = 1_000_000 - 1
    sol2 = calculate_distancies(new_grid, galaxies, empty_rows, empty_columns, expansion, debug=False)

    return sol2


s1 = part1(data)
s2 = part2(data)

print()
print(f"=========:: [DAY {DAY}] ::=========")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
