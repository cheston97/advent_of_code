INPUT = 'input.txt'

from collections import deque
import itertools
import math

instructions = [line.strip().split(' ') for line in open(INPUT).readlines()]

DELTAS = {
    'R': (0, 1),
    'L': (0, -1),
    'U': (-1, 0),
    'D': (1, 0),
}

# Map of (row, col) to color value
GRID = {}

ROW = 0
COL = 0

for dir, steps, color in instructions:
    steps = int(steps)
    deltas = DELTAS[dir]
    for i in range(steps):
        ROW += deltas[0]
        COL += deltas[1]
        GRID[(ROW, COL)] = color

MIN_ROW = math.inf
MAX_ROW = -math.inf
MIN_COL = math.inf
MAX_COL = -math.inf

for row, col in GRID:
    MIN_ROW = min(row, MIN_ROW)
    MAX_ROW = max(row, MAX_ROW)
    MIN_COL = min(col, MIN_COL)
    MAX_COL = max(col, MAX_COL)

def print_grid():
    for row in range(MIN_ROW, MAX_ROW + 1):
        current_row = []
        for col in range(MIN_COL, MAX_COL + 1):
            if (row, col) in GRID:
                current_row.append('#')
            else:
                current_row.append('.')
        print(''.join(current_row))

# print_grid()

# Find a fill starting point on 2nd row
flood_points = deque()
# for i in range(MIN_COL, MAX_COL + 1):
#     if (MIN_ROW, i) in GRID:
#         flood_points.append((MIN_ROW + 1, i + 1))
flood_points.append((MIN_ROW + 63, MIN_COL + 5))
# flood_points.append((MIN_ROW + 2, MIN_COL + 3))

while flood_points:
    row, col = flood_points.pop()
    GRID[(row, col)] = '#'
    for d_row, d_col in itertools.product((-1, 0, 1), (-1, 0, 1)):
        if d_row == 0 and d_col == 0:
            continue
        new_row = row + d_row
        new_col = col + d_col
        if MIN_ROW < new_row < MAX_ROW and MIN_COL < new_col < MAX_COL and (new_row, new_col) not in GRID:
            flood_points.append((new_row, new_col))

# print('*' * 50)
# print_grid()

print(len(GRID))