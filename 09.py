from codetiming import Timer
from icecream import ic
from datetime import date
import os

# from rich import print
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


def reduce_diffs(numbers: list[int]) -> list[list[int]]:
    return_seqs = []
    while not all([x == numbers[0] for x in numbers]):
        diff_seq = []
        for n in range(1, len(numbers)):
            diff_seq.append(numbers[n] - numbers[n - 1])
        numbers = diff_seq
        return_seqs.append(diff_seq)
    return return_seqs


def next_number(seq: list[int], previsions: list[list[list]], backwards: bool = False) -> int:
    next_number = seq[-1]
    if backwards:
        next_number = seq[0]

    while previsions:
        l = previsions.pop()

        if backwards:
            next_sum = l[0]
        else:
            next_sum = l[-1]

        if previsions:
            if backwards:
                previsions[-1].insert(0, previsions[-1][0] - next_sum)
            else:
                previsions[-1].append(previsions[-1][-1] + next_sum)

    if backwards:
        next_number -= next_sum
    else:
        next_number += next_sum
    return next_number
    
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

    for line in data:
        line = [int(x) for x in line.split(' ')]
        seqs = reduce_diffs(line)
        next_n = next_number(line, seqs)
        # print(f"{' '.join(str(c) for c in line)} → {next_n}")
        sol1 += next_n
    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2......DONE: {milliseconds:.0f} ms")
def part2(data: any) -> int:
    """
    This is basically part1, but with backwards=True in next_number().
    """
    sol2 = 0

    for line in data:
        line = [int(x) for x in line.split(' ')]
        seqs = reduce_diffs(line)
        next_n = next_number(line, seqs, backwards=True)
        # print(f"{next_n} ← {' '.join(str(c) for c in line)} ")
        sol2 += next_n

    return sol2


s1 = part1(data)
s2 = part2(data)

print()
print(f"=========:: [DAY {DAY}] ::=========")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")