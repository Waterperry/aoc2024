# one liners
with open("input") as f: print(sum(target for target, nums in [(int(line.split(":")[0]), [int(x) for x in line.split(":")[1].split(" ") if len(x) > 0]) for line in f.readlines()] if any((lambda target,num,nums,ops: target == [(num:=op(num, right)) for op, right in zip(ops, nums[1:])][-1])(target, nums[0], nums.copy(), list(op)) for op in list(__import__("itertools").product([lambda x,y: x+y, lambda x,y: x*y], repeat=len(nums) - 1)))))
with open("input") as f: print(sum(target for target, nums in [(int(line.split(":")[0]), [int(x) for x in line.split(":")[1].split(" ") if len(x) > 0]) for line in f.readlines()] if any((lambda target,num,nums,ops: target == [(num:=op(num, right)) for op, right in zip(ops, nums[1:])][-1])(target, nums[0], nums.copy(), list(op)) for op in list(__import__("itertools").product([lambda x,y: x+y, lambda x,y: x*y, lambda x,y: int(f"{x}{y}")], repeat=len(nums) - 1)))))

# actual solution

from itertools import product
from typing import Callable

with open("input") as f:
    lines: list[str] = [line.strip() for line in f.readlines()]

targets_and_numbers: list[tuple[int, list[int]]] = [
    (int(line.split(":")[0]), [int(x) for x in line.split(":")[1].split(" ") if len(x) > 0])
    for line in lines
]


def apply_ops(target: int, nums: list[int], ops: list[Callable]) -> bool:
    nums = nums.copy()
    l = nums.pop(0)

    while ops:
        if l > target:
            return False
        op = ops.pop(0)
        r = nums.pop(0)
        l = op(l, r)

    return l == target

add = lambda x, y: x + y
mul = lambda x, y: x * y
concat = lambda x, y: int(str(x) + str(y))

possible = 0
for target, nums in targets_and_numbers:
    all_ops = list(product([add, mul], repeat=len(nums)-1))
    for op in all_ops:
        if apply_ops(target, nums, list(op)):
            possible += target
            break

print(possible)

possible = 0
for target, nums in targets_and_numbers:
    all_ops: list[list[Callable]] = list(product([add, mul, concat], repeat=len(nums)-1))
    for op in all_ops:
        if apply_ops(target, nums, list(op)):
            possible += target
            break

print(possible)
