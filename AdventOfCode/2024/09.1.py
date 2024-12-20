from tqdm import trange


input = """2333133121414131402"""

disk_map = [(int(c), i // 2 if i % 2 == 0 else -1) for i, c in enumerate(input)]

# a dense format to represent the layout of files and free space on the disk. The digits alternate between indicating the length of a file and the length of free space.
# move file blocks one at a time from the end of the disk to the leftmost free space block (until there are no gaps remaining between file blocks)

disk = []
for i, (size, index) in enumerate(disk_map):
    if i % 2 == 0:
        for _ in range(size):
            disk.append(index)
    else:
        for _ in range(size):
            disk.append(-1)


for i in trange(len(disk) - 1, 0, -1):
    if disk[i] != -1:
        for j in range(0, i):
            if disk[j] == -1:
                disk[j], disk[i] = disk[i], disk[j]
                break


print(disk)
print('Final Sum:')
print(sum(val * i for i, val in enumerate(disk)))
