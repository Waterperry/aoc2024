print(
    sum(
        int(match.group(1)) * int(match.group(2))
        for line in open("input").readlines()
        for match in __import__("re").finditer(r"mul\(([0-9]*),([0-9]*)\)", line)
    )
)

print(
    sum(
        int(match.group(1)) * int(match.group(2))
        for match in __import__("re").finditer(
            r"mul\(([0-9]*),([0-9]*)\)",
            __import__("re").sub(r"don't\(\).*?(do\(\)|$)", "|||", "".join(line.strip() for line in open("input").readlines())),
        )
    )
)  # 80570939
