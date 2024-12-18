import pathlib


def check_safety(report):
    increasing = False
    decreasing = False
    previous_level = None
    for level in report:
        level = int(level)
        if previous_level is not None:
            if abs(level - previous_level) < 1 or abs(level - previous_level) > 3:
                return False
            elif level > previous_level:
                increasing = True
                if decreasing:
                    return False
            else:
                decreasing = True
                if increasing:
                    return False
        previous_level = level
    return True


def answer_1(input_lines):
    safe_count = 0
    for report in input_lines:
        levels = report.split(" ")
        safe = check_safety(levels)
        if safe:
            safe_count += 1
    return safe_count


def answer_2(input_lines):
    safe_count = 0
    for report in input_lines:
        levels = report.split(" ")
        safe = check_safety(levels)
        if safe:
            safe_count += 1
        else:
            for i in range(len(levels)):
                levels_copy = levels.copy()
                levels_copy.pop(i)
                safe = check_safety(levels_copy)
                if safe:
                    safe_count += 1
                    break
    return safe_count


if __name__ == '__main__':

    with open(f"{pathlib.Path(__file__).parent.resolve()}/advent_of_code_input.txt", "r") as input_file:
        input_lines = input_file.read().split("\n")

    print(answer_1(input_lines))

    print(answer_2(input_lines))




