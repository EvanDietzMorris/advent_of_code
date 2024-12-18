import pathlib
import itertools
import math
from functools import cache


@cache
def process_stone(stone):
    if stone == 0:
        return [1]

    num_digits = int(math.log10(stone))+1  # avoid converting to string (thanks stack overflow)
    if num_digits % 2 == 0:
        half_digits = int(num_digits / 2)
        stone_string = str(stone)
        return [int(stone_string[:half_digits]), int(stone_string[half_digits:])]

    return [stone*2024]


def process_blinks_brute_force(stones, blinks):
    for i in range(blinks):
        stones = list(itertools.chain.from_iterable(map(process_stone, stones)))
    return len(stones)


def get_answer_1(stones, blinks):
    print(f'input: {stones}')
    return process_blinks_brute_force(stones, blinks)


@cache
def process_stones_recursively(stone, blinks):
    if blinks == 0:
        return 0
    stones_sum = 0
    stones_after_blink = process_stone(stone)  # run the rules on one stone
    stones_sum += len(stones_after_blink) - 1  # add to the sum if an additional one was created
    for new_stone in stones_after_blink:
        stones_sum += process_stones_recursively(new_stone, blinks - 1)  # recursively do the next blink for each new stone
    return stones_sum


def get_answer_2(stones, blinks):
    total = len(stones)
    for stone in stones:
        total += process_stones_recursively(stone, blinks)
    return total


if __name__ == '__main__':

    # input_file = "advent_of_code_test_input"
    input_file = "advent_of_code_input"
    with open(f"{pathlib.Path(__file__).parent.resolve()}/{input_file}.txt", "r") as input_file:
        stones_input = [int(stone_input) for stone_input in input_file.read().split()]

    blinks_input = 25
    answer_1 = get_answer_1(stones_input, blinks_input)
    print(answer_1)

    blinks_input = 75
    answer_2 = get_answer_2(stones_input, blinks_input)
    print(answer_2)

