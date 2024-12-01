def part1():
    with open("input_1") as f:
        lines: list[tuple[str, ...]] = [line.strip().split(" ") for line in f.readlines()]

    lists: list[tuple[int, int]] = [(int(l[0]), int(l[-1])) for l in lines]
    list_l, list_r = zip(*lists)

    total = 0
    for l, r in zip(sorted(list_l), sorted(list_r)):
        total += (l - r) * (-1 if l < r else 1)

    return total

def p1_golfed():
    return (sum(l - r if l > r else r - l for l, r in zip(sorted(int(l.split(" ")[0]) for l in open("input_1").readlines()), sorted(int(l.split(" ")[-1]) for l in open("input_1").readlines()))))

def part2():
    with open("input_1") as f:
        lines: list[tuple[str, ...]] = [line.strip().split(" ") for line in f.readlines()]

    lists: list[tuple[int, int]] = [(int(l[0]), int(l[-1])) for l in lines]
    list_l, list_r = zip(*lists)

    total = 0
    for l in list_l:
        diff = list_r.count(l) * l
        total += diff

    return total

def p2_golfed() -> int:
    return sum([int(line.split(" ")[-1]) for line in open("input_1").readlines()].count(l) * l for l in [int(line.split(" ")[0]) for line in open("input_1").readlines()])


print(part1())
print(p1_golfed())
print(part2())
print(p2_golfed())
