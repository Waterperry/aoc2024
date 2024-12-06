with open("input") as f:
    map: list[str] = [line.strip() for line in f.readlines()]

Y_DIM = len(map)
X_DIM = len(map[0])


def get_start() -> tuple[int, int]:
    global map

    for y in range(Y_DIM):
        for x in range(X_DIM):
            if map[y][x] == "^":
                return y, x
    raise ValueError("can't find start symbol")


start_pos: tuple[int, int] = get_start()


def part1() -> set[tuple[int, int]]:
    current_delta = (-1, 0)
    next_delta: dict[tuple[int, int], tuple[int, int]] = {
        (-1, 0): (0, 1),
        (0, 1): (1, 0),
        (1, 0): (0, -1),
        (0, -1): (-1, 0),
    }

    y, x = start_pos
    visited: int = 1
    visited_tiles: set[tuple[int, int]] = {(y, x)}

    while True:
        dy, dx = current_delta
        yn, xn = y + dy, x + dx
        if not (0 <= xn < X_DIM and 0 <= yn < Y_DIM):
            break
        elif map[yn][xn] == "#":
            current_delta = next_delta[current_delta]
        else:
            y, x = yn, xn
            if (y, x) not in visited_tiles:
                visited_tiles.add((y, x))
                visited += 1

    print(visited)
    return visited_tiles


visited_tiles: dict[tuple[int, int]] = part1()


# part 2
def is_loop(_map: list[str], replaced_tile: tuple[int, int]) -> bool:
    if _map[replaced_tile[0]][replaced_tile[1]] in {"#", "^"}:
        return False

    current_delta = (-1, 0)
    next_delta: dict[tuple[int, int], tuple[int, int]] = {
        (-1, 0): (0, 1),
        (0, 1): (1, 0),
        (1, 0): (0, -1),
        (0, -1): (-1, 0),
    }

    y, x = start_pos
    visited_tiles: set[tuple[int, int, str]] = {(y, x, current_delta)}

    while True:
        dy, dx = current_delta
        yn, xn = y + dy, x + dx
        if not (0 <= xn < X_DIM and 0 <= yn < Y_DIM):
            return False
        elif _map[yn][xn] == "#" or (yn, xn) == replaced_tile:
            current_delta = next_delta[current_delta]
        else:
            y, x = yn, xn
            if (y, x, current_delta) in visited_tiles:
                return True
            visited_tiles.add((y, x, current_delta))


loops: int = 0
for candidate in visited_tiles:
    if is_loop(map, replaced_tile=candidate):
        loops += 1

print(loops)
