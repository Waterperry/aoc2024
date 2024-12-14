from functools import reduce

with open("input") as f:
    lines: list[str] = [line.strip() for line in f.readlines()]

X_DIM: int = 101  # 11
Y_DIM: int = 103  # 7

class Robot:
    def __init__(self, x: int, y: int, dx: int, dy: int) -> None:
        self.x: int = x
        self.y: int = y
        self.dx: int = dx
        self.dy: int = dy

    def move(self) -> None:
        self.x += self.dx
        self.y += self.dy

        self.x %= X_DIM
        self.y %= Y_DIM
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y}) + ({self.dx}, {self.dy})"

def print_grid(_robots: list[Robot]) -> None:
    for y in range(Y_DIM):
        for x in range(X_DIM):
            num_robots: int = 0
            for _robot in _robots:
                if _robot.x == x and _robot.y == y:
                    num_robots += 1
            if num_robots == 0:
                print(".", end="")
            else:
                print(num_robots, end="")
        print()
    print("\n\n")
 
robots: list[Robot] = []
for line in lines:
    p, v = line.split(" ")
    x, y = map(int, p.split("=")[1].split(","))
    dx, dy = map(int, v.split("=")[1].split(","))
    robots.append(Robot(x, y, dx, dy))
for _ in range(100):
    for robot in robots:
        robot.move()
        
quadrants_count: list[int] = [0, 0, 0, 0]
for robot in robots:
    if robot.x == X_DIM // 2 or robot.y == Y_DIM // 2:
        continue
    idx = 2 * int(robot.x < X_DIM // 2) + int(robot.y < Y_DIM // 2)
    quadrants_count[idx] += 1
    
print(reduce(lambda x, y: x * y, quadrants_count))

robots = []
for line in lines:
    p, v = line.split(" ")
    x, y = map(int, p.split("=")[1].split(","))
    dx, dy = map(int, v.split("=")[1].split(","))
    robots.append(Robot(x, y, dx, dy))


def score_robots(robots: list[Robot]) -> int:
    score: int = 0
    robot_positions: set[tuple[int, int]] = {(robot.x, robot.y) for robot in robots}
    for robot in robots:
        if (
            (robot.x + 1, robot.y - 1) in robot_positions
            or (robot.x + 1, robot.y + 1) in robot_positions
        ):
            score += 1

    return score

timestep: int = 0
best_score: int = 0
for _ in range(50_000):
    for robot in robots:
        robot.move()
    timestep += 1

    timestep_score: int = score_robots(robots)
    if timestep_score > best_score:
        best_score = timestep_score
        print_grid(robots)
        print(f"new best at {timestep}: {timestep_score}")
