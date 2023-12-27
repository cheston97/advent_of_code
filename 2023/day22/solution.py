INPUT = 'input.txt'

from copy import copy

class Brick:
    def __init__(self, name, start_cell, end_cell):
        self.name = name
        self.flat_points = None
        self.z_min = None
        self.z_max = None
        self.supports = set()
        self.supported_by = set()
        self._set_points(start_cell, end_cell)
    
    def _set_points(self, start_cell, end_cell):
        self.flat_points = set()
        x1, y1, z1 = start_cell
        x2, y2, z2 = end_cell
        self.z_min = z1
        self.z_max = z2
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.flat_points.add((x, y))

    def fall_to_z(self, z):
        if z > self.z_min:
            raise Exception("can't fall upwards")
        d_z = self.z_min - z
        self.z_min -= d_z
        self.z_max -= d_z
        return d_z > 0
    
    def place_on_top_of(self, other):
        did_fall = self.fall_to_z(other.z_max + 1)
        self.supported_by.add(other)
        other.supports.add(self)
        return did_fall

    def is_supported(self):
        return len(self.supported_by) > 0

    def intersects(self, other):
        return bool(self.flat_points.intersection(other.flat_points))
    
    def is_removable(self):
        for b in self.supports:
            if len(b.supported_by) == 1:
                return False
        return True

    def __str__(self):
        return 'Brick(%s)' % self.name
    
    def __repr__(self):
        return str(self)

def copy_brick(brick):
    new_brick = copy(brick)
    new_brick.supports = set()
    new_brick.supported_by = set()
    new_brick.flat_points = copy(brick.flat_points)
    return new_brick

ORIGINAL_BRICKS = []
lines = [line.strip() for line in open(INPUT).readlines()]
for i, line in enumerate(lines):
    name = chr(ord('A') + i)
    p1_str, p2_str = line.split('~')
    p1 = [int(x) for x in p1_str.split(',')]
    p2 = [int(x) for x in p2_str.split(',')]
    ORIGINAL_BRICKS.append(Brick(name, p1, p2))

# Destroys the input
def cascade(original_bricks):
    fallen_bricks = []
    num_moved = 0
    original_bricks.sort(key=lambda b: b.z_min, reverse=True)
    while len(original_bricks):
        original = original_bricks.pop()
        for fallen in sorted(fallen_bricks, key=lambda b: b.z_max, reverse=True):
            if original == fallen:
                continue
            if original.is_supported() and original.z_min > fallen.z_max + 1:
                break
            if not original.is_supported():
                if original.intersects(fallen):
                    if original.place_on_top_of(fallen):
                        num_moved += 1
                    fallen_bricks.append(original)
                    continue
            if original.is_supported() and original.z_min == fallen.z_max + 1 and original.intersects(fallen):
                if original.place_on_top_of(fallen):
                    num_moved += 1
        if not original.is_supported():
            if original.fall_to_z(1):
                num_moved += 1
            fallen_bricks.append(original)
    return fallen_bricks, num_moved

FALLEN_BRICKS, num_moved = cascade(ORIGINAL_BRICKS)

# Part 1
total_removable = 0
for b in FALLEN_BRICKS:
    if b.is_removable():
        total_removable += 1

print('Part 1:', total_removable)

# Part 2
total_moved = 0
for i, b in enumerate(FALLEN_BRICKS):
    print ('Testing brick number', i)
    # Make a deep copy of the bricks list and get rid of the test brick
    bricks = [copy_brick(brick) for brick in FALLEN_BRICKS]
    bricks.pop(i)
    # Remove all supports and cascade
    for brick in bricks:
        brick.supported_by = set()
        brick.supports = set()
    _, num_moved = cascade(bricks)
    total_moved += num_moved

print('Part 2:', total_moved)
