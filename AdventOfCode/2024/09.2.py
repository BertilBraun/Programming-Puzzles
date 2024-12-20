from tqdm import trange


input = """2333133121414131402"""

disk_map = [(int(c), i // 2 if i % 2 == 0 else -1) for i, c in enumerate(input)]

# a dense format to represent the layout of files and free space on the disk. The digits alternate between indicating the length of a file and the length of free space.
# move file blocks one at a time from the end of the disk to the leftmost free space block (until there are no gaps remaining between file blocks)


new_disk_map = [val for val in disk_map]

for i in trange(len(disk_map) - 1, 0, -2):
    file_size, file_index = disk_map[i]
    for j in range(len(new_disk_map)):
        if new_disk_map[j][1] == file_index:
            break

        freespace_size, freespace_index = new_disk_map[j]

        if freespace_index != -1:
            continue

        if freespace_size >= file_size:
            new_disk_map[j] = (freespace_size - file_size, freespace_index)
            new_disk_map.insert(j, (file_size, file_index))
            new_disk_map.insert(j, (0, 0))

            for k in range(j + 3, len(new_disk_map)):
                if new_disk_map[k][1] != file_index:
                    continue

                new_disk_map[k] = (0, file_index)
                new_disk_map.insert(k + 1, (file_size, -1))
                break
            break

layed_out_disk = []
for i in range(len(new_disk_map)):
    for j in range(new_disk_map[i][0]):
        if new_disk_map[i][1] == -1:
            layed_out_disk.append(0)
        else:
            layed_out_disk.append(new_disk_map[i][1])


print('Final Sum:')
print(sum(val * i for i, val in enumerate(layed_out_disk)))
