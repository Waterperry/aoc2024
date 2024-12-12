from collections import defaultdict

with open("input") as f:
    stones: list[int] = [int(x) for x in f.read().strip().split(" ")]

def blink(i: int) -> list[int]:
    if i == 0:
        return [1]
    elif len(str(i)) % 2 == 0:
        s = str(i)
        halves = s[:len(s)//2], s[len(s)//2:]
        return [int(h) for h in halves]
    else:
        return [i * 2024]

p1_stones = stones.copy()
for _ in range(25):
    new_stones = [x for stone in p1_stones for x in blink(stone)]
    p1_stones = new_stones
print(len(p1_stones))

stone_counts = defaultdict(int) | {stone: 1 for stone in stones}

for _ in range(75):
    new_stone_counts = defaultdict(int)
    for stone, count in stone_counts.items():
        for new_stone in blink(stone):
            new_stone_counts[new_stone] += count
    stone_counts = new_stone_counts
print(sum(stone_counts.values()))
