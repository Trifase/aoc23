import os

# from pprint import pprint as pp
from datetime import date
from rich import print as richprint

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


def energize_grid(data: list[list[str]], start: tuple[int], dir: str, return_grid=False) -> list[tuple[int]]:
    energized = set()

    beams = []
    y, x = start
    beams.append(MovingThing(y=y, x=x, dir=dir))

    special_cells = ["|", "-", "\\", "/"]
    special_cells_triggered = set()

    while len(beams) > 0:
        for beam in beams.copy():
            # Move the beam
            beam.go()

            # Check if the beam is out of bounds. Remove if true.
            if beam.x < 0 or beam.x > len(data[0]) - 1 or beam.y < 0 or beam.y > len(data) - 1:
                beams.remove(beam)
                continue

            # Add the energized point to the set
            energized.add(beam.coords)

            try:
                cell = data[beam.y][beam.x]
            except IndexError:
                print("This beam tried to access outside the grid")
                print(beam)
                print(f"IndexError: {beam.y}, {beam.x}")
                quit()

            # check if we are on a special cell already triggered and remove the beam, to prevent a loop
            trigger = f"{beam.y},{beam.x},{beam.dir}"
            if cell in special_cells and trigger in special_cells_triggered:
                beams.remove(beam)
                continue

            # check if the bean needs to rotate
            if cell == "\\":
                match beam.dir:
                    case "N":
                        beam.dir = "W"
                    case "S":
                        beam.dir = "E"
                    case "E":
                        beam.dir = "S"
                    case "W":
                        beam.dir = "N"
                special_cells_triggered.add(trigger)

            elif cell == "/":
                match beam.dir:
                    case "N":
                        beam.dir = "E"
                    case "S":
                        beam.dir = "W"
                    case "E":
                        beam.dir = "N"
                    case "W":
                        beam.dir = "S"
                special_cells_triggered.add(trigger)

            # check if we need to split the beam
            if cell == "|" and beam.dir in ["E", "W"]:
                beams.append(MovingThing(y=beam.y, x=beam.x, dir="N"))
                beams.append(MovingThing(y=beam.y, x=beam.x, dir="S"))
                special_cells_triggered.add(trigger)
                beams.remove(beam)
                continue

            if cell == "-" and beam.dir in ["N", "S"]:
                beams.append(MovingThing(y=beam.y, x=beam.x, dir="E"))
                beams.append(MovingThing(y=beam.y, x=beam.x, dir="W"))
                special_cells_triggered.add(trigger)
                beams.remove(beam)
                continue

    if return_grid:
        return energized, beams
    return len(energized)


# Input parsing
print()
with Timer(name="Parsing", text="Parsing.....DONE: {milliseconds:.0f} ms"):
    """
    We'll parse the input line by line.
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=EXAMPLE)
    # print(data)


# Part 1
@Timer(name="Part 1", text="Part 1......DONE: {milliseconds:.0f} ms")
def part1(data: any) -> int:
    sol1 = 0

    y, x = (0, -1)
    dir = "E"
    energized = energize_grid(data, (y, x), dir)

    sol1 = energized
    return sol1


def print_grid(data, energized):
    for y in range(len(data)):
        for x in range(len(data[y])):
            if (y, x) in energized and data[y][x] not in ["|", "-", "\\", "/"]:
                print("░", end="")
            else:
                print(data[y][x], end="")
        print()


# Part 2
@Timer(name="Part 2", text="Part 2......DONE: {milliseconds:.0f} ms")
def part2(data: any) -> int:
    sol2 = 0
    energized_set = []

    # # A weak try to print a nice grid ###############
    # winner = (110, 104)
    # winner_dir = "N"

    # energized, beams = energize_grid(data, winner, winner_dir, return_grid=True)
    # # print(energized)
    # data = [list(line) for line in data]
    # for beam in energized:
    #     y, x = beam
    #     cell = data[y][x]
    #     if y == 0:
    #         up = None
    #         down = (y + 1, x)
    #         left = (y, x - 1 )
    #         right = (y, x + 1)
    #     elif y == len(data) - 1:
    #         up = (y - 1, x)
    #         down = None
    #         left = (y, x - 1 )
    #         right = (y, x + 1)
    #     elif x == 0:
    #         up = (y - 1, x)
    #         down = (y + 1, x)
    #         left = None
    #         right = (y, x + 1)
    #     elif x == len(data[0]) - 1:
    #         up = (y - 1, x)
    #         down = (y + 1, x)
    #         left = (y, x - 1 )
    #         right = None
    #     else:
    #         up = (y - 1, x)
    #         down = (y + 1, x)
    #         left = (y, x - 1 )
    #         right = (y, x + 1)


    #     if cell == ".":
    #         if up in energized and down in energized and left in energized and right in energized:
    #             data[y][x] = "[red]╬[/red]"
    #         elif up in energized and down in energized and left in energized:
    #             data[y][x] = "[red]╣[/red]"
    #         elif up in energized and down in energized and right in energized:
    #             data[y][x] = "[red]╠[/red]"
    #         elif up in energized and left in energized and right in energized:
    #             data[y][x] = "[red]╩[/red]"
    #         elif down in energized and left in energized and right in energized:
    #             data[y][x] = "[red]╦[/red]"
    #         elif up in energized and down in energized:
    #             data[y][x] = "[red]║[/red]"
    #         elif left in energized and right in energized:
    #             data[y][x] = "[red]═[/red]"
    #         elif up in energized and left in energized:
    #             data[y][x] = "[red]╝[/red]"
    #         elif up in energized and right in energized:
    #             data[y][x] = "[red]╚[/red]"
    #         elif down in energized and left in energized:
    #             data[y][x] = "[red]╗[/red]"
    #         elif down in energized and right in energized:
    #             data[y][x] = "[red]╔[/red]"
    #         elif up in energized:
    #             data[y][x] = "[red]╨[/red]"
    #         elif down in energized:
    #             data[y][x] = "[red]╥[/red]"
    #         elif left in energized:
    #             data[y][x] = "[red]╡[/red]"
    #         elif right in energized:
    #             data[y][x] = "[red]╞[/red]"
    #         else:
    #             data[y][x] = '[white] [/white]'

    # for y in range(len(data)):
    #     for x in range(len(data[0])):
    #         if data[y][x] == '\\':
    #             data[y][x] = "[blue]╲[/blue]"
    #         elif data[y][x] == '/':
    #             data[y][x] = "[blue]/[/blue]"
    #         elif data[y][x] == '|':
    #             data[y][x] = "[blue]│[/blue]"
    #         elif data[y][x] == '-':
    #             data[y][x] = "[blue]─[/blue]"
    #         elif data[y][x] == '.':
    #             data[y][x] = " "

    # from rich.console import Console
    # console = Console(highlight=False)
    # for line in data:
    #     line_str = ''.join(line)
    #     console.print(line_str)
    #################################################

    # from west
    for y in range(len(data)):
        energized = energize_grid(data, (y, -1), "E")
        energized_set.append(energized)

    # from east
    for y in range(len(data)):
        energized = energize_grid(data, (y, len(data[0])), "W")
        energized_set.append(energized)

    # from north
    for x in range(len(data[0])):
        energized = energize_grid(data, (-1, x), "S")
        energized_set.append(energized)

    # from south
    for x in range(len(data[0])):
        energized = energize_grid(data, (len(data), x), "N")
        energized_set.append(energized)

    sol2 = max(energized_set)

    return sol2


s1 = part1(data)
s2 = part2(data)

print()
print(f"=========:: [DAY {DAY}] ::=========")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
