with open("input") as f:
    disk: str = f.read().strip()

def part1() -> None:
    def create_disk_pattern(disk: str) -> list[str]:
        pattern: list[str | int] = []
        for i in range(len(disk)):
            if i % 2 == 0:
                # append file with ID
                pattern.extend([i//2] * int(disk[i]))
            else:
                # append free space
                pattern.extend(["."] * int(disk[i]))
        return pattern

    pattern: list[str] = create_disk_pattern(disk)

    left: int = 0
    right: int = len(pattern) - 1

    while pattern[left] != ".":
        left += 1

    while pattern[right] == ".":
        right -= 1

    while left < right:
        if pattern[left] != ".":
            left += 1
        elif pattern[right] == ".":
            right -= 1
        else:
            # left is free, right is num
            pattern[left] = pattern[right]
            pattern[right] = "."

    total: int = 0
    for i, num in enumerate(pattern):
        if num != ".":
            total += i * int(num)
    print(total)


part1()


def part2() -> None:
    def get_file_ids_and_sizes(disk: str) -> list[tuple[int, int]]:
        return [((i//2 if i%2 == 0 else "."), int(disk[i])) for i in range(len(disk))]

    file_ids_and_sizes: list[tuple[int, int]] = get_file_ids_and_sizes(disk)

    def tuples_to_pattern(tuples: list[tuple[int, int]]) -> list[int | str]:
        pattern: list[int | str] = []
        for file_id, size in tuples:
            if size != 0:
                pattern.extend([file_id] * size)
        return pattern

    rev_file_ids_and_sizes = file_ids_and_sizes.copy()[::-1]
    for file_id, size in rev_file_ids_and_sizes:
        if file_id == ".":
            continue
        skip_rest: bool = False
        for left in range(len(file_ids_and_sizes)):
            lfile_id, lsize = file_ids_and_sizes[left]

            if lfile_id == file_id:
                skip_rest = True
                break

            if lfile_id != ".":
                continue

            if lsize >= size:
                file_ids_and_sizes[left] = (file_id, size)
                if lsize - size > 0:
                    file_ids_and_sizes.insert(left + 1, (".", lsize - size))

                # replace the old file's position with dots
                for i in range(len(file_ids_and_sizes) - 1, 0, -1):
                    if file_ids_and_sizes[i][0] == file_id:
                        new_size = size
                        if (i + 1 < len(file_ids_and_sizes)) and file_ids_and_sizes[i + 1][0] == ".":
                            new_size += file_ids_and_sizes[i + 1][1]
                            _ = file_ids_and_sizes.pop(i + 1)
                        if file_ids_and_sizes[i - 1][0] == ".":
                            file_ids_and_sizes[i - 1] = (".", new_size + file_ids_and_sizes[i - 1][1])
                            _ = file_ids_and_sizes.pop(i)
                            break
                        else:
                            file_ids_and_sizes[i] = (".", new_size)
                            break
                skip_rest = True
                break

        if skip_rest: 
            continue

    total: int = 0
    for i, num in enumerate(tuples_to_pattern(file_ids_and_sizes)):
        if num != ".":
            total += i * int(num)
    print(total)

part2()
