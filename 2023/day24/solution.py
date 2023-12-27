INPUT = 'input.txt'

RANGE_MIN = 200000000000000
RANGE_MAX = 400000000000000

lines = [line.strip().split('@') for line in open(INPUT).readlines()]

def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    else:
        return False

class Hailstone:
    def __init__(self, position_str, velocity_str) -> None:
        self.position = tuple(int(p) for p in position_str.split(', '))
        self.velocity = tuple(int(v) for v in velocity_str.split(', '))
    
    def intersects(self, other, range=(RANGE_MIN, RANGE_MAX)):
        px, py = self.position[:2]
        vx, vy = self.velocity[:2]
        
        opx, opy = other.position[:2]
        ovx, ovy = other.velocity[:2]

        l1 = line((px, py), (px + vx, py + vy))
        l2 = line((opx, opy), (opx + ovx, opy + ovy))

        isect = intersection(l1, l2)

        # no intersection
        if isect == False:
            return False
    
        ix, iy = isect

        # intersection in the past
        if (ix - px) / vx < 0 or (iy - py) / vy < 0 or (ix - opx) / ovx < 0 or (iy - opy) / ovy < 0:
            return False
        
        # intersection out of range
        if not (range[0] <= ix <= range[1] and range[0] <= iy <= range[1]):
            return False
        
        return True


stones = [Hailstone(p_str, v_str) for p_str, v_str in lines]

num_intersections = 0
for i, s1 in enumerate(stones):
    for j, s2 in enumerate(stones):
        if i >= j:
            continue
        if (s1.intersects(s2)):
            num_intersections += 1

print("Num intersections:", num_intersections)