import os

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


def get_column(grid: list[str], index: int) -> list[str]:
    column = []
    for row in grid:
        column.append(row[index])
    column = list(reversed(column))
    column = "".join(column)
    return column


def check_mirroring(pattern: list[str], index: int, old_h_mirroring_index=None, old_v_mirroring_index=None, vertical=False) -> bool:
    left = pattern[:index]
    right = pattern[index:]

    left.reverse()

    # For part 2: we skip the old mirroring indexes, because they can still be valid
    if not vertical and old_h_mirroring_index and index == old_h_mirroring_index:
        return False

    if vertical and old_v_mirroring_index and index == old_v_mirroring_index:
        return False

    is_ok = False

    if len(left) == len(right):
        is_ok = left == right

    elif len(left) < len(right):
        is_ok = all([left[i] == right[i] for i in range(len(left))])

    else:
        is_ok = all([right[i] == left[i] for i in range(len(right))])
    return is_ok


def find_mirroring(pattern: list[str], old_h_mirroring_index=None, old_v_mirroring_index=None, vertical=False) -> int:
    for i in range(len(pattern) - 1):
        index = None
        if pattern[i] == pattern[i + 1]:

            index = i + 1  # 1 indexing
            if check_mirroring(pattern, index, old_h_mirroring_index, old_v_mirroring_index, vertical):
                break
            else:
                index = None

    return index


def print_pattern(pattern, list=False):
    print(f'{"="*len(pattern[0])}')
    for line in pattern:
        if list:
            print("".join(line))
        else:
            print(line)
    print(f'{"="*len(pattern[0])}')


def rotate_pattern(pattern):
    new_pattern = []
    for i in range(len(pattern[0])):
        column = get_column(pattern, i)
        new_pattern.append(column)
    return new_pattern


def complete_mirroring(pattern, n_pattern, old_h_mirroring_index=None, old_v_mirroring_index=None):
    h_mirroring_index = None
    v_mirroring_index = None

    h_mirroring_index = find_mirroring(pattern, old_h_mirroring_index, old_v_mirroring_index)
    if not h_mirroring_index:
        v_pattern = rotate_pattern(pattern)
        v_mirroring_index = find_mirroring(v_pattern, old_h_mirroring_index, old_v_mirroring_index, vertical=True)

    return h_mirroring_index, v_mirroring_index


# Input parsing
print()
with Timer(name="Parsing", text="Parsing.....DONE: {milliseconds:.0f} ms"):
    """
    We'll parse the input line by line. We'll return the grid (a list of lists), the empty rows and the empty columns sets.
    """

    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=EXAMPLE)
    patterns = []
    pattern = []
    for line in data:
        if line == "":
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(line)

    # last pattern:
    patterns.append(pattern)

    data = patterns


# Part 1
@Timer(name="Part 1", text="Part 1......DONE: {milliseconds:.0f} ms")
def part1(data: any) -> int:
    sol1 = 0
    columns_left = 0
    rows_above = 0

    for n_pattern, pattern in enumerate(data):
        h_mirroring_index, v_mirroring_index = complete_mirroring(pattern, n_pattern)

        if h_mirroring_index:
            rows_above += h_mirroring_index

        if v_mirroring_index:
            columns_left += v_mirroring_index

    sol1 = columns_left + (100 * rows_above)
    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2......DONE: {milliseconds:.0f} ms")
def part2(data: any) -> int:
    sol2 = 0
    columns_left = 0
    rows_above = 0

    old_indexes = {}

    for n_pattern, pattern in enumerate(data):
        # First pass - we get the 'old' mirror lines
        old_h_mirroring_index, old_v_mirroring_index = complete_mirroring(pattern, n_pattern)

        old_indexes[n_pattern] = {}
        if old_h_mirroring_index:
            old_indexes[n_pattern]["h"] = old_h_mirroring_index

        if old_v_mirroring_index:
            old_indexes[n_pattern]["v"] = old_v_mirroring_index

        # Second pass - iterate the smudges until we find a new mirroring
        new_h_mirroring_index = None
        new_v_mirroring_index = None
        new_mirror_found = False

        while not new_mirror_found:
            for y in range(len(pattern)):
                if new_mirror_found:
                    break
                for x in range(len(pattern[0])):
                    pattern_clone = [list(line) for line in pattern]

                    # we flip a bit
                    if pattern_clone[y][x] == "#":
                        pattern_clone[y][x] = "."
                    else:
                        pattern_clone[y][x] = "#"

                    # we pass the old mirroring indexes, both horizontal and vertical - so that the function that checks for mirroring can skip them, because they can still be valid
                    new_h_mirroring_index, new_v_mirroring_index = complete_mirroring(
                        pattern_clone, n_pattern, old_h_mirroring_index, old_v_mirroring_index
                    )

                    if (new_h_mirroring_index != old_h_mirroring_index and new_h_mirroring_index is not None) or (
                        new_v_mirroring_index != old_v_mirroring_index and new_v_mirroring_index is not None
                    ):
                        new_mirror_found = True
                        break

            if new_h_mirroring_index:
                rows_above += new_h_mirroring_index
            if new_v_mirroring_index:
                columns_left += new_v_mirroring_index

    sol2 = columns_left + (100 * rows_above)
    return sol2


s1 = part1(data)
s2 = part2(data)

print()
print(f"=========:: [DAY {DAY}] ::=========")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
