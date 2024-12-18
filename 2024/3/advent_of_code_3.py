import re
import pathlib


def answer_1(corrupted_memory):
    answer = 0
    matches = re.findall(r"mul\(\d{1,3},\d{1,3}\)", corrupted_memory)
    for match in matches:
        numbers = re.findall(r"\d{1,3}", match)
        answer += int(numbers[0]) * int(numbers[1])
    return answer


def answer_2(corrupted_memory):
    answer = 0
    split_by_dont = corrupted_memory.split("don't()")
    filtered_memory = split_by_dont[0]
    for section in split_by_dont:
        split_by_do = section.split("do()", 1)
        if len(split_by_do) > 1:
            filtered_memory += split_by_do[1]
    matches = re.findall(r"mul\(\d{1,3},\d{1,3}\)", filtered_memory)
    for match in matches:
        numbers = re.findall(r"\d{1,3}", match)
        answer += int(numbers[0]) * int(numbers[1])
    return answer

if __name__ == '__main__':

    with open(f"{pathlib.Path(__file__).parent.resolve()}/advent_of_code_input.txt", "r") as input_file:
        input = input_file.read()

    print(answer_1(input))

    print(answer_2(input))


