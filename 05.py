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
    for map in maps.values():
        for _range, change in map['ranges'].items():
            origin, end = [int(x) for x in _range.split('-')]
            if seed in range(origin, end):
                seed = seed + change
                break
    return seed

def make_maps(data: list) -> dict:
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

def stop_everything(_range, cerco, range_cercato, this_map):
    if _range[0] not in [0, 3507573, 7014538, 8865630, 10512506, 10997558, 11018488, 14676492, 17913397, 22056764, 26193168, 27466204, 27703099, 29181280, 45616495, 49759862, 56884378, 59336731, 64524116, 65420654, 69945093, 72937484, 73321151, 82121354, 86331660, 96082543]: # or this_map['name'] != 'humidity-to-location':
        return _range
    else:
        
        cerco_min, cerco_max = cerco
        _range_min, _range_max = _range
        iniziale = cerco_min < _range_min and _range_min <= cerco_max < _range_max
        completamente_dentro = cerco_min >= _range_min and cerco_max <= _range_max
        finale = _range_min <= cerco_min < _range_max and cerco_max > _range_max
        entrambe = cerco_min < _range_min and cerco_max > _range_max
        if iniziale:
            motivo = "Parte iniziale"
        elif completamente_dentro:
            motivo = "Completamente dentro"
        elif finale:
            motivo = "Parte finale"
        elif entrambe:
            motivo = "Entrambe"
        else:
            motivo = "Normale"
        pprint(f"Cercavo {cerco} in {range_cercato} in {this_map['name']}: {motivo}")
        return _range
        # quit()

def get_next_ranges(source_range: set, this_map: dict):
    next_ranges = set()
    for source in source_range:
        cerco_min, cerco_max = source
        # pprint(f"{this_map['name']}: cerco {cerco_min}-{cerco_max}")
        cerco = (cerco_min, cerco_max)
        found = False
        for _range, change in this_map['ranges'].items():

            _range_min, _range_max = [int(x) for x in _range.split('-')]
            _range = (_range_min, _range_max)

            # print(f"CERCO {cerco_min}-{cerco_max} in {_range_min}-{_range_max}")
            # print(f"Valuto il range {_range_min},{_range_max} con change {change}")
            pprint(f"cerco {cerco_min}-{cerco_max} in {_range_min}-{_range_max}")

            if cerco_min < _range_min and _range_min <= cerco_max < _range_max: # parte iniziale non coperta
                pprint('INIZIALE NON COPERTA')
                parte_iniziale = (cerco_min, _range_min)
                parte_modificata = (_range_min + change, cerco_max + change)
                # pprint(f"Parzialmente bene, parte iniziale non coperta: {parte_iniziale}")
                # next_ranges.add(stop_everything(parte_iniziale, cerco, _range, this_map))
                next_ranges.add(stop_everything(parte_modificata, cerco, _range, this_map))
                # pprint(f"Aggiungo parte iniziale: {parte_iniziale}")
                # pprint(f"Aggiungo parte modificata: {parte_modificata}")
                pprint(f"{cerco} → {parte_modificata}")
                pprint(f"{cerco} → {parte_iniziale} (Iniziale)")
                found = True
            
            elif cerco_min >= _range_min and cerco_max <= _range_max:  # completely inside
                pprint('TUTTO DENTRO')
                # pprint(f"{_range_min}, {_range_max} ({change}) va bene → {(cerco_min + change, cerco_max + change)}")
                parte_modificata = (cerco_min + change, cerco_max + change)
                # next_ranges.add(parte_modificata)
                next_ranges.add(stop_everything(parte_modificata, cerco, _range, this_map))
                # pprint(f"Aggiungo parte modificata: {parte_modificata}")
                pprint(f"{cerco} → {parte_modificata}")
                found = True



            elif _range_min <= cerco_min < _range_max and cerco_max > _range_max: # parte finale non coperta
                pprint('FINALE NON COPERTA')
                parte_finale = (_range_max + 1, cerco_max)
                parte_modificata = (cerco_min + change, _range_max + change)
                # pprint(f"Parzialmente bene, parte finale non coperta: {parte_finale}")
                # next_ranges.add(stop_everything(parte_finale, cerco, _range, this_map))
                next_ranges.add(stop_everything(parte_modificata, cerco, _range, this_map))
                # pprint(f"Aggiungo parte finale: {parte_finale}")
                # pprint(f"Aggiungo parte modificata: {parte_modificata}")
                pprint(f"{cerco} → {parte_modificata}")
                pprint(f"{cerco} → {parte_finale} (Finale)")
                found = True

            elif cerco_min < _range_min and cerco_max > _range_max: # entrambe le parti scoperte
                pprint('ENTRAMBE LE PARTI SCOPERTE')
                parte_iniziale = (cerco_min, _range_min)
                parte_finale = (_range_max + 1, cerco_max)
                parte_modificata = (_range_min + change, _range_max + change)
                # pprint(f"Parzialmente bene, entrambe le parti scoperte: {parte_iniziale}, {parte_finale}")
                # next_ranges.add(stop_everything(parte_iniziale, cerco, _range, this_map))
                # next_ranges.add(stop_everything(parte_finale, cerco, _range, this_map))
                next_ranges.add(stop_everything(parte_modificata, cerco, _range, this_map))
                # pprint(f"Aggiungo parte iniziale: {parte_iniziale}")
                # pprint(f"Aggiungo parte finale: {parte_finale}")
                # pprint(f"Aggiungo parte modificata: {parte_modificata}")
                pprint(f"{cerco} → {parte_modificata}")
                pprint(f"{cerco} → {parte_iniziale} (Iniziale)")
                pprint(f"{cerco} → {parte_finale} (Finale)")
                found = True
            else:
                pprint('NON VA BENE')
                pass
                # pprint(f"{_range_min}, {_range_max} non va bene.")

        if not found:
            # print('NON TROVATO')
            # pprint("Rimane uguale")
            next_ranges.add(stop_everything(cerco, cerco, _range, this_map))
            pprint(f"{cerco} → {cerco}")
            # quit()
            
    # print(f"{cerco_min}-{cerco_max} → {this_map['name']} → {next_ranges}")

    return next_ranges

