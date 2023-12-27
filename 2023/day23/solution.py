INPUT = 'input.txt'

from collections import deque

lines = [line.strip() for line in open(INPUT).readlines()]
NUM_ROWS = len(lines)
NUM_COLS = len(lines[0])

def find_starting_point():
    for i, val in enumerate(lines[0]):
        if val == '.':
            return (0, i)

SLOPES = {
    # 'v': (1, 0),
    # '>': (0, 1),
}

DIRS = (
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
)

def get_next_positions(position, visited_set):
    row, col = position
    if lines[row][col] in SLOPES:
        d_row, d_col = SLOPES[lines[row][col]]
        next_row = row + d_row
        next_col = col + d_col
        if (next_row, next_col) not in visited_set:
            return [(row + d_row, col + d_col)]
        else:
            return []
    next_pos_list = []
    for d_row, d_col in DIRS:
        next_row = row + d_row
        next_col = col + d_col
        if not (0 <= next_row < NUM_ROWS and 0 <= next_col < NUM_COLS):
            continue
        if lines[next_row][next_col] == '#':
            continue
        if (next_row, next_col) in visited_set:
            continue
        next_pos_list.append((next_row, next_col))
    return next_pos_list

# (position, steps, visited_set)
maze_q = deque()
starting_point = find_starting_point()
maze_q.append((find_starting_point(), 0, {starting_point}))

hike_lengths = []
while maze_q:
    print(len(maze_q))
    pos, steps, visited_set = maze_q.pop()
    if pos[0] == NUM_ROWS - 1:
        hike_lengths.append(steps)
        continue
    for next_pos in get_next_positions(pos, visited_set):
        new_set = set(visited_set)
        new_set.add(next_pos)
        maze_q.append((next_pos, steps + 1, new_set))

print(max(*hike_lengths))