from codetiming import Timer
from dataclassy import dataclass
from icecream import ic
from rich import print

from utils import SESSIONS, get_data, get_neighbors, make_grid

YEAR = 2023
DAY = 3

EXAMPLE = False
INFO = True
DEBUG = True

if DEBUG:
    ic.enable()
else:
    ic.disable()


def pprint(data):
    if INFO:
        print(data)


@dataclass
class PartNumber:
    number: int
    coords: list
    grid: list
    neighbors: list = None
    is_gear: bool = False
    has_symbol: bool = False
    gear_coords: tuple = None

    def __str__(self):
        return f"Number {self.number} at {self.coords}"


# Input parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    """
    We'll parse the input line by line, make a grid. Then we'll find the numbers and their coordinates, computate some data, and put into a list.
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=EXAMPLE)

    grid = make_grid(data)

    numbers = []

    # find the numbers
    for y in range(len(grid)):
        line = grid[y]
        number_found = False

        for x in range(len(line)):
            if line[x].isdigit() and not number_found:
                number_found = True
                number = []
                number.append((y, x))

            elif line[x].isdigit() and number_found:
                number.append((y, x))

            elif not line[x].isdigit() and number_found:
                number_found = False
                numbers.append(
                    PartNumber(
                        number=int("".join(grid[y][x] for y, x in number)),
                        coords=number,
                        grid=grid,
                    )
                )

            # edge case: the last number of the line
            if x == len(line) - 1 and number_found:
                number_found = False
                numbers.append(
                    PartNumber(
                        number=int("".join(grid[y][x] for y, x in number)),
                        coords=number,
                        grid=grid,
                    )
                )

    # populate the neighbors, and other stuff
    for n in numbers:
        neighbors_coords = set()
        for cifra in n.coords:
            neighbors_coords.update(
                set(get_neighbors(cifra, grid, diagonals=True, return_values=False))
            )
        neighbors_coords.difference_update(set(n.coords))
        n.neighbors = neighbors_coords

        n.has_symbol = any(grid[y][x] != "." for y, x in neighbors_coords)

        for y, x in neighbors_coords:
            if grid[y][x] == "*":
                n.is_gear = True
                n.gear_coords = (y, x)
                break

    data = numbers


# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data):
    sol1 = 0

    for n in numbers:
        if n.has_symbol:
            sol1 += n.number

    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data):
    sol2 = 0

    gears_points = set()
    for n in numbers:
        if n.is_gear:
            gears_points.add(n.gear_coords)

    for gear in gears_points:
        gears = [n.number for n in numbers if n.gear_coords == gear]

        # Bold assumption: for every gear asterisk there are at MOST 2 numbers
        if len(gears) == 2:
            sol2 += gears[0] * gears[1]

    return sol2


s1 = part1(data)
s2 = part2(data)

print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")

print
