import pathlib


def print_map(obstacle_map):
    for row in obstacle_map:
        print(row)
    print("------------------------------------------------")


def find_guard(obstacle_map):
    for y, row in enumerate(obstacle_map):
        if '^' in row:
            return y, row.index('^')


class GuardStuckInALoop(Exception):
    def __init__(self):
        pass


def run_loop(event_map,
             max_height,
             max_width,
             g_y,
             g_x,
             g_orientation,
             alter_map=True,
             previous_locations=None):

    if alter_map:
        current_row = event_map[g_y]
        event_map[g_y] = current_row[:g_x] + 'X' + current_row[g_x + 1:]

    if g_y == max_height and g_orientation == 'v':
        return None, None, None
    elif g_x == max_width and g_orientation == '>':
        return None, None, None
    elif g_y == 0 and g_orientation == '^':
        return None, None, None
    elif g_x == 0 and g_orientation == '<':
        return None, None, None

    if g_orientation == "^":
        if event_map[g_y - 1][g_x] == '#':
            g_orientation = ">"
        else:
            g_y -= 1
    elif g_orientation == ">":
        if event_map[g_y][g_x + 1] == '#':
            g_orientation = "v"
        else:
            g_x += 1
    elif g_orientation == "v":
        if event_map[g_y + 1][g_x] == '#':
            g_orientation = "<"
        else:
            g_y += 1
    elif g_orientation == "<":
        if event_map[g_y][g_x - 1] == '#':
            g_orientation = "^"
        else:
            g_x -= 1

    if previous_locations is not None:
        # the tricky bug was introduced here, it used to be {g_y}{g_x}{g_orientation}
        # which would conflate a location like 12 6 ^ with 1 26 ^ and create false matches
        if f'{g_y}_{g_x}_{g_orientation}' in previous_locations:
            raise GuardStuckInALoop()
        else:
            previous_locations.add(f'{g_y}_{g_x}_{g_orientation}')

    return g_y, g_x, g_orientation


def get_answer_1(obstacle_map,
                 max_height,
                 max_width,
                 guard_y,
                 guard_x,
                 guard_orientation):
    while guard_orientation:
        guard_y, guard_x, guard_orientation = run_loop(obstacle_map,
                                                       max_height,
                                                       max_width,
                                                       guard_y,
                                                       guard_x,
                                                       guard_orientation)
    return sum([row.count('X') for row in obstacle_map])


def get_answer_2(obstacle_map,
                 max_height,
                 max_width,
                 guard_y,
                 guard_x,
                 guard_orientation):

    original_guard_y, original_guard_x, original_guard_orientation = guard_y, guard_x, guard_orientation
    loops_created = 0
    for y, row in enumerate(obstacle_map):
        for x, state in enumerate(obstacle_map[y]):
            if obstacle_map[y][x] == 'X' and not ((y == original_guard_y) and (x == original_guard_x)):
                obstacle_map_with_one_more_obstacle = obstacle_map.copy()
                new_obstacle_row = obstacle_map_with_one_more_obstacle[y]
                obstacle_map_with_one_more_obstacle[y] = new_obstacle_row[:x] + '#' + new_obstacle_row[x + 1:]
                locations = set()
                guard_y, guard_x, guard_orientation = original_guard_y, original_guard_x, original_guard_orientation
                try:
                    while guard_orientation:
                        guard_y, guard_x, guard_orientation = run_loop(obstacle_map_with_one_more_obstacle,
                                                                       max_height,
                                                                       max_width,
                                                                       guard_y,
                                                                       guard_x,
                                                                       guard_orientation,
                                                                       alter_map=False,
                                                                       previous_locations=locations)
                except GuardStuckInALoop:
                    loops_created += 1
    return loops_created


if __name__ == '__main__':

    with open(f"{pathlib.Path(__file__).parent.resolve()}/advent_of_code_6_input.txt", "r") as input_file:
        obstacle_map = []
        for line in input_file:
            obstacle_map.append(line.strip())

    max_height = len(obstacle_map) - 1
    max_width = len(obstacle_map[1]) - 1

    input_guard_y, input_guard_x = find_guard(obstacle_map)
    input_guard_orientation = "^"

    answer_1 = get_answer_1(obstacle_map,
                            max_height,
                            max_width,
                            input_guard_y,
                            input_guard_x,
                            input_guard_orientation)
    print(answer_1)
    answer_2 = get_answer_2(obstacle_map,
                            max_height,
                            max_width,
                            input_guard_y,
                            input_guard_x,
                            input_guard_orientation)
    print(answer_2)
