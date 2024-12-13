import numpy as np
from tqdm import tqdm

with open("input") as f:
    lines: list[str] = [line.strip() for line in f.readlines()]

DELTA = np.ndarray
COORD = np.ndarray

machine_configs: list[tuple[DELTA, DELTA, COORD]] = []
_a = _b = _prize = None
for line in lines:
    if line.startswith("Button A"):
        _a = np.array([int(delta.split("+")[1]) for delta in line.split(": ")[1].split(", ")], dtype=int)
    elif line.startswith("Button B"):
        _b = np.array([int(delta.split("+")[1]) for delta in line.split(": ")[1].split(", ")], dtype=int)
    elif line.startswith("Prize: "):
        _prize = np.array([int(delta.split("=")[1]) for delta in line.split(": ")[1].split(", ")], dtype=int)
    else:
        machine_configs.append((_a, _b, _prize))
        _a, _b, _prize = None, None, None

if _a is not None and _b is not None and _prize is not None:
    machine_configs.append((_a, _b, _prize))

A_COST: int = 3
B_COST: int = 1

def solve_config(a_delta: DELTA, b_delta: DELTA, prize_location: COORD) -> int | None: 
    prize_x, prize_y = prize_location
    a_x, a_y = a_delta
    b_x, b_y = b_delta

    # fuck it brute force
    max_a = min(100, max(prize_x // a_x, prize_y // a_y))
    max_b = min(100, max(prize_x // b_x, prize_y // b_y))

    combos = (
        (a, b)
        for a in range(max_a + 1)
        for b in range(max_b + 1)
    )

    calc_cost = lambda tup: (tup[0] * A_COST) + (tup[1] * B_COST)
    costs = [
        calc_cost(combo)
        for combo in combos
        if np.all((combo[0] * a_delta) + (combo[1] * b_delta) == prize_location)
    ]
    if len(costs) == 0:
        return None

    return min(costs)

total: int = 0
for config in tqdm(machine_configs):
    cost = solve_config(*config)
    if cost is not None:
        total += cost
print(total)

shift = 10_000_000_000_000
machine_configs = [
    (a, b, np.asarray(prize + shift, dtype=np.int64))
    for (a, b, prize) in machine_configs
]

def solve_config_better(a_delta: DELTA, b_delta: DELTA, prize_location: COORD) -> int | None:
    x_a, y_a = a_delta
    x_b, y_b = b_delta
    x_p, y_p = prize_location

    # x_a, y_a, x_b, y_b, x_p, y_p = int(x_a), int(y_a), int(x_b), int(y_b), int(x_p), int(y_p)
    n = ((x_a * y_p) - (y_a * x_p))/((x_a*y_b) - (y_a*x_b))
    m = (x_p - (n*x_b)) / x_a

    if int(m) == m and int(n) == n:
        return int(m * A_COST + n * B_COST)
    return None
    
total = 0
for config in machine_configs:
    cost = solve_config_better(*config)
    if cost is not None:
        total += cost
print(total)