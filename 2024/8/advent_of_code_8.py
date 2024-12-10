import itertools
import pathlib
from collections import defaultdict


def get_answer(antenna_map):
    map_height = len(antenna_map)
    map_width = len(antenna_map[0])
    antennas = defaultdict(set)
    for y, line in enumerate(antenna_map):
        for x, antenna in enumerate(line):
            if antenna != '.':
                antennas[antenna].add((y, x))

    antinode_locations = set()
    for antenna_type, antenna_locations in antennas.items():
        antinode_locations.update(antenna_locations)
        for combination in itertools.combinations(antenna_locations, 2):
            (y1, x1), (y2, x2) = sorted(combination, reverse=True)
            y_distance = y1 - y2
            x_distance = abs(x1 - x2)

            if x1 >= x2:
                x3 = x1 + x_distance if x1 + x_distance < map_width else None
                x4 = x2 - x_distance if x2 - x_distance >= 0 else None
                x3_increasing = True
            else:
                x3 = x1 - x_distance if x1 - x_distance >= 0 else None
                x4 = x2 + x_distance if x2 + x_distance < map_width else None
                x3_increasing = False

            y3 = y1 + y_distance if y1 + y_distance < map_height else None
            while y3 is not None and x3 is not None:
                antinode_locations.add((y3, x3))
                y3 = y3 + y_distance if y3 + y_distance < map_height else None
                if x3_increasing and y3 is not None:
                    x3 = x3 + x_distance if x3 + x_distance < map_width else None
                else:
                    x3 = x3 - x_distance if x3 - x_distance >= 0 else None

            y4 = y2 - y_distance if y2 - y_distance >= 0 else None
            while y4 is not None and x4 is not None:
                antinode_locations.add((y4, x4))
                y4 = y4 - y_distance if y4 - y_distance >= 0 else None
                if x3_increasing and y4 is not None:
                    x4 = x4 - x_distance if x4 - x_distance >= 0 else None
                else:
                    x4 = x4 + x_distance if x4 + x_distance < map_width else None

    return len(antinode_locations)


if __name__ == '__main__':

    with open(f"{pathlib.Path(__file__).parent.resolve()}/advent_of_code_8_input.txt", "r") as input_file:
        input_map = [line.strip() for line in input_file]

    # I just overwrote answer 1 today, they're basically the same
    answer_1 = get_answer(input_map)
    print(answer_1)

