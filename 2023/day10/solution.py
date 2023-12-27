INPUT = 'input.txt'
grid = [list(line.strip()) for line in open(INPUT).readlines()]
 
"""
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't
  show what shape the pipe has.
"""
 
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
DONE = 5
 
PIPE_TO_ENTRY_EXIT_MAP = {
     '|': {UP: UP, DOWN: DOWN},
     '-': {LEFT: LEFT, RIGHT: RIGHT},
     'L': {DOWN: RIGHT, LEFT: UP},
     'J': {RIGHT: UP, DOWN: LEFT},
     '7': {RIGHT: DOWN, UP: LEFT},
     'F': {UP: RIGHT, LEFT: DOWN},
     'S': {UP: DONE, DOWN: DONE, LEFT: DONE, RIGHT: DONE},
}
 
DIR_TO_DELTAS = {
     UP: (-1, 0),
     DOWN: (1, 0),
     LEFT: (0, -1),
     RIGHT: (0, 1),
     DONE: (0, 0),
}
 
points_on_path = set()
 
def find_s():
    for row_num, row in enumerate(grid):
        for col_num, col in enumerate(row):
            if col == 'S':
                return (row_num, col_num)
 
def is_valid_point(row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[row])
 
def get_exit_direction(row, col, entry_dir):
     if not is_valid_point(row, col):
          return None
     cell_char = grid[row][col]
     entry_exit_map = PIPE_TO_ENTRY_EXIT_MAP.get(cell_char)
     if not entry_exit_map:
          return None
     return entry_exit_map.get(entry_dir)
 
def can_be_entered_in_direction(row, col, entry_dir):
    return get_exit_direction(row, col, entry_dir) != None
 
def find_starting_direction(row, col):
    for direction, (d_row, d_col) in DIR_TO_DELTAS.items():
        if can_be_entered_in_direction(row + d_row, col + d_col, direction):
            return (row + d_row, col + d_col), direction
 
start_row, start_col = find_s()
points_on_path.add((start_row, start_col))
 
(row, col), direction = find_starting_direction(start_row, start_col)
 
num_steps = 0
 
while (direction != DONE):
    points_on_path.add((row, col))
    direction = get_exit_direction(row, col, direction)
    if direction == None:
        raise Exception('exit direction not found')
    deltas = DIR_TO_DELTAS.get(direction)
    if deltas == None:
        raise Exception('deltas not found')
    row += deltas[0]
    col += deltas[1]
    num_steps += 1
 
 
print(num_steps / 2.0)
 
for row_num, row in enumerate(grid):
    for col_num, cell_val in enumerate(row):
        if cell_val != '.' and (row_num, col_num) not in points_on_path:
            grid[row_num][col_num] = '.'
        if cell_val == 'S':
            # HACK ALERT! This is only because that's how S works in my input.
            grid[row_num][col_num] = '-'
 
inside_count = 0
for row_num, row in enumerate(grid):
    row_str = []
    num_ups = 0
    num_downs = 0
    inside = False
    for col_num, cell_val in enumerate(row):
        if cell_val == '.':
            if inside:
                inside_count += 1
                row_str.append('I')
            else:
                row_str.append('O')
        else:
            row_str.append(cell_val)
        entry_exit_map = PIPE_TO_ENTRY_EXIT_MAP.get(cell_val)
        if entry_exit_map is None:
            continue
        if UP in entry_exit_map:
            num_ups += 1
        if DOWN in entry_exit_map:
            num_downs += 1
        inside = (num_ups % 2 == 1) and (num_downs % 2 == 1)
    print(''.join(row_str))
 
 
print(inside_count)