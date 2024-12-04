# part 1 -- for true one-liner, replace `grid` with [list(line.strip()) for line in open("input").readlines() if len(line) > 0] and X_DIM with len(`grid_expansion`)[0] and Y_DIM with len(`grid_expansion`)

grid, Y_DIM, X_DIM = [list(line.strip()) for line in open("input").readlines() if len(line) > 0], len([list(line.strip()) for line in open("input").readlines() if len(line) > 0]), len([list(line.strip()) for line in open("input").readlines() if len(line) > 0][0])
print(
    sum(
        [
            sum(
                [
                    int(
                        grid[y][x] == "X"
                        and 0 <= xn + 2*(xn-x) < X_DIM
                        and 0 <= yn + 2*(yn-y) < Y_DIM
                        and grid[yn+(yn-y)][xn+(xn-x)] == "A"
                        and grid[yn+2*(yn-y)][xn+2*(xn-x)] == "S"
                    )
                    for yn, xn in {
                        (y+y_d, x+x_d)
                        for y_d in [-1, 0, 1]
                        for x_d in [-1, 0, 1]
                        if (0 <= (x+x_d) < X_DIM) and (0 <= (y+y_d) < Y_DIM) and (grid[y+y_d][x+x_d] == {"X": "M", "M": "A", "A": "S"}[grid[y][x]])
                    }
                ]
            )
            for x in range(X_DIM)
            for y in range(Y_DIM)
            if grid[y][x] == "X"
        ]
    )
)

# part 2
print(
    sum(
        int(
            len([
                (_y, _x)
                for _y, _x in [
                    (yn - y, xn - x)
                    for yn, xn in {
                        (y+y_d, x+x_d)
                        for y_d in [-1, 0, 1]
                        for x_d in [-1, 0, 1]
                        if (0 <= (x+x_d) < X_DIM) and (0 <= (y+y_d) < Y_DIM) and (grid[y+y_d][x+x_d] == {"X": "M", "M": "A", "A": "S"}[grid[y][x]])
                    }
                ]
                if 0 <= y - _y < Y_DIM
                and 0 <= x - _x < X_DIM
                and grid[y-_y][x-_x] == "M"
                and _y != 0 and _x != 0
            ]) > 1
        )
        for y in range(Y_DIM)
        for x in range(X_DIM)
        if grid[y][x] == "A"
    )
)

# How i actually solved it before my idiocy
def search_neighbours_for(y: int, x: int) -> set[tuple[int, int]]:
    looking_for: str = next_letter[grid[y][x]]
    occurrences: set[str] = set()
    ys = [-1, 0, 1]
    xs = [-1, 0, 1]
    for y_d in ys:
        for x_d in xs:
            if x_d == y_d == 0:
                continue
            _x = x + x_d
            _y = y + y_d
            if not (0 <= _x < X_DIM):
                continue
            if not (0 <= _y < Y_DIM):
                continue
            if grid[_y][_x] == looking_for:
                occurrences.add((_y, _x))

    return occurrences

with open("input") as f:
    grid: list[list[str]] = [list(line.strip()) for line in f.readlines() if len(line) > 0]
Y_DIM = len(grid)
X_DIM = len(grid[0])

next_letter: dict[str, str] = { "X": "M", "M": "A", "A": "S", }


# part 1
matches: int = 0
for y in range(Y_DIM):
    for x in range(X_DIM):
        if grid[y][x] != "X":
            continue
        for yn, xn in search_neighbours_for(y, x):
            y_delta = yn - y
            x_delta = xn - x
            if 0 <= xn + 2*x_delta < X_DIM:
                if 0 <= yn + 2*y_delta < Y_DIM:
                    if grid[yn+y_delta][xn+x_delta] == "A":
                        if grid[yn+2*y_delta][xn+2*x_delta] == "S":
                            matches += 1
print(matches)

# part 2
matches = 0
for y in range(Y_DIM):
    for x in range(X_DIM):
        if grid[y][x] != "A":
            continue
        neighbours = search_neighbours_for(y, x)
        if len(neighbours) < 2:
            continue
        all_vectors = [
            (yn - y, xn - x)
            for yn, xn in neighbours
        ]
        good_vectors = [
            (_y, _x)
            for _y, _x in all_vectors
            if 0 <= y - _y < Y_DIM
            and 0 <= x - _x < X_DIM
            and grid[y-_y][x-_x] == "M"
            and _y != 0 and _x != 0  # don't allow crosses
        ]
        if len(good_vectors) > 1:
            matches += 1
print(matches)


