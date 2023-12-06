from codetiming import Timer
from icecream import ic
# from rich import print

from utils import SESSIONS, get_data

YEAR = 2023
DAY = 5

EXAMPLE = False
INFO = False
DEBUG = False

if DEBUG:
    ic.enable()
else:
    ic.disable()


def pprint(data: any) -> None:
    if INFO:
        print(data)

def get_location_from_seed(seed: int, maps: dict) -> int:
    """
    From a single seed to a single location. We'll iterate all the maps and apply the changes to the seed.
    """
    for map in maps.values():
        for _range, change in map['ranges'].items():
            origin, end = [int(x) for x in _range.split('-')]
            if seed in range(origin, end):
                seed = seed + change
                break
    return seed

def make_maps(data: list) -> dict:
    """
    This will map the input data into a dictionary of maps. Each map will have a name and a dictionary of ranges, and a change parameter that edits the destination range
    """

    maps = {}
    map_number = 0
    mappa = {}
    for line in data[2:]:
        if not mappa:
            mappa = {}

        if not line:
            mappa['ranges'] = dict(sorted(mappa['ranges'].items()))
            maps[map_number] =mappa
            map_number += 1

        elif line.endswith(':'):
            mappa = {}
            mappa['name'] = line.split(' map')[0]
            mappa['ranges'] = {}

        else:
            dest, origin, _range = [int(x) for x in line.split()]

            mappa['ranges'][f'{origin}-{origin + _range}'] = dest - origin

        # edge case: add the last map
        if line == data[-1]:
            mappa['ranges'] = dict(sorted(mappa['ranges'].items()))
            maps[map_number] = mappa
    return maps

def get_next_ranges(source_range: set, this_map: dict) -> set:
    """ 
    This will take a set of ranges and a single map. It will return a set of mapped destination ranges, but only the part of the source range inside a mapped range
    or those that are not covered by the map.
    """

    next_ranges = set()

    for source in source_range:
        cerco_min, cerco_max = source
        cerco = (cerco_min, cerco_max)
        found = False
        for _range, change in this_map['ranges'].items():

            _range_min, _range_max = [int(x) for x in _range.split('-')]
            _range = (_range_min, _range_max)

            if cerco_min < _range_min and _range_min <= cerco_max < _range_max: # parte iniziale non coperta
                parte_modificata = (_range_min + change, cerco_max + change)
                next_ranges.add(parte_modificata)
                found = True
            
            elif cerco_min >= _range_min and cerco_max <= _range_max:  # completely inside
                parte_modificata = (cerco_min + change, cerco_max + change)
                next_ranges.add(parte_modificata)
                found = True

            elif _range_min <= cerco_min < _range_max and cerco_max > _range_max: # parte finale non coperta
                parte_modificata = (cerco_min + change, _range_max + change)
                next_ranges.add(parte_modificata)
                found = True

            elif cerco_min < _range_min and cerco_max > _range_max: # entrambe le parti scoperte
                parte_modificata = (_range_min + change, _range_max + change)
                next_ranges.add(parte_modificata)
                found = True

            else:
                pass

        if not found:
            next_ranges.add(cerco)

    return next_ranges

def get_location_range_from_seed_range(seed_range: tuple, maps: dict) -> tuple:
    """
    For every seed range, we'll get the location range. We do this by iterating all the maps.
    """
    ranges_to_search = [seed_range]

    for mappa in maps.values():
        next_ranges = set()
        for _range, _ in mappa['ranges'].items():
            _range = [int(x) for x in _range.split('-')]

        next_ranges.update(get_next_ranges(ranges_to_search, mappa))

        ranges_to_search = next_ranges
    return ranges_to_search


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
    seeds = [int(x) for x in data[0].split(': ')[1].split(' ')]
    maps = make_maps(data)

    locations = []
    for seed in seeds:
        location = get_location_from_seed(seed, maps)
        locations.append(location)

    sol1 = min(locations)

    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2......DONE: {milliseconds:.0f} ms")
def part2(data: any) -> int:
    sol2 = 0

    maps = make_maps(data)
    seeds = [int(x) for x in data[0].split(': ')[1].split(' ')]

    initial_ranges = []

    # We make the 10 seeds ranges from the 20 input seeds
    for i in range(0, len(seeds), 2):
        n_seeds = seeds[i + 1]
        seed_range = (seeds[i], seeds[i] + n_seeds - 1)
        initial_ranges.append(seed_range)

    ranges_to_search = initial_ranges

    # we get all the locations for all the seed ranges
    for mappa in maps.values():
        next_ranges = get_next_ranges(ranges_to_search, mappa)
        ranges_to_search = next_ranges

    # we get the minimum of the lower bount of the ranges
    sol2 = min([_range[0] for _range in ranges_to_search])
    return sol2

s1 = part1(data)
s2 = part2(data)

print()
print(f"=========:: [DAY {DAY}] ::=========")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")

