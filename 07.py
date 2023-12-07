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


card_points = {'2': 2,'3': 3,'4': 4,'5': 5,'6': 6,'7': 7,'8': 8,'9': 9,
         'T': 10,'J': 11,'Q': 12,'K': 13,'A': 14}


def value_of_hand(hand: str) -> int:
    """
    This will calculate the value of a hand. It will return an int.
    Possible values are: High card (1), one pair (2), two pair (3), three of a kind (4), full house (5), four of a kind (6), five of a kind (7).
    """
    value = 1

    cards = set(hand)

    # Five of a kind
    if len(cards) == 1:
        # ic("Five of a kind")
        value = 7

    # Four of a kind, or full house
    elif len(cards) == 2:
        # ic("Four of a kind, or full house")
        for x in cards:
            if hand.count(x) == 4: # four of a kind
                # ic("Four of a kind")
                value = 6
                break
        else:
            # ic("Full house")
            value = 5 # full house

    elif len(cards) == 3:
        # ic("Three of a kind, or two pair")
        for x in cards:
            if hand.count(x) == 3:
                # ic("Three of a kind")
                value = 4 # three of a kind
                break
            elif hand.count(x) == 2:
                # ic("Two pair")
                value = 3 # two pair
                break


    elif len(cards) == 4: # one pair
        # ic("One pair")
        value = 2

    return value


def calculate_hand(line: str, jokers: bool = False) -> tuple[int]:
    """
    This will calculate the value of a hand. It will return a list with: the value of the hand, the five value of the cards, the final bet.
    possible values of hand: High card (1), one pair (2), two pair (3), three of a kind (4), full house (5), four of a kind (6), five of a kind (7).
    '33332 256' will return (6, [3, 3, 3, 3, 2], 256)

    jokers: if True, the J can be any other card, to make the strongest combination possible. In card-to-card comparison, the J will be considered the weakest card.
    """
    hand = line.split()[0]
    bet = int(line.split()[-1])

    if jokers:
        card_points['J'] = 1

    list_of_values = [card_points[x] for x in hand]

    if not jokers or 'J' not in hand:
        value = value_of_hand(hand)

    elif jokers and 'J' in hand:
        all_values = []
        for c in card_points.keys():
            v = value_of_hand(hand.replace('J', c))
            all_values.append(v)
            if v == 7: # no need to search further
                break
        value = max(all_values)

    return (value, list_of_values, bet)



def compare_hands(hand1: str, hand2: str) -> bool:
    hand1_bigger = False
    hand1_value, hand1_list = calculate_hand(hand1)
    hand2_value, hand2_list = calculate_hand(hand2)
    # print(f"Comparo {hand1} ({hand1_value}) con {hand2} ({hand2_value})")
    if hand1_value > hand2_value:
        # print(f"{hand1} è più grande di {hand2}")
        hand1_bigger = True

    # Se il valore è uguale, compariamo le singole carte, dalla prima alla quinta
    elif hand1_value == hand2_value:
        # print("Le mani hanno lo stesso valore, confronto le carte")
        for i in range(len(hand1_list)):
            # print(f"Confronto {hand1_list[i]} con {hand2_list[i]}")
            # Se la carta di hand1 è più grande, hand1 è più grande
            if hand1_list[i] > hand2_list[i]:
                # print(f"{hand1_list[i]} è più grande di {hand2_list[i]}")
                hand1_bigger = True
                break
            elif hand1_list[i] < hand2_list[i]:
                # print(f"{hand1_list[i]} è più piccola di {hand2_list[i]}")
                break
            # else:
                # print(f"{hand1_list[i]} è uguale a {hand2_list[i]}")
    # else:
    #     print(f"{hand1} è più piccola di {hand2}")
    return hand1_bigger


def bubble_sort(my_list: list) -> list:
    n = len(my_list)
    for i in range(n):
        done = False
        for j in range(0, n - i - 1):
            hand1 = my_list[j].split()[0]
            hand2 = my_list[j + 1].split()[0]
            pprint(f"Sorting: {hand1} vs {hand2}")
            if compare_hands(hand1, hand2):
                # pprint(f"{hand1} è più grande di {hand2}, li scambio")
                my_list[j], my_list[j + 1] = my_list[j + 1], my_list[j]
                done = True
        if done:
            break
    return my_list

def insertion_sort(my_list: list) -> list:
    for i in range(1, len(my_list)):
        hand2 = my_list[i]
        j = i - 1
        hand1 = my_list[j]

        while j >= 0 and hand1 > hand2:
            my_list[j + 1] = my_list[j]
            j -= 1

        my_list[j + 1] = hand2
    return my_list



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
        sol1 += (line[-1] * i)

    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2......DONE: {milliseconds:.0f} ms")
def part2(data: any) -> int:
    sol2 = 0

    calculated_data = [calculate_hand(line, jokers=True) for line in data]
    ordered_data = sorted(calculated_data, key=lambda element: (element[0], element[1]))

    for i, line in enumerate(ordered_data, start=1):
        sol2 += (line[-1] * i)

    return sol2

s1 = part1(data)
s2 = part2(data)

print()
print(f"=========:: [DAY {DAY}] ::=========")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")

