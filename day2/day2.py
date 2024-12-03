with open("input") as f:
    lines: list[str] = [line.strip() for line in f.readlines()]

def abs(x: int) -> int:
    return x if x >= 0 else x*-1

def check_safe(line: list[int]) -> bool:
    direction: str = "increasing" if line[1] > line[0] else "decreasing"
    for l, r in zip(line[:-1], line[1:]):
        diff = abs(l - r)
        if l > r and direction == "increasing":
            return False
        if l < r and direction == "decreasing": 
            return False
        if not (1 <= diff <= 3):
            return False
    return True

def check_safe_tolerant(line: list[int], is_sublist: bool = False) -> bool:
    direction: str = "increasing" if line[1] > line[0] else "decreasing"
    is_safe: bool = True
    for l, r in zip(line[:-1], line[1:]):
        diff = abs(l - r)
        if l > r and direction == "increasing":
            is_safe = False
        if l < r and direction == "decreasing": 
            is_safe = False
        if not (1 <= diff <= 3):
            is_safe = False

    if is_safe:
        return True
    else:
        for i in range(len(line)):
            sublist = line.copy()
            _  = sublist.pop(i)
            if check_safe(sublist):
                return True
    return False

print(sum(int(check_safe([int(x) for x in line.split(" ")])) for line in lines))
print(
    sum(
        int(
            all((-3 <= (l - r) <= -1) or (1 <= (l - r) <= 3) for l, r in zip([int(x) for x in line.split(" ")][:-1], [int(x) for x in line.split(" ")][1:]))
            and
            (
                all(
                    l < r for l, r in zip(
                        [int(x) for x in line.split(" ")][:-1],
                        [int(x) for x in line.split(" ")][1:]
                    )
                )
                or
                all(
                    r < l for l, r in zip(
                        [int(x) for x in line.split(" ")][:-1],
                        [int(x) for x in line.split(" ")][1:]
                    )
                )
            )
        )
        for line in open("input").readlines()
    )
)
print(sum(int(check_safe_tolerant([int(x) for x in line.split(" ")])) for line in lines))
