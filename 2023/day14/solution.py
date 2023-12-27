import numpy

INPUT = 'input.txt'

ROLLING_ROCK = 'O'
FIXED_ROCK = '#'
GROUND = '.'

grid = [list(line.strip()) for line in open(INPUT).readlines()]

def move_rocks(grid, insertion_point, num_rocks, row_num, col_num):
    # Insert num_rocks at insertion point
    for insertion_row in range(insertion_point, insertion_point + num_rocks):
        grid[insertion_row][col_num] = ROLLING_ROCK
    # Set everything from the last rock to the current row as GROUND
    for insertion_row in range(insertion_point + num_rocks, row_num):
        grid[insertion_row][col_num] = GROUND

def shift_north(grid):
    num_rows = len(grid)
    num_cols = len(grid[0])
    for col_num in range(num_cols):
        num_rocks = 0
        insertion_point = None
        for row_num in range(num_rows):
            current_char = grid[row_num][col_num]
            if current_char == ROLLING_ROCK:
                num_rocks += 1
                if insertion_point == None:
                    insertion_point = row_num
            elif current_char == FIXED_ROCK:
                # If an insertion point has not been set, continue
                if insertion_point == None:
                    continue
                move_rocks(grid, insertion_point, num_rocks, row_num, col_num)
                # Set num_rocks to 0
                num_rocks = 0
                # Set insertion point to NONE until one can be found
                insertion_point = None
            elif current_char == GROUND:
                if insertion_point == None:
                    insertion_point = row_num
            if row_num == num_rows - 1 and insertion_point is not None and num_rocks > 0:
                move_rocks(grid, insertion_point, num_rocks, row_num + 1, col_num)

def one_cycle(grid):
    for i in range(4):
        shift_north(grid)
        grid = numpy.rot90(grid, axes=(1,0))
    return grid

for i in range(1000):
    grid = one_cycle(grid)
    total_load = 0
    num_rows = len(grid)
    for row_num, row in enumerate(grid):
        for char in row:
            if char == ROLLING_ROCK:
                total_load += (num_rows - row_num)

    print(i+1, total_load)