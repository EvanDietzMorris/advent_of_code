import pathlib

def answer_1(column_1, column_2):
    distance = 0
    for val_1, val_2 in zip(sorted(column_1), sorted(column_2)):
        absolute_distance = abs(int(val_1) - int(val_2))
        distance += absolute_distance
    return distance


def answer_2(column_1, column_2):
    similarity_score = 0
    for val_1 in column_1:
        similarity_score += val_1 * column_2.count(val_1)
    return similarity_score


if __name__ == '__main__':

    with open(f"{pathlib.Path(__file__).parent.resolve()}/advent_of_code_input.txt", "r") as input_file:
        column_1 = []
        column_2 = []
        for input in input_file.read().split("\n"):
            column_1.append(int(input.split()[0]))
            column_2.append(int(input.split()[1]))

    print(answer_1(column_1, column_2))
    print(answer_2(column_1, column_2))
