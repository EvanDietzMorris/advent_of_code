import pathlib


def get_answer(equation_inputs, operators):
    total = 0
    for equation_input in equation_inputs:
        answer, values = equation_input
        answer = int(answer)
        possible_answers = []

        # get the first two values and evaluate an expression with each operator on them
        val_1, val_2 = tuple(values[:2])
        for operator in operators:
            if operator == "||":
                sub_answer = int(val_1 + val_2)
            else:
                sub_answer = eval(f'{val_1}{operator}{val_2}')
            # save the ones that might work
            if sub_answer <= answer:
                possible_answers.append(sub_answer)

        # walk through the other values, evaluate expressions for all operators for all previous values that might work
        # again save the ones that might work and throw out the rest
        for next_value in values[2:]:
            new_possible_answers = []
            for possible_answer in possible_answers:
                for operator in operators:
                    if operator == "||":
                        sub_answer = int(str(possible_answer) + next_value)
                    else:
                        sub_answer = eval(f'{possible_answer}{operator}{next_value}')
                    if sub_answer <= answer:
                        new_possible_answers.append(sub_answer)
            possible_answers = new_possible_answers
            if not possible_answers:
                break

        # sum up the ones that worked
        if answer in possible_answers:
            total += answer

    return total


if __name__ == '__main__':

    with open(f"{pathlib.Path(__file__).parent.resolve()}/advent_of_code_7_input.txt", "r") as input_file:
        equations_input = []
        for line in input_file:
            answer, values = tuple(line.strip().split(': '))
            equations_input.append((answer, values.split(' ')))

    possible_operators = ["+", "*"]
    answer_1 = get_answer(equations_input, possible_operators)
    print(answer_1)

    possible_operators = ["+", "*", "||"]
    answer_2 = get_answer(equations_input, possible_operators)
    print(answer_2)