def get_location_range_from_seed_range(seed_range: tuple, maps: dict) -> tuple:
    ranges_to_search = [seed_range]
    for mappa in maps.values():
        next_ranges = set()
        pprint("=====================================")
        pprint(f"Map: {mappa['name']}")
        for _range, change in mappa['ranges'].items():
            _range = [int(x) for x in _range.split('-')]
            pprint(f"Map: {_range} + {change}")
        pprint(f"Ranges to search: {ranges_to_search}")
        pprint("- - - - - - - - - - - - - - - - - - -")
        next_ranges.update(get_next_ranges(ranges_to_search, mappa))
        pprint(f"Next ranges: {next_ranges}")
        pprint("=====================================")
        ranges_to_search = next_ranges
    return ranges_to_search

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
    seeds = [int(x) for x in data[0].split(': ')[1].split(' ')]
    maps = make_maps(data)


    locations = []
    for seed in seeds:
        location = get_location_from_seed(seed, maps)
        locations.append(location)

        # print(f"Seed {seed} → Location {location}")

    sol1 = min(locations)
    print()

    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data: any) -> int:
    sol2 = 0

    maps = make_maps(data)
    pprint(maps)
    seeds = [int(x) for x in data[0].split(': ')[1].split(' ')]
    pprint(seeds)

    initial_ranges = []

    for i in range(0, len(seeds), 2):
        n_seeds = seeds[i + 1]
        seed_range = (seeds[i], seeds[i] + n_seeds - 1)
        initial_ranges.append(seed_range)

    ranges_to_search = initial_ranges
    for mappa in maps.values():
        pprint(f"===== {mappa['name']} =====")
        pprint(f"Cerco i ranges {sorted(ranges_to_search)}")
        next_ranges = get_next_ranges(ranges_to_search, mappa)
        pprint(f"Ecco i prossimi ranges: {sorted(next_ranges)}")
        # quit()
        # print("------------------------")
        ranges_to_search = next_ranges

    pprint(f"Final ranges: {sorted(ranges_to_search)}")

    min_location = 0
    min_locations = set()
    for location in ranges_to_search:
        if location[0] < min_location or not min_location:
            min_location = location[0]
        min_locations.add(location[0])
    pprint("===========")
    pprint(sorted(min_locations))
    sol2 = min_location
    return sol2

s1 = part1(data)
s2 = part2(data)

print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")

