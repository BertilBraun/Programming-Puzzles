jet_pattern = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""


# Define the rock shapes
rock_shapes = [
    [[1, 1, 1, 1]],  # Horizontal line
    [[0, 1, 0], [1, 1, 1], [0, 1, 0]],  # Plus shape
    [[1, 1, 1], [0, 0, 1], [0, 0, 1]],  # Reverse L shape
    [[1], [1], [1], [1]],  # Vertical line
    [[1, 1], [1, 1]],  # Square
]

chamber_width = 7
chamber = [[0] * chamber_width for _ in range(2022 * 5)]  # Initialize with sufficient height
chamber_height = 0  # Track the maximum height of the chamber
jet_index = 0


def can_move(rock, pos, delta):
    """Check if a rock can move in the given direction (delta)."""
    dx, dy = delta
    for i, row in enumerate(rock):
        for j, cell in enumerate(row):
            if cell:
                new_x, new_y = pos[0] + i + dx, pos[1] + j + dy
                if new_x < 0 or new_y < 0 or new_y >= chamber_width or chamber[new_x][new_y]:
                    return False
    return True


def place_rock(rock, pos):
    """Place a rock in the chamber."""
    for i, row in enumerate(rock):
        for j, cell in enumerate(row):
            if cell:
                chamber[pos[0] + i][pos[1] + j] = 1


for rock_num in range(2022):
    # Select the next rock and determine its initial position
    rock = rock_shapes[rock_num % len(rock_shapes)]
    rock_height = len(rock)
    rock_width = len(rock[0])
    start_x = chamber_height + 3
    start_y = 2
    pos = (start_x, start_y)

    while True:
        # Apply jet push
        jet_direction = 1 if jet_pattern[jet_index] == '>' else -1
        jet_index = (jet_index + 1) % len(jet_pattern)
        if can_move(rock, pos, (0, jet_direction)):
            pos = (pos[0], pos[1] + jet_direction)

        # Move down
        if can_move(rock, pos, (-1, 0)):
            pos = (pos[0] - 1, pos[1])
        else:
            # Place the rock and update chamber height
            place_rock(rock, pos)
            chamber_height = max(chamber_height, pos[0] + rock_height)
            break

# print the last 10 rows of the chamber
for row in chamber[:20][::-1]:
    print(''.join('#' if cell else '.' for cell in row))

print(chamber_height)
