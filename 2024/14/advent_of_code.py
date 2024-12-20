import pathlib
import math

from collections import defaultdict
from dataclasses import dataclass


@dataclass
class SecurityRobot:
    position_x: int
    position_y: int
    velocity_x: int
    velocity_y: int

    def __eq__(self, other):
        return other.position_y > self.position_y

def find_safety_factor(robots, area_height, area_width):
    halfway_y = int(area_height / 2)
    halfway_x = int(area_width / 2)
    quadrants = defaultdict(int)
    for robot in robots:
        if robot.position_x < halfway_x:
            if robot.position_y < halfway_y:
                quadrants['q1'] += 1
            elif robot.position_y > halfway_y:
                quadrants['q2'] += 1
        elif robot.position_x > halfway_x:
            if robot.position_y < halfway_y:
                quadrants['q3'] += 1
            elif robot.position_y > halfway_y:
                quadrants['q4'] += 1
    return math.prod(quadrants.values())


def find_easter_egg(seconds, robots, area_height, area_width):
    display_string = f'Robots at second: {seconds}\n'
    display = defaultdict(list)
    for y in range(area_height):
        for x in range(area_width):
            display[str(y)].append(".")
    for robot in robots:
        display[str(robot.position_y)][robot.position_x] = '1'
    for rows, columns in display.items():
        display_string += ''.join(columns) + '\n'
    if '11111111111111111111111111111' in display_string:
        return display_string
    return None


def get_answer_1(robots, area_height, area_width):
    for _ in range(100):
        for robot in robots:
            robot.position_y = (robot.position_y + robot.velocity_y) % area_height
            robot.position_x = (robot.position_x + robot.velocity_x) % area_width
    return find_safety_factor(robots, area_height, area_width)


def get_answer_2(robots, area_height, area_width):
    for seconds in range(1, 20000):
        for robot in robots:
            robot.position_y = (robot.position_y + robot.velocity_y) % area_height
            robot.position_x = (robot.position_x + robot.velocity_x) % area_width
        easter_egg_display = find_easter_egg(seconds, robots, area_height, area_width)
        if easter_egg_display:
            return easter_egg_display


def init_robots(input_file):
    with open(f"{pathlib.Path(__file__).parent.resolve()}/{input_file}.txt", "r") as input_file:
        input_lines = input_file.read().split("\n")
        inputs = [input_line.split() for input_line in input_lines]
        starting_robots = []
        for starting_robot in inputs:
            position_input = starting_robot[0].removeprefix("p=").split(',')
            position_x = int(position_input[0])
            position_y = int(position_input[1])
            velocity_input = starting_robot[1].removeprefix("v=").split(',')
            velocity_x = int(velocity_input[0])
            velocity_y = int(velocity_input[1])
            robot = SecurityRobot(position_x, position_y, velocity_x, velocity_y)
            starting_robots.append(robot)
    return starting_robots


if __name__ == '__main__':

    test = False
    if test:
        area_height = 7
        area_width = 11
        input_file = "advent_of_code_test_input"
    else:
        area_height = 103
        area_width = 101
        input_file = "advent_of_code_input"

    starting_robots = init_robots(input_file)
    print(get_answer_1(starting_robots, area_height, area_width))

    starting_robots = init_robots(input_file)
    print(get_answer_2(starting_robots, area_height, area_width))
