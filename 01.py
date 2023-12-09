from rich import print

from codetiming import Timer
from icecream import ic

from utils import SESSIONS, get_data, get_data_from_file

YEAR = 2023
DAY = 1
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


# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data):
    if EXAMPLE:
        data = get_data_from_file("data/1-example-a.txt", strip=True)
    sol1 = 0
    for line in data:
        calibration_value = ""
        for c in line:
            if c.isdigit():
                calibration_value += c
        calibration_value = calibration_value[0] + calibration_value[-1]
        sol1 += int(calibration_value)

    return sol1


def extract_numbers(line):
    numbers = {}

    strings = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

    for i, c in enumerate(line):
        if c.isdigit():
            numbers[i] = int(c)

    for s in strings.keys():
        indexes = [i for i in range(len(line)) if line.startswith(s, i)]
        for i in indexes:
            numbers[i] = strings[s]

    return dict(sorted(numbers.items()))


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data):
    sol2 = 0

    for d, line in enumerate(data):
        numbers = extract_numbers(line)
        keys = list(numbers.keys())
        first = keys[0]
        last = keys[-1]
        sol2 += int(f"{numbers[first]}{numbers[last]}")
        # print(f"{d} {line}: {list(numbers.values())} | {numbers[first]} + {numbers[last]} =  {numbers[first]}{numbers[last]} | {sol2}")

    # print(f"Parsed {d} lines")
    return sol2


s1 = part1(data)
s2 = part2(data)

print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")

print
