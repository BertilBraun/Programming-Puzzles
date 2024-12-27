def simulate_large_rock_count(jet_pattern, total_rocks):
    rock_shapes = [
        [[1, 1, 1, 1]],  # Horizontal line
        [[0, 1, 0], [1, 1, 1], [0, 1, 0]],  # Plus shape
        [[1, 1, 1], [0, 0, 1], [0, 0, 1]],  # Corrected Reverse L shape
        [[1], [1], [1], [1]],  # Vertical line
        [[1, 1], [1, 1]],  # Square
    ]

    chamber_width = 7
    jet_length = len(jet_pattern)
    chamber = [[0] * chamber_width for _ in range(10000)]  # Sufficient height
    chamber_height = 0
    jet_index = 0

    seen_states = {}

    def can_move(rock, pos, delta):
        dx, dy = delta
        for i, row in enumerate(rock):
            for j, cell in enumerate(row):
                if cell:
                    new_x, new_y = pos[0] + i + dx, pos[1] + j + dy
                    if new_x < 0 or new_y < 0 or new_y >= chamber_width or chamber[new_x][new_y]:
                        return False
        return True

    def place_rock(rock, pos):
        for i, row in enumerate(rock):
            for j, cell in enumerate(row):
                if cell:
                    chamber[pos[0] + i][pos[1] + j] = 1

    def simulate_rock(rock_num, chamber_height, jet_index):
        rock = rock_shapes[rock_num % len(rock_shapes)]
        pos = (chamber_height + 3, 2)

        while True:
            jet_direction = 1 if jet_pattern[jet_index] == '>' else -1
            jet_index = (jet_index + 1) % jet_length
            if can_move(rock, pos, (0, jet_direction)):
                pos = (pos[0], pos[1] + jet_direction)
            if can_move(rock, pos, (-1, 0)):
                pos = (pos[0] - 1, pos[1])
            else:
                place_rock(rock, pos)
                chamber_height = max(chamber_height, pos[0] + len(rock))
                break

        return chamber_height, jet_index

    t = 0
    added = 0
    while t < total_rocks:
        chamber_height, jet_index = simulate_rock(t, chamber_height, jet_index)

        state_key = (
            t % len(rock_shapes),
            jet_index,
            tuple(tuple(row) for row in chamber[chamber_height - 50 : chamber_height]),
        )
        if state_key in seen_states:
            old_t, old_y = seen_states[state_key]
            dt = t - old_t
            dy = chamber_height - old_y

            full_cycles = (total_rocks - t) // dt
            t += full_cycles * dt
            added += full_cycles * dy

            assert t < total_rocks

        seen_states[state_key] = (t, chamber_height)
        t += 1

    return chamber_height + added


# Input
jet_pattern = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
total_rocks = 1000000000000

# Calculate the height of the tower
tower_height = simulate_large_rock_count(jet_pattern, total_rocks)
print(f'The height of the tower after {total_rocks} rocks is: {tower_height}')
