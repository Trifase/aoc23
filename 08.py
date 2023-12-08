from codetiming import Timer
from icecream import ic
import math

# from rich import print
from utils import SESSIONS, get_data

YEAR = 2023
DAY = 8

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
    instructions = [int(x) for x in data[0].replace('L', '0').replace('R', '1')]

    network = {}
    for line in data[2:]:
        key, value = line.split(' = ')
        left, right = value[1:-1].split(', ')
        network[key] = [left, right]

    data = instructions, network


# Part 1
@Timer(name="Part 1", text="Part 1......DONE: {milliseconds:.0f} ms")
def part1(data: any) -> int:
    """
    Starting from 'AAA' we'll follow the instructions and count the steps until we reach 'ZZZ'
    """
    sol1 = 0
    instructions = data[0]
    network = data[1]

    this = 'AAA'
    steps = 0
    while this != 'ZZZ':

        left, right = network[this]
        if instructions[steps % len(instructions)] == 0:
            this = left
        else:
            this = right

        steps += 1

    sol1 = steps

    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2......DONE: {milliseconds:.0f} ms")
def part2(data: any) -> int:
    """
    This is basically the same of part 1, but we have to do it for all the starting points (keys that ends with 'A') until we
    reach a key that ends with 'Z'. We collect all the steps needed and then we calculate the LCM of all the steps.
    """
    sol2 = 0

    instructions = data[0]
    network = data[1]

    this_list = [x for x in network.keys() if x.endswith('A')]
    list_steps = []

    for this in this_list:
        steps = 0

        while not this.endswith('Z'):
            left, right = network[this]
            if instructions[steps % len(instructions)] == 0:
                this = left
            else:
                this = right
            steps += 1

        list_steps.append(steps)

    sol2=math.lcm(*list_steps)


    return sol2


s1 = part1(data)
s2 = part2(data)

print()
print(f"=========:: [DAY {DAY}] ::=========")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
