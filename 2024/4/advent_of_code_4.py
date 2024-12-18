import pathlib
from collections import defaultdict


def count_xmas(line):
    return line.count('XMAS') + line.count('SAMX')


def get_diagonal_lines(lines):
    diagonal_lines = []
    max_index = max(len(lines[0]), len(lines))
    # get lines going from top left to bottom right
    for y in range(max_index):
        diagonal_line = ""
        k = 0
        while True:
            try:
                #print(f'{y+k},{k}')
                diagonal_line += lines[y+k][k]
                k += 1
            except IndexError:
                break
        diagonal_lines.append(diagonal_line)
    for x in range(1, max_index):
        diagonal_line = ""
        k = 0
        while True:
            try:
                #print(f'{k},{k+x}')
                diagonal_line += lines[k][k+x]
                k += 1
            except IndexError:
                break
        diagonal_lines.append(diagonal_line)
    # get lines going from bottom left to top right
    for y in sorted(range(max_index), reverse=True):
        diagonal_line = ""
        coordinates = ""
        k = 0
        while True:
            try:
                coordinates += f'{y-k},{k} - '
                diagonal_line += lines[y-k][k]
                k += 1
                if y - k < 0:
                    break
            except IndexError:
                break
        diagonal_lines.append(diagonal_line)
        # print(coordinates)
    for x in range(1, max_index):
        diagonal_line = ""
        coordinates = ""
        y = 0
        while True:
            try:
                coordinates += f'{max_index-1-y},{x+y} - '
                diagonal_line += lines[max_index-1-y][x+y]
                y += 1
            except IndexError:
                break
        diagonal_lines.append(diagonal_line)
        # print(coordinates)
    #print(diagonal_lines)
    return diagonal_lines


# answer 1
def run(input):
    xmas_count = 0
    lines = input.split("\n")
    vertical_lines = defaultdict(str)
    for row, line in enumerate(lines):
        xmas_count += count_xmas(line)
        for column, char in enumerate(line):
            vertical_lines[str(column)] += char
    for line in vertical_lines.values():
        xmas_count += count_xmas(line)
    diagonal_lines = get_diagonal_lines(lines)
    for line in diagonal_lines:
        xmas_count += count_xmas(line)
    return xmas_count


# answer 2
def run_2(input):
    xmas_count = 0
    lines = input.split("\n")
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if i - 1 < 0 or j - 1 < 0:
                continue
            elif char == 'A':
                try:
                    surrounding_pair_1 = lines[i-1][j-1] + lines[i+1][j+1]
                    surrounding_pair_2 = lines[i-1][j+1] + lines[i+1][j-1]
                    if ('M' in surrounding_pair_1 and 'S' in surrounding_pair_1) \
                            and ('M' in surrounding_pair_2 and 'S' in surrounding_pair_2):
                        xmas_count += 1
                except IndexError:
                    pass
    return xmas_count


if __name__ == '__main__':

    with open(f"{pathlib.Path(__file__).parent.resolve()}/advent_of_code_input.txt", "r") as input_file:
        input = input_file.read()

    print(run(input))

    print(run_2(input))

