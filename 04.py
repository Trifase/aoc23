from codetiming import Timer
from icecream import ic
from rich import print

from utils import SESSIONS, get_data

YEAR = 2023
DAY = 4

EXAMPLE = True
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
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    """
    We'll parse the input line by line.
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=EXAMPLE)


# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data: any) -> int:
    sol1 = 0

    for line in data:
        card_numbers = set(int(x.strip()) for x in line.split("|")[1].split())
        winning_numbers = set(int(x.strip()) for x in line.split("|")[0].split(":")[-1].split())
        matches = winning_numbers.intersection(card_numbers)

        points = 0

        if matches:
            points = 1
            for _ in range(len(matches) - 1):
                points = points * 2

        sol1 += points

    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data: any) -> int:
    sol2 = 0
    cards = {}

    # First pass: parsing all the tickets once
    for index, line in enumerate(data):
        card_numbers = set(int(x.strip()) for x in line.split("|")[1].split())
        winning_numbers = set(int(x.strip()) for x in line.split("|")[0].split(":")[-1].split())
        matches = winning_numbers.intersection(card_numbers)
        cards[index] = {
            "numbers": card_numbers,
            "matching_numbers": len(matches),
            "quantity": 1,
        }

    # Second pass: adding the cards
    for index, card in cards.items():
        for i in range(index + 1, index + card["matching_numbers"] + 1):
            if cards[i]:
                cards[i]["quantity"] += 1 * card["quantity"]

    sol2 = sum([card["quantity"] for card in cards.values()])

    return sol2


s1 = part1(data)
s2 = part2(data)

print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")

print
