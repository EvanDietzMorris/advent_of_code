import pathlib

from collections import defaultdict
from dataclasses import dataclass


@dataclass
class CropRegion:
    crop_type: str

    def __post_init__(self):
        self.locations = set()

    def __eq__(self, other_region):
        return self.locations == other_region.locations

    def get_sides(self):
        return sum([location.corners for location in self.locations])

    def get_area(self):
        return len(self.locations)


@dataclass
class CropLocation:
    crop_type: str
    coordinates: tuple
    perimeter: int = 0
    corners: int = 0

    def __eq__(self, other_location):
        return other_location.coordinates == self.coordinates

    def __hash__(self):
        return hash(self.coordinates)


def get_region(crop_regions, crop_type, crop_location: CropLocation):
    for crop_region in crop_regions[crop_type]:
        if crop_location in crop_region.locations:
            return crop_region
    return None


def get_neighbors(crop_locations, y, x, max_height, max_width):

    if y < max_height - 1:
        top_neighbor = crop_locations[str(y+1)][x]
    else:
        top_neighbor = None

    if y > 0:
        bottom_neighbor = crop_locations[str(y-1)][x]
    else:
        bottom_neighbor = None

    if x < max_width - 1:
        right_neighbor = crop_locations[str(y)][x+1]
    else:
        right_neighbor = None

    if x > 0:
        left_neighbor = crop_locations[str(y)][x-1]
    else:
        left_neighbor = None

    return [top_neighbor, bottom_neighbor, left_neighbor, right_neighbor]

def get_diagonal_neighbors(crop_locations, y, x, max_height, max_width):

    if y < max_height - 1 and x < max_width - 1:
        top_right_neighbor = crop_locations[str(y+1)][x+1]
    else:
        top_right_neighbor = None

    if y > 0 and x < max_width - 1:
        bottom_right_neighbor = crop_locations[str(y-1)][x+1]
    else:
        bottom_right_neighbor = None

    if y < max_height - 1 and x > 0:
        top_left_neighbor = crop_locations[str(y+1)][x-1]
    else:
        top_left_neighbor = None

    if y > 0 and x > 0:
        bottom_left_neighbor = crop_locations[str(y-1)][x-1]
    else:
        bottom_left_neighbor = None

    return [top_right_neighbor, bottom_right_neighbor, top_left_neighbor, bottom_left_neighbor]


# this is a mess but it works
def get_corners(crop_type, neighbors, diagonal_neighbors):
    corners = 0
    top_neighbor, bottom_neighbor, left_neighbor, right_neighbor = neighbors
    top_match = top_neighbor.crop_type == crop_type if top_neighbor else None
    bottom_match = bottom_neighbor.crop_type == crop_type if bottom_neighbor else None
    left_match = left_neighbor.crop_type == crop_type if left_neighbor else None
    right_match = right_neighbor.crop_type == crop_type if right_neighbor else None

    top_right_neighbor, bottom_right_neighbor, top_left_neighbor, bottom_left_neighbor = diagonal_neighbors
    top_right_match = top_right_neighbor.crop_type == crop_type if top_right_neighbor else None
    bottom_right_match = bottom_right_neighbor.crop_type == crop_type if bottom_right_neighbor else None
    top_left_match = top_left_neighbor.crop_type == crop_type if top_left_neighbor else None
    bottom_left_match = bottom_left_neighbor.crop_type == crop_type if bottom_left_neighbor else None

    corner_neighbor_match_groups = [
        [left_match, top_left_match, top_match],
        [top_match, top_right_match, right_match],
        [right_match, bottom_right_match, bottom_match],
        [bottom_match, bottom_left_match, left_match],
    ]

    for corner_neighbor_matches in corner_neighbor_match_groups:
        matches = sum([1 for match in corner_neighbor_matches if match])
        if matches == 3:
            pass
        elif matches == 2:
            if not corner_neighbor_matches[1]:  # without this check we'd double count some corners
                corners += 1
        elif matches == 1:
            if corner_neighbor_matches[1]:
                corners += 1
        else:
            corners += 1
    return corners


def find_regions(farm):
    all_crop_locations = defaultdict(list)
    for y, row in enumerate(farm):
        for x, crop_type in enumerate(row):
            all_crop_locations[str(y)].append(CropLocation(crop_type=crop_type, coordinates=(y, x)))

    max_height = len(farm)
    max_width = len(farm[0])
    all_crop_regions = defaultdict(list)
    for y, crop_locations in all_crop_locations.items():
        for x, crop_location in enumerate(crop_locations):
            crop_type = crop_location.crop_type
            neighbors = get_neighbors(all_crop_locations, int(y), x, max_height, max_width)
            current_region = None
            for neighbor in neighbors:
                if neighbor is not None and neighbor.crop_type == crop_type:
                    surrounding_region = get_region(all_crop_regions, crop_type, neighbor)
                    if surrounding_region is not None:
                        if current_region is None:
                            current_region = surrounding_region
                        elif current_region == surrounding_region:
                            pass
                        else:
                            merged_region_locations = surrounding_region.locations
                            all_crop_regions[surrounding_region.crop_type].remove(surrounding_region)
                            current_region.locations.update(merged_region_locations)
                else:
                    crop_location.perimeter += 1

            crop_location.corners = get_corners(crop_type,
                                                neighbors,
                                                get_diagonal_neighbors(all_crop_locations,
                                                                       int(y),
                                                                       x,
                                                                       max_height,
                                                                       max_width))

            if current_region is None:
                current_region = CropRegion(crop_type=crop_type)
                all_crop_regions[crop_type].append(current_region)
            current_region.locations.add(crop_location)

    for y, crop_locations in all_crop_locations.items():
        for x, crop_location in enumerate(crop_locations):
            print(crop_location)

    return all_crop_regions


def get_answer_1(farm):
    all_crop_regions = find_regions(farm)
    price = 0
    for crop_type, crop_region_list in all_crop_regions.items():
        for crop_region in crop_region_list:
            area = crop_region.get_area()
            perimeter = sum([crop_location.perimeter for crop_location in crop_region.locations])
            # print(f'{crop_type}: {area} * {perimeter}')
            price += area * perimeter
    return price


def get_answer_2(farm):

    all_crop_regions = find_regions(farm)
    price = 0
    for crop_type, crop_region_list in all_crop_regions.items():
        for crop_region in crop_region_list:
            area = crop_region.get_area()
            sides = crop_region.get_sides()
            # print(f'{crop_type}: {area} * {sides}')
            price += area * sides
    return price


if __name__ == '__main__':

    # input_file = "advent_of_code_test_input"
    input_file = "advent_of_code_input"
    with open(f"{pathlib.Path(__file__).parent.resolve()}/{input_file}.txt", "r") as input_file:
        farm_input = input_file.read().split("\n")

    print(get_answer_1(farm_input))

    print(get_answer_2(farm_input))
