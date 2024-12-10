import pathlib


def find_trailheads(topography):
    trailheads = []
    for y, topography_line in enumerate(topography):
        for x, height in enumerate(topography_line):
            if height == 0:
                trailheads.append((y, x))
    return trailheads


def get_answer_1(topography):
    score = 0
    trailheads = find_trailheads(topography)
    for trailhead in trailheads:
        current_height = 0
        current_trails = [trailhead]
        while current_trails:
            # possible_trails = set()   # for answer one use a set here
            possible_trails = []    # for answer two use a list
            for (current_y, current_x) in current_trails:
                try:
                    possible_y, possible_x = current_y, current_x + 1
                    if topography[possible_y][possible_x] == current_height + 1:
                        # possible_trails.add((possible_y, possible_x))  # for answer one these are sets
                        possible_trails.append((possible_y, possible_x))
                except IndexError:
                    pass
                try:
                    possible_y, possible_x = current_y + 1, current_x
                    if topography[possible_y][possible_x] == current_height + 1:
                        possible_trails.append((possible_y, possible_x))
                except IndexError:
                    pass
                try:
                    possible_y, possible_x = current_y, current_x - 1
                    if possible_x >= 0 and topography[possible_y][possible_x] == current_height + 1:
                        possible_trails.append((possible_y, possible_x))
                except IndexError:
                    pass
                try:
                    possible_y, possible_x = current_y - 1, current_x
                    if possible_y >= 0 and topography[possible_y][possible_x] == current_height + 1:
                        possible_trails.append((possible_y, possible_x))
                except IndexError:
                    pass

            if current_height == 8:
                score += len(possible_trails)
                current_trails = None
            else:
                current_height += 1
                current_trails = possible_trails
    return score


if __name__ == '__main__':

    # input_file = "advent_of_code_test_input"
    input_file = "advent_of_code_input"
    with open(f"{pathlib.Path(__file__).parent.resolve()}/{input_file}.txt", "r") as input_file:
        intput_topography = []
        for line in input_file:
            intput_topography.append([int(intput_height) for intput_height in line.strip()])

    answer_1 = get_answer_1(intput_topography)
    print(answer_1)

