from collections import defaultdict

with open("input") as f:
    lines: list[str] = [line.strip() for line in f.readlines()]

lines = [line for line in lines if len(line) > 0]

rule_lines: list[str] = [line for line in lines if "|" in line]
order_lines: list[list[int]] = [[int(x) for x in line.split(",")] for line in lines if "," in line]

must_come_after: dict[int, set[int]] = defaultdict(set)

for rule in rule_lines:
    l, r = rule.split("|")
    l, r = int(l), int(r)
    must_come_after[r].add(l)

def is_good_line(line: list[int]) -> bool:
    for i in range(len(line) - 1):
        following = line[i+1:]
        if any(f in must_come_after[line[i]] for f in following):
            return False
    return True


def part1() -> None:
    good_rules_page_sum: int = 0
    for ordering in order_lines:
        if is_good_line(ordering):
            good_rules_page_sum += ordering[len(ordering)//2]

    print(good_rules_page_sum)  # 7074
part1()


def reorder_line(line: list[int]) -> list[int]:
    new_line: list[int] = []
    working: list[int] = line.copy()
    while len(new_line) < len(line):
        for value in working:
            other = set(working).difference({value})
            if not any(x in must_come_after[value] for x in other):
                new_line.append(value)
                working.remove(value)
                break
        else:
            raise ValueError(f"Can't sort line: {line} ({working=})")
    return new_line


good_rules_page_sum: int = 0
for line in order_lines:
    if not is_good_line(line):
        reordered = reorder_line(line)
        good_rules_page_sum += reordered[len(reordered)//2]
print(good_rules_page_sum)
