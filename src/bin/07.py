

from dataclasses import dataclass
from functools import cache


@dataclass
class dir:
    name: str
    size: int
    children: dict[str, dir]

    @property
    def total_size(self):
        return self.size + sum(child.total_size for child in self.children.values())


def sum_size_if_less_than(dir, size):
    s = dir.total_size if dir.total_size < size else 0

    for child in dir.children.values():
        s += sum_size_if_less_than(child, size)

    return s


def min_size_greater_than(dir, size):
    m = dir.total_size if dir.total_size >= size else 100000000000

    for child in dir.children.values():
        m = min(m, min_size_greater_than(child, size))

    return m


with open("../inputs/07.txt") as f:
    input = f.read().splitlines()

    root = dir("/", 0, {})
    stack = [root]

    while input:
        line = input.pop(0)
        if line == "$ cd /":
            stack = [root]
        elif line == "$ cd ..":
            stack.pop(-1)
        elif line.startswith("$ cd "):
            name = line.replace("$ cd ", "")
            if name not in stack[-1].children:
                stack[-1].children[name] = dir(name, 0, {})
            stack.append(stack[-1].children[name])
        elif line == "$ ls":
            while input and input[0][0] != "$":
                line = input.pop(0)
                if line.startswith("dir"):
                    continue
                (size, _) = line.split()
                stack[-1].size += int(size)

    print(sum_size_if_less_than(root, 100000))
    print(min_size_greater_than(root, 30000000 - (70000000 - root.total_size)))
