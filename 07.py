from codetiming import Timer
from icecream import ic

# from rich import print
from utils import SESSIONS, get_data

YEAR = 2023
DAY = 7

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


card_points = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


def value_of_hand(hand: str) -> int:
    """
    This will calculate the value of a hand. It will return an int.
    Possible values are: High card (1), one pair (2), two pair (3), three of a kind (4), full house (5), four of a kind (6), five of a kind (7).
    """
    value = 1

    cards = set(hand)

    # Five of a kind
    if len(cards) == 1:
        value = 7

    # Four of a kind, or full house
    elif len(cards) == 2:
        for x in cards:
            if hand.count(x) == 4:  # four of a kind
                value = 6
                break
        else:
            value = 5  # full house

    elif len(cards) == 3:
        for x in cards:
            if hand.count(x) == 3:
                value = 4  # three of a kind
                break
            elif hand.count(x) == 2:
                value = 3  # two pair
                break

    elif len(cards) == 4:  # one pair
        value = 2

    return value


def calculate_hand(line: str, jokers: bool = False) -> tuple[int]:
    """
    This will parse a single line. It will return a list with: the value of the hand, the five value of the cards, the final bet.
    possible values of hand: High card (1), one pair (2), two pair (3), three of a kind (4), full house (5), four of a kind (6), five of a kind (7).
    '33332 256' will return (6, [3, 3, 3, 3, 2], 256)

    jokers: if True, the J can be any other card, to make the strongest combination possible.
            In card-to-card comparison, the J will be considered the weakest card.
    """
    hand = line.split()[0]
    bet = int(line.split()[-1])

    if jokers:
        card_points["J"] = 1

    list_of_values = [card_points[x] for x in hand]

    if not jokers or "J" not in hand:
        value = value_of_hand(hand)

    elif jokers and "J" in hand:
        all_values = []
        # Iterating all the values of the cards to get the best combination
        for c in card_points.keys():
            v = value_of_hand(hand.replace("J", c))
            all_values.append(v)
            if v == 7:  # no need to search further
                break
        value = max(all_values)

    return (value, list_of_values, bet)


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

    calculated_data = [calculate_hand(line) for line in data]
    ordered_data = sorted(calculated_data, key=lambda element: (element[0], element[1]))

    for i, line in enumerate(ordered_data, start=1):
        sol1 += line[-1] * i

    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2......DONE: {milliseconds:.0f} ms")
def part2(data: any) -> int:
    sol2 = 0

    calculated_data = [calculate_hand(line, jokers=True) for line in data]
    ordered_data = sorted(calculated_data, key=lambda element: (element[0], element[1]))

    for i, line in enumerate(ordered_data, start=1):
        sol2 += line[-1] * i

    return sol2


s1 = part1(data)
s2 = part2(data)

print()
print(f"=========:: [DAY {DAY}] ::=========")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
