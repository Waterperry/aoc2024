with open("input") as f:
    map: list[list[int]] = [[int(x) for x in line.strip()] for line in f.readlines()]

Y_DIM = len(map)
X_DIM = len(map[0])

potential_trailheads: list[tuple[int, int]] = []
for y in range(Y_DIM):
    for x in range(X_DIM):
        if map[y][x] == 0:
            potential_trailheads.append((y, x))

def eligible_neighbours(y: int, x: int) -> list[tuple[int, int]]:
    neighbours: list[tuple[int, int]] = []
    for dy, dx in ((-1, 0), (1, 0), (0, 1), (0, -1)):
        yn, xn = y + dy, x + dx
        if 0 <= yn < Y_DIM and 0 <= xn < X_DIM:
            if map[yn][xn] == (1 + map[y][x]):
                neighbours.append((yn, xn))
    return neighbours


total_score: int = 0
for y_init, x_init in potential_trailheads:
    distinct_peaks_reached: set[tuple[int, int]] = set()
    neighbours: list[tuple[int, int]] = eligible_neighbours(y_init, x_init)
    while len(neighbours) > 0:
        y, x = neighbours.pop(0)
        _eligible_neighbours = eligible_neighbours(y, x)
        if map[y][x] == 8:
            for peak in _eligible_neighbours:
                distinct_peaks_reached.add(peak)
        else:
            neighbours.extend(_eligible_neighbours)
    total_score += len(distinct_peaks_reached)
print(total_score)

total_score: int = 0
for y_init, x_init in potential_trailheads:
    routes_count: int = 0
    neighbours: list[tuple[int, int]] = eligible_neighbours(y_init, x_init)
    while len(neighbours) > 0:
        y, x = neighbours.pop(0)
        _eligible_neighbours = eligible_neighbours(y, x)
        if map[y][x] == 8:
            routes_count += len(_eligible_neighbours)
        else:
            neighbours.extend(_eligible_neighbours)
    total_score += routes_count
print(total_score)
