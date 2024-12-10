import functools
import pathlib
import random
from itertools import permutations
from collections import defaultdict

RULE_LOOKUP = None

def is_correct(update, rule_lookup):
    previous_pages = []
    for page in update:
        if any(not_allowed_page in previous_pages for not_allowed_page in rule_lookup[page]):
            return False
        previous_pages.append(page)
    return True

def compare_pages(page_1, page_2):
    if page_2 in RULE_LOOKUP[page_1]:
        return 1
    elif page_1 in RULE_LOOKUP[page_2]:
        return -1
    else:
        return 1


# answer 1
def run(rule_lookup, updates):
    answer = 0
    for update in updates:
        if is_correct(update, rule_lookup):
            # find the middle value and add it to the total, using int() to floor the decimal values ie 2.5 becomes 2
            answer += int(update[int(len(update)/2)])
    return answer


# answer 2
def run_2_pray(rule_lookup, updates):
    answer = 0
    for update in updates:
        if not is_correct(update, rule_lookup):
            random.shuffle(update)
            while not is_correct(update, rule_lookup):
                random.shuffle(update)
            # find the middle value and add it to the total, using int() to floor the decimal values ie 2.5 becomes 2
            answer += int(update[int(len(update)/2)])
    return answer


def run_2_brute_force(rule_lookup, updates):
    answer = 0
    for update in updates:
        if not is_correct(update, rule_lookup):
            for update_permutation in permutations(update):
                if is_correct(update_permutation, rule_lookup):
                    # find the middle value and add it to the total, using int() to floor the decimal values ie 2.5 becomes 2
                    answer += int(update_permutation[int(len(update_permutation)/2)])
                    break
    return answer


def run_2(rule_lookup, updates):
    answer = 0
    for update in updates:
        if not is_correct(update, rule_lookup):
            print(update)
            update.sort(key=functools.cmp_to_key(compare_pages))
            print(update)
            answer += int(update[int(len(update) / 2)])
    return answer


if __name__ == '__main__':

    with open(f"{pathlib.Path(__file__).parent.resolve()}/advent_of_code_5_input.txt", "r") as input_file:
        # parse input
        rules = []
        updates = []
        for line in input_file:
            # make lists of the input rows and convert them all to ints
            if '|' in line:
                rules.append(list(map(int, line.strip().split('|'))))
            elif ',' in line:
                updates.append(list(map(int, line.strip().split(','))))

    # turn rules into lookup
    rule_lookup = defaultdict(list)
    for rule in rules:
        rule_lookup[rule[0]].append(rule[1])
    RULE_LOOKUP = rule_lookup

    answer_1 = run(rule_lookup, updates)
    print(answer_1)

    answer_2 = run_2(rule_lookup, updates)
    print(answer_2)

