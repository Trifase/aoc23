import os

# from pprint import pprint as pp
from datetime import date

from codetiming import Timer
from dataclassy import dataclass
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


def HASH(string: str) -> int:
    """
    Determine the ASCII code for the current character of the string.
    Increase the current value by the ASCII code you just determined.
    Set the current value to itself multiplied by 17.
    Set the current value to the remainder of dividing itself by 256.
    """
    value = 0
    for c in string:
        value += ord(c)
        value *= 17
        value %= 256
    return value


@dataclass
class Lens:
    label: str
    focal_length: int

    def __str__(self):
        return f"{self.label} {self.focal_length}"

    def __repr__(self):
        return f"{self.label} {self.focal_length}"


def remove_lens(box_lens: list[Lens], label: str) -> list[Lens]:
    """
    Remove a lens from the box.
    """
    for lens in box_lens:
        if lens.label == label:
            box_lens.remove(lens)
    return box_lens


def replace_lens(box_lenses: list[Lens], label: str, focal_length: int) -> list[Lens]:
    """
    Replace a lens in the box.
    """
    replaced = False

    for lens in box_lenses:
        if lens.label == label:
            lens.focal_length = focal_length
            replaced = True

    if not replaced:
        box_lenses.append(Lens(label, focal_length))

    return box_lenses


# Input parsing
print()
with Timer(name="Parsing", text="Parsing.....DONE: {milliseconds:.0f} ms"):
    """
    We'll parse the input line by line.
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=EXAMPLE)
    data = data[0].split(",")


# Part 1
@Timer(name="Part 1", text="Part 1......DONE: {milliseconds:.0f} ms")
def part1(data: any) -> int:
    sol1 = 0

    for string in data:
        sol1 += HASH(string)

    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2......DONE: {milliseconds:.0f} ms")
def part2(data: any) -> int:
    sol2 = 0

    boxes = {}
    for b in range(256):
        boxes[b] = []

    label = None
    box = None

    for step in data:
        if "-" in step:
            label = step.split("-")[0]
            box = HASH(label)
            lenses = boxes[box]
            lenses = remove_lens(lenses, label)
            boxes[box] = lenses

        elif "=" in step:
            label = step.split("=")[0]
            box = HASH(label)
            focal_length = int(step.split("=")[1])
            lenses = boxes[box]
            lenses = replace_lens(lenses, label, focal_length)
            boxes[box] = lenses

    for b in range(256):
        if boxes[b]:
            for slot, lens in enumerate(boxes[b]):
                focusing_power = (1 + b) * (1 + slot) * lens.focal_length
                sol2 += focusing_power

    return sol2


s1 = part1(data)
s2 = part2(data)

print()
print(f"=========:: [DAY {DAY}] ::=========")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
