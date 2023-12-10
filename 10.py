import os
from datetime import date

from codetiming import Timer
from icecream import ic
from PIL import Image

from utils import SESSIONS, MovingThing, get_data

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


# Input parsing
print()
with Timer(name="Parsing", text="Parsing.....DONE: {milliseconds:.0f} ms"):
    """
    We'll parse the input line by line.
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=EXAMPLE)
    grid = []
    for line in data:
        grid.append(list(line))
    data = grid


def find_connecting_pipes(coords: tuple, grid: list[list[str]]) -> dict:
    y, x = coords
    y_max = len(grid)
    x_max = len(grid[0])

    this = grid[y][x]

    neighbors = {}

    su = (y - 1, x) if y != 0 else None
    dx = (y, x + 1) if x != x_max - 1 else None
    giu = (y + 1, x) if y != y_max - 1 else None
    sx = (y, x - 1) if x != 0 else None

    su_str = grid[su[0]][su[1]] if su else None
    dx_str = grid[dx[0]][dx[1]] if dx else None
    giu_str = grid[giu[0]][giu[1]] if giu else None
    sx_str = grid[sx[0]][sx[1]] if sx else None

    if su and this in ["|", "L", "J", "S"] and su_str in ["|", "7", "F", "S"]:
        neighbors["N"] = su_str, su
    if dx and this in ["-", "L", "F", "S"] and dx_str in ["-", "J", "7", "S"]:
        neighbors["E"] = dx_str, dx
    if giu and this in ["|", "7", "F", "S"] and giu_str in ["|", "L", "J", "S"]:
        neighbors["S"] = giu_str, giu
    if sx and this in ["-", "J", "7", "S"] and sx_str in ["-", "L", "F", "S"]:
        neighbors["W"] = sx_str, sx

    return neighbors


def return_loop(grid: list[list[str]]) -> set[tuple]:
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "S":
                start = (y, x)
                break

    animal = MovingThing()
    animal.coords = start

    back_again = False
    loop = set()
    loop.add(start)

    opposing_directions = {
        "N": "S",
        "S": "N",
        "E": "W",
        "W": "E",
    }

    last_dir = None
    while not back_again:
        # find all the connecting pipes
        neighbors = find_connecting_pipes(animal.coords, grid)
        possible_directions = [(k, v[1]) for k, v in neighbors.items()]

        # choosing a direction
        for dir, coord in possible_directions:
            # print(f"last_dir: {last_dir} - dir: {dir}")
            if coord not in loop or coord == start and dir != opposing_directions.get(last_dir):
                # print(f"moving {dir} to {coord}")
                animal.coords = coord
                last_dir = dir
                loop.add(coord)
                break
            else:
                pass

        # check if you are back again
        if animal.coords == start:
            back_again = True
    return loop


# Part 1
@Timer(name="Part 1", text="Part 1......DONE: {milliseconds:.0f} ms")
def part1(data: any) -> int:
    sol1 = 0

    loop = return_loop(data)

    sol1 = len(loop) // 2

    # img_h = len(data[0])
    # img_v = len(data)
    # img = Image.new('RGB', (img_v, img_h))
    # for c in loop:
    #     print(c)
    #     img.putpixel(c, (255, 255, 255))
    # if EXAMPLE:
    #     img.save('loop_example.png')
    # else:
    #     img.save('loop.png')

    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2......DONE: {milliseconds:.0f} ms")
def part2(data: any) -> int:
    sol2 = 0

    tiles = {
        "NS": "|",
        "EW": "-",
        "SW": "7",
        "NW": "J",
        "EN": "L",
        "ES": "F",
    }

    loop = return_loop(data)
    enclosed_tiles = set()

    for y in range(len(data)):
        intersections = 0
        first_corner = False

        for x in range(len(data[y])):
            # The S need to be replaced with the proper tile.
            if grid[y][x] == "S":
                neighbors = find_connecting_pipes((y, x), grid)
                replacement = "".join(sorted([k for k in neighbors.keys()]))
                grid[y][x] = tiles[replacement]

            # Traversing the whole grid row by row, we can check how many times we intersect the loop. If this number is odd,
            # when we are on a non-loop cell, it's an inside cell.
            if (y, x) in loop:
                # So, let's talk about edge cases: these all count as 1 intersections.
                # ┌───┘ └───┐
                # While these don't count as intersections:
                # └───┘ ┌───┐
                # The way we deal with them is ignoring the middle part and checking what type of corner they are

                if grid[y][x] in ["F", "L"]:
                    first_corner = grid[y][x]

                elif grid[y][x] == "-" and first_corner:
                    pass

                elif grid[y][x] in ["J", "7"]:
                    if first_corner:
                        if grid[y][x] == "J" and first_corner == "L":
                            pass
                        elif grid[y][x] == "7" and first_corner == "F":
                            pass
                        else:
                            intersections += 1
                            first_corner = False

                elif grid[y][x] != "-":
                    intersections += 1

            elif (y, x) not in loop:
                if intersections % 2 == 1:
                    enclosed_tiles.add((y, x))
                    sol2 += 1

    # This will draw a nice image of the loop and the enclosed tiles.
    # White = Empty space
    # Black = Loop
    # Red = Enclosed tiles
    img_h = len(data[0])
    img_v = len(data)
    img = Image.new("RGB", (img_v, img_h), (255, 255, 255))
    for c in loop:
        img.putpixel(c, (0, 0, 0))

    for c in enclosed_tiles:
        img.putpixel(c, (255, 0, 0))
        img.save("images/day-10-loop.png")

    return sol2


s1 = part1(data)
s2 = part2(data)

print()
print(f"=========:: [DAY {DAY}] ::=========")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
