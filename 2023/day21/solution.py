INPUT = 'test_input.txt'
NUM_STEPS = 5000

from collections import deque
from functools import cache

grid = [line.strip() for line in open(INPUT).readlines()]
max_rows = len(grid) - 1
max_cols = len(grid[0]) - 1

for row, line in enumerate(grid):
    for col, val in enumerate(line):
        if val == 'S':
            starting_point = (row, col)

if starting_point is None:
    raise Exception('no starting point found')

# set of (row, col, steps)
final_pos = set()
# items are tuples of (row, col, remaining steps)
position_q = deque()
row, col = starting_point
position_q.append((row, col, NUM_STEPS))

def should_process(row, col, steps):
    # if steps < 0:
    #     return False
    row = row % (max_rows + 1)
    col = col % (max_cols + 1)
    # if row < 0 or row > max_rows or col < 0 or col > max_cols:
    #     return False
    if grid[row][col] == '#':
        return False
    return True

@cache
def process(row, col, steps):
    if steps == 0:
        final_pos.add((row, col))
        return
    for d_row, d_col in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        next_row = row + d_row
        next_col = col + d_col
        next_steps = steps - 1
        if should_process(next_row, next_col, next_steps):
            position_q.append((next_row, next_col, next_steps))

while(len(position_q)):
    row, col, steps = position_q.pop()
    process(row, col, steps)

print(len(final_pos))