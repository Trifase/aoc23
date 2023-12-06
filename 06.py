# from rich import print
from math import prod

from codetiming import Timer
from icecream import ic

from utils import SESSIONS, get_data

YEAR = 2023
DAY = 6

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


def get_ways_of_beating(time: int, record: int) -> int:
    beat_the_record = 0
    for speed in range(time):
        time_remaining = time - speed
        distance_travelled = speed * time_remaining

        # pprint(f"Hold the button for {speed} seconds. After its remaining {time_remaining} milliseconds of travel time, the boat will have gone {distance_travelled} millimeters.")

        if distance_travelled > record:
            beat_the_record += 1

    return beat_the_record


# Input parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    """
    We'll parse the input line by line.
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=EXAMPLE)
    times = [int(x.strip()) for x in data[0].split(":")[-1].split()]
    distances = [int(x.strip()) for x in data[1].split(":")[-1].split()]
    data = dict(zip(times, distances))


# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data: any) -> int:
    sol1 = 0

    number_of_ways = []

    for time, record in data.items():
        beat_the_record = get_ways_of_beating(time, record)
        number_of_ways.append(beat_the_record)

    sol1 = prod(number_of_ways)

    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data: any) -> int:
    sol2 = 0

    times, distances = zip(*data.items())
    sol2 = get_ways_of_beating(
        int("".join(str(x) for x in times)), int("".join(str(x) for x in distances))
    )

    return sol2


s1 = part1(data)
s2 = part2(data)

print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
