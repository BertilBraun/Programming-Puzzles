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

    for rock_num in range(total_rocks):
        chamber_height, jet_index = simulate_rock(rock_num, chamber_height, jet_index)

        state_key = (
            rock_num % len(rock_shapes),
            jet_index,
            tuple(tuple(row) for row in chamber[chamber_height - 4 : chamber_height]),
        )
        if state_key in seen_states:
            prev_rock_num, prev_height = seen_states[state_key]
            cycle_length = rock_num - prev_rock_num
            prev_rock_num += 1
            cycle_height = chamber_height - prev_height

            full_cycles = (total_rocks - prev_rock_num) // cycle_length
            remaining_rocks = (total_rocks - prev_rock_num) % cycle_length
            total_height = prev_height + full_cycles * cycle_height

            print(
                f'Cycle length: {cycle_length}, Cycle height: {cycle_height}, Full cycles: {full_cycles}, Remaining rocks: {remaining_rocks}, Total height: {total_height} Previous height: {prev_height}, Current height: {chamber_height}, Previous rock: {prev_rock_num % len(rock_shapes)}'
            )

            prev_chamber_height = chamber_height

            for r in range(remaining_rocks):
                chamber_height, jet_index = simulate_rock(prev_rock_num + r, chamber_height, jet_index)

            chamber_growth = chamber_height - prev_chamber_height
            print(
                f'Current height: {chamber_height}, Previous height: {prev_chamber_height}, Growth: {chamber_growth}, Total height: {total_height + chamber_growth}'
            )
            return total_height + chamber_growth
        seen_states[state_key] = (rock_num, chamber_height)

    return chamber_height


# Input
jet_pattern = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
total_rocks = 1000000000000

# Calculate the height of the tower
tower_height = simulate_large_rock_count(jet_pattern, total_rocks)
assert tower_height < 1590724637676
print(f'The height of the tower after {total_rocks} rocks is: {tower_height}')
