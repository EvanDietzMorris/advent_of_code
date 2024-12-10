import pathlib
from collections import defaultdict


def get_answer_1(disk_map):

    # split the input into two parallel arrays
    file_sizes = [int(disk_map[i]) for i in range(0, len(disk_map), 2)]
    free_spaces = [int(disk_map[i]) for i in range(1, len(disk_map), 2)]

    block = 0
    checksum = 0
    # keep track of which file is at the end of the disk
    last_file_index = len(file_sizes) - 1
    # walk through the files, i represents the file id
    for i in range(len(file_sizes)):
        file_size = file_sizes[i]
        free_space = free_spaces[i]
        # walk through blocks for the current file, calculating the checksum
        for b in range(file_size):
            checksum += block * i
            block += 1
        # if i == last_file_index we've already 'moved' all the remaining files
        if i == last_file_index:
            break
        # walk through blocks of free space
        for space in range(free_space):
            # find the next file which still has size/content
            while file_sizes[last_file_index] == 0:
                last_file_index -= 1
            # 'move' files from the end by subtracting 1 from the size of those files
            file_sizes[last_file_index] -= 1
            checksum += block * last_file_index
            block += 1
    return checksum


def get_answer_2(disk_map):

    # split the input into two parallel arrays
    file_sizes = [int(disk_map[i]) for i in range(0, len(disk_map), 2)]
    free_spaces = [int(disk_map[i]) for i in range(1, len(disk_map), 2)]

    free_spaces.append(0)

    moved_files = defaultdict(list)
    # walk backwards through the files, i represents the file id
    for i in range(len(file_sizes)-1, -1, -1):
        file_size = file_sizes[i]
        # for each free space see if the file fits, j represents the free space index
        for j in range(i):
            # if so 'move' it
            if file_size <= free_spaces[j]:
                moved_files[str(j)].append((i, file_size))
                free_spaces[j] -= file_size  # reduce the free space size where it moved to
                free_spaces[i-1] += file_size  # increase the free space size it moved from
                file_sizes[i] = 0  # "move" the whole file
                break

    block = 0
    checksum = 0
    # walk through the files, i represents the file id
    for i in range(len(file_sizes)):
        file_size = file_sizes[i]
        free_space = free_spaces[i]
        # walk through blocks for the current file, calculating the checksum
        for b in range(file_size):
            checksum += block * i
            block += 1
        # see if files were moved to this free space
        if str(i) in moved_files:
            # if so add them to the check sum
            for moved_file_id, file_size in moved_files[str(i)]:
                for b in range(file_size):
                    checksum += block * moved_file_id
                    block += 1
        # skip any remaining free space
        block += free_space
    return checksum


if __name__ == '__main__':

    # input_file = "advent_of_code_test_input"
    input_file = "advent_of_code_input"
    with open(f"{pathlib.Path(__file__).parent.resolve()}/{input_file}.txt", "r") as input_file:
        input_disk_map = input_file.read()

    answer_1 = get_answer_1(input_disk_map)
    print(answer_1)

    answer_2 = get_answer_2(input_disk_map)
    print(answer_2)

