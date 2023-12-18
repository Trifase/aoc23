import os

# from pprint import pprint as pp
from datetime import date

from codetiming import Timer
from icecream import ic

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

# Part 1
@Timer(name="Part 1", text="Part 1......DONE: {milliseconds:.0f} ms")
def part1(data: any) -> int:
    sol1 = 0
    point = MovingThing(0, 0)
    points = []
    points.append(point.coords_grid)

    perimeter = 0

    for line in data:
        dir, steps, _ = line.split()

        match dir:
            case "R":
                    point.move_to((point.x + int(steps), point.y))
            case "L":
                    point.move_to((point.x - int(steps), point.y))
            case "D":
                    point.move_to((point.x, point.y + int(steps)))
            case "U":
                    point.move_to((point.x, point.y - int(steps)))
        points.append(point.coords_grid)
        perimeter += int(steps)

    # This is the shoelace formula
    for n in range(len(points) - 1):
        x1, y1 = points[n]
        x2, y2 = points[n+1]
        sol1 += x1 * y2 - x2 * y1

    xn, yn = points[-1]
    x0, y0 = points[0]
    sol1 += xn * y0 - x0 * yn

    sol1 = abs(sol1 / 2)

    # We should adjust for the width of the perimeter. The perimeter itself is a rectangle of width 1, so we can just divide by 2 and add 1.
    sol1 += perimeter / 2 + 1

    # We also convert to int
    sol1 = int(sol1)

    return sol1



# Part 2
@Timer(name="Part 2", text="Part 2......DONE: {milliseconds:.0f} ms")
def part2(data: any) -> int:
    sol2 = 0


    point = MovingThing(0, 0)
    points = []
    points.append(point.coords_grid)

    perimeter = 0

    DIRS = 'RDLU'
    for line in data:
        # (#70c710) - get rid of the first 2 chars and the last one
        # the last int is the direction
        _, _, hexnum = line.split()
        hexnum = hexnum.replace(")", "").replace("#", "").replace("(", "")
        dir = int(hexnum[-1])
        hexnum = hexnum[:-1]
        steps = int(hexnum, 16)
        
        dir = DIRS[dir]

        match dir:
            case "R":
                    point.move_to((point.x + int(steps), point.y))
            case "L":
                    point.move_to((point.x - int(steps), point.y))
            case "D":
                    point.move_to((point.x, point.y + int(steps)))
            case "U":
                    point.move_to((point.x, point.y - int(steps)))
        points.append(point.coords_grid)
        perimeter += int(steps)


    for n in range(len(points) - 1):
        x1, y1 = points[n]
        x2, y2 = points[n+1]
        sol2 += x1 * y2 - x2 * y1

    xn, yn = points[-1]
    x0, y0 = points[0]
    sol2 += xn * y0 - x0 * yn

    sol2 = abs(sol2 / 2)

    # We should adjust for the width of the perimeter. The perimeter itself is a rectangle of width 1, so we can just divide by 2 and add 1.
    sol2 += perimeter / 2 + 1
    sol2 = int(sol2)

    return sol2



s1 = part1(data)
s2 = part2(data)

print()
print(f"=========:: [DAY {DAY}] ::=========")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
