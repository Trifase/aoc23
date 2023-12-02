from rich import print

from codetiming import Timer
from icecream import ic

from utils import SESSIONS, get_data

YEAR = 2023
DAY = 2
EXAMPLE = False
DEBUG = False

if DEBUG:
    ic.enable()
else:
    ic.disable()


# Input parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    """
    We'll parse the input line by line. 
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=EXAMPLE)

def analize_game(game, mode="normal"):
    red, green, blue = 0, 0, 0

    id, cubes = game.split(":")
    id = id.split()[1]
    for play in cubes.split(';'):
        for cube in play.split(','):
            qty, color = cube.split()
            qty = int(qty)
            if mode=="normal":
                if color == "green":
                    green = qty if qty > green else green
                elif color == "red":
                    red = qty if qty > red else red
                elif color == "blue":
                    blue = qty if qty > blue else blue
            elif mode=="min":
                if color == "green":
                    green = qty if (qty > green or not green) else green
                elif color == "red":
                    red = qty if (qty > red or not red) else red
                elif color == "blue":
                    blue = qty if (qty > blue or not blue) else blue
                ic(red, green, blue)

    return red, green, blue

# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data):
    sol1 = 0

    max_red, max_green, max_blue = 12, 13, 14

    # print(f"OK?\tRed\tGreen\tBlue\tsol1\tGame")

    for game in data:
        id = game.split(":")[0].split()[1]
        red, green, blue = analize_game(game)
        is_game_ok = red <= max_red and green <= max_green and blue <= max_blue
        if is_game_ok:
            sol1 += int(id)
        # print(f"{is_game_ok}\t{red}\t{green}\t{blue}\t{sol1}\t{game}")

    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data):
    sol2 = 0

    # print(f"Power\nRed\tGreen\tBlue\tsol2\tGame")

    for game in data:

        red, green, blue = analize_game(game, mode="min")
        power = red * green * blue
        sol2 += power

        # print(f"{power}\t{red}\t{green}\t{blue}\t{sol2}\t{game}")
    return sol2

s1 = part1(data)
s2 = part2(data)

print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")

print