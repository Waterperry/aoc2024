with open("input") as f:
    grid: list[list[str]] = [list(l.strip()) for l in f.readlines()]

X_DIM = len(grid[0])
Y_DIM = len(grid)
DELTAS: list[tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def get_whole_region(y: int, x: int) -> set[tuple[int, int]]:
    frontier: set[tuple[int, int]] = {(y, x)}
    region: set[tuple[int, int]] = set()
    while len(frontier) > 0:
        yn, xn = frontier.pop()
        region.add((yn, xn))
        for dy, dx in DELTAS:
            _y, _x= yn + dy, xn + dx
            if (0 <= _y < Y_DIM) and (0 <= _x < X_DIM) and (grid[_y][_x] == grid[y][x]):
                frontier.add((_y, _x))
        frontier.difference_update(region)
    return region

regions: list[set[tuple[int, int]]] = []
for y in range(Y_DIM):
    for x in range(X_DIM):
        if any((y, x) in region for region in regions):
            continue
        regions.append(get_whole_region(y, x))


def part1() -> None:
    def calculate_perimeter(y: int, x: int, region: set[tuple[int, int]]) -> int:
        num_neighbours: int = 0
        for dy, dx in DELTAS:
            yn, xn = y + dy, x + dx
            if (yn, xn) in region:
                num_neighbours += 1

        match num_neighbours:
            case 0:
                return 4
            case 1:
                return 3
            case 2:
                return 2
            case 3:
                return 1
            case 4: 
                return 0
        raise ValueError

    cost: int = 0
    for region in regions:
        area: int = len(region)
        perimeter: int = 0
        for y, x in region:
            perimeter += calculate_perimeter(y, x, region)
        cost += area * perimeter

    print(cost)

part1()


def part2() -> None:
    def calculate_contiguous_regions(target: set[tuple[int, int]], dy: int, dx: int) -> int:
        contig_delta_map: dict[tuple[int, int], tuple[int, int]] = {
            (1, 0): (0, 1),
            (0, 1): (1, 0),
            (-1, 0): (0, 1),
            (0, -1): (1, 0),
        }
        if len(target) == 0:
            return 0
        if len(target) == 1:
            return 1

        # will only ever be 1d
        l_target: list[tuple[int, int]] = sorted(target)

        num_contiguous: int = 1
        for (y1, x1), (y2, x2) in zip(l_target[:-1], l_target[1:]):
            cdy, cdx = contig_delta_map[(dy, dx)]
            if (y1 + cdy, x1 + cdx) != (y2, x2):
                num_contiguous += 1
        return num_contiguous

    def scan_with_delta(region: set[tuple[int, int]], dy: int, dx: int) -> int:
        assert not dy or not dx, "no diagonal deltas"

        all_ys: set[int] = {_y for _y, _ in region}
        all_xs: set[int] = {_x for _, _x in region}

        frontier: list[tuple[int, int]]
        if dy > 0:  # frontier is flat line moving from top to bottom
            frontier = [(min(all_ys), x) for x in all_xs]
        elif dy < 0:  # frontier is flat line moving from bottom to top
            frontier = [(max(all_ys), x) for x in all_xs]
        elif dx > 0:  # frontier is vertical line moving from left to right
            frontier = [(y, min(all_xs)) for y in all_ys]
        elif dx < 0:  # frontier is vertical line moving from right to left
            frontier = [(y, max(all_xs)) for y in all_ys]
        else:
            raise ValueError("")

        num_edges: int = 0
        frontier_activation_mask: list[bool] = [True for _ in frontier]
        while any(0 <= y < Y_DIM and 0 <= x < X_DIM for y, x in frontier):
            # target is all tiles in frontier that are also in region
            target: set[tuple[int, int]] = set()
            for frontier_pos, activated in zip(frontier, frontier_activation_mask):
                if not activated:
                    continue
                if frontier_pos in region:
                    target.add(frontier_pos)
            
            num_contiguous_regions = calculate_contiguous_regions(target, dy, dx)
            num_edges += num_contiguous_regions

            # for each coord in target, disable the frontier at that point
            for coord in target:
                frontier_idx = frontier.index(coord)
                frontier_activation_mask[frontier_idx] = False
            
            # for each point in the frontier which doesn't belong to the region, reenable the frontier
            for frontier_pos in frontier:
                if frontier_pos not in region:
                    frontier_idx = frontier.index(frontier_pos)
                    frontier_activation_mask[frontier_idx] = True

            frontier = [(y + dy, x + dx) for y, x in frontier]

        return num_edges

    total_cost: int = 0
    for region in regions:
        y, x = list(region)[0]
        region_id: str = grid[y][x]
        area: int = len(region)
        num_edges: int = 0
        for delta in DELTAS:
            num_edges += scan_with_delta(region, *delta)
        total_cost += area * num_edges
    print(total_cost)
        

part2()
