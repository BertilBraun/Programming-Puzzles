import re


W = 101
H = 103

W = 11
H = 7

input = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

bots = []
for line in input.split('\n'):
    match = re.match(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', line)
    assert match
    p = (int(match.group(1)), int(match.group(2)))
    v = (int(match.group(3)), int(match.group(4)))
    bots.append((p, v))


ITERATIONS = 100

for i, (p, v) in enumerate(bots):
    p = (p[0] + v[0] * ITERATIONS, p[1] + v[1] * ITERATIONS)
    p = ((p[0] + W) % W, (p[1] + H) % H)
    bots[i] = (p, v)


# count bots in each quadrant
def count_bots_in_quadrant(bots, lx, ly, hx, hy):
    count = 0
    for p, v in bots:
        if lx <= p[0] < hx and ly <= p[1] < hy:
            count += 1
    return count


ul = count_bots_in_quadrant(bots, 0, 0, W // 2, H // 2)
ur = count_bots_in_quadrant(bots, (W + 1) // 2, 0, W, H // 2)
ll = count_bots_in_quadrant(bots, 0, (H + 1) // 2, W // 2, H)
lr = count_bots_in_quadrant(bots, (W + 1) // 2, (H + 1) // 2, W, H)

print(ul, ur, ll, lr)
print(ul * ur * ll * lr)
