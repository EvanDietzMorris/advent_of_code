import pathlib


def find_robot_starting_position(warehouse):
    for y, row in enumerate(warehouse):
        for x, position in enumerate(row):
            if position == '@':
                warehouse[y][x] = "."  # set it to empty, then don't have to check for collisions or move the robot
                return y, x


def calculate_gps_sum(warehouse, box_character='O'):
    gps_sum = 0
    for y, row in enumerate(warehouse):
        for x, position in enumerate(row):
            if position == box_character:
                gps_sum += 100 * y + x
    return gps_sum


def get_answer_1(warehouse, moves):

    robot_y, robot_x = find_robot_starting_position(warehouse)

    for move in moves:
        if move == "<":
            y_change = 0
            x_change = -1
        elif move == "^":
            y_change = -1
            x_change = 0
        elif move == ">":
            y_change = 0
            x_change = 1
        else:  # move == "v":
            y_change = 1
            x_change = 0

        desired_y = robot_y + y_change
        desired_x = robot_x + x_change
        if warehouse[desired_y][desired_x] == ".":
            robot_y, robot_x = desired_y, desired_x
        elif warehouse[desired_y][desired_x] == "#":
            pass
        else:  # warehouse[desired_y][desired_x] == "O":
            looking_for_wall_or_empty = True
            move_possible = False
            next_y, next_x = desired_y, desired_x
            while looking_for_wall_or_empty:
                next_y, next_x = next_y + y_change, next_x + x_change
                if warehouse[next_y][next_x] == ".":
                    warehouse[next_y][next_x] = "O"
                    warehouse[desired_y][desired_x] = "."
                    looking_for_wall_or_empty = False
                    move_possible = True
                elif warehouse[next_y][next_x] == "#":
                    looking_for_wall_or_empty = False
                    move_possible = False
            if move_possible:
                robot_y, robot_x = desired_y, desired_x

    return calculate_gps_sum(warehouse)


def get_answer_2(warehouse, moves):

    robot_y, robot_x = find_robot_starting_position(warehouse)

    for move in moves:
        if move == "<":
            y_change = 0
            x_change = -1
        elif move == "^":
            y_change = -1
            x_change = 0
        elif move == ">":
            y_change = 0
            x_change = 1
        else:  # move == "v":
            y_change = 1
            x_change = 0

        desired_y = robot_y + y_change
        desired_x = robot_x + x_change
        if warehouse[desired_y][desired_x] == ".":  # if the robot can move do it and move on
            robot_y, robot_x = desired_y, desired_x
        elif warehouse[desired_y][desired_x] == "#":  # if the robot cant move do nothing and move on
            pass
        else:
            # otherwise there's a box in the way, record it's full position
            if warehouse[desired_y][desired_x] == "[":
                box_y, box_x_1, box_x_2 = desired_y, desired_x, desired_x + 1
            else:
                # warehouse[desired_y][desired_x] == "]":
                box_y, box_x_1, box_x_2 = desired_y, desired_x - 1, desired_x

            # check to make sure boxes can move until they all can or until you hit a wall
            looking_for_wall_or_empty = True
            move_possible = False
            all_boxes_to_move = [(box_y, box_x_1, box_x_2)]
            boxes_to_move = all_boxes_to_move.copy()
            while looking_for_wall_or_empty:
                next_boxes_to_move = []
                hits_wall = False
                for (box_y, box_x_1, box_x_2) in boxes_to_move:

                    # determine the positions that need to be checked to see if this box can move
                    next_y, next_x_1, next_x_2 = box_y + y_change, box_x_1 + x_change, box_x_2 + x_change
                    if y_change == 0:
                        if x_change > 0:
                            spots_to_check = [(next_y, next_x_2)]
                        else:
                            spots_to_check = [(next_y, next_x_1)]
                    else:
                        spots_to_check = [(next_y, next_x_1), (next_y, next_x_2)]

                    for (spot_y, spot_x) in spots_to_check:
                        if warehouse[spot_y][spot_x] == "#":
                            hits_wall = True
                            break
                        elif warehouse[spot_y][spot_x] == "[":  # if another box in the way add it to the queue
                            if (spot_y, spot_x, spot_x+1) not in next_boxes_to_move:
                                next_boxes_to_move.append((spot_y, spot_x, spot_x+1))
                        elif warehouse[spot_y][spot_x] == "]":
                            if (spot_y, spot_x-1, spot_x) not in next_boxes_to_move:
                                next_boxes_to_move.append((spot_y, spot_x-1, spot_x))

                    if hits_wall:
                        move_possible = False
                        looking_for_wall_or_empty = False
                        break

                if next_boxes_to_move:
                    all_boxes_to_move.extend(next_boxes_to_move)
                    boxes_to_move = next_boxes_to_move
                elif not hits_wall:
                    move_possible = True
                    looking_for_wall_or_empty = False

            if move_possible:
                robot_y, robot_x = desired_y, desired_x
                for (box_y, box_x_1, box_x_2) in reversed(all_boxes_to_move):
                    warehouse[box_y][box_x_1] = "."
                    warehouse[box_y][box_x_2] = "."
                    warehouse[box_y + y_change][box_x_1 + x_change] = "["
                    warehouse[box_y + y_change][box_x_2 + x_change] = "]"

    return calculate_gps_sum(warehouse, box_character='[')


def read_input():
    test = False
    if test:
        input_file = "advent_of_code_test_input"
    else:
        input_file = "advent_of_code_input"
    with open(f"{pathlib.Path(__file__).parent.resolve()}/{input_file}.txt", "r") as input_file:
        inputs = input_file.read().split("\n\n")
        warehouse = [list(warehouse_line) for warehouse_line in inputs[0].split("\n")]
        moves = "".join(inputs[1].split("\n"))
    return warehouse, moves


def convert_to_double_wide(warehouse):
    double_wide_warehouse = []
    for row in warehouse:
        double_wide_row = []
        for position in row:
            if position == "#":
                double_wide_row.extend(["#", "#"])
            elif position == "O":
                double_wide_row.extend(["[", "]"])
            elif position == ".":
                double_wide_row.extend([".", "."])
            elif position == "@":
                double_wide_row.extend(["@", "."])
        double_wide_warehouse.append(double_wide_row)
    return double_wide_warehouse


if __name__ == '__main__':

    warehouse, moves = read_input()
    print(get_answer_1(warehouse, moves))

    warehouse, moves = read_input()
    warehouse = convert_to_double_wide(warehouse)
    print(get_answer_2(warehouse, moves))
