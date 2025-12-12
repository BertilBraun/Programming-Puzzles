from aoc import *
from util import *
import z3

# Global knobs to bias Z3 toward native SAT cardinality/PB reasoning (avoid PB -> many equations).
# Safe for this script-style usage.
z3.set_param('sat.cardinality.solver', True)
z3.set_param('sat.pb.solver', True)


def solve1_old(input: str) -> str | int | None:
    elements = input.split('\n\n')
    shapes = []
    for element in elements[:-1]:
        shape = []
        for line in element.splitlines()[1:]:
            shape.append([c == '#' for c in line])
        shapes.append(shape)

    def rotate_shape(shape: list[list[bool]]) -> list[list[bool]]:
        # rotate the shape 90 degrees clockwise
        return [list(row) for row in zip(*shape[::-1])]

    def all_rotations(shape_index: int) -> list[list[list[bool]]]:
        shape = shapes[shape_index]
        rotations = [shape]
        for _ in range(3):
            shape = rotate_shape(shape)
            rotations.append(shape)
        return rotations

    def _shape_to_cells(shape: list[list[bool]]) -> set[tuple[int, int]]:
        cells: set[tuple[int, int]] = set()
        for y, row in enumerate(shape):
            for x, v in enumerate(row):
                if v:
                    cells.add((x, y))
        return cells

    def _cells_key(cells: set[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
        # No normalization needed if shapes are always 3x3 anchored at (0,0),
        # but sorting gives a stable, comparable key (also dedupes symmetric rotations).
        return tuple(sorted(cells))

    shape_rotations: list[list[tuple[tuple[int, int], ...]]] = []
    shape_sizes: list[int] = []
    for i in range(len(shapes)):
        rots: list[tuple[tuple[int, int], ...]] = []
        seen: set[tuple[tuple[int, int], ...]] = set()
        for rot in all_rotations(i):
            cells = _shape_to_cells(rot)
            key = _cells_key(cells)
            if not key:
                continue
            if key in seen:
                continue
            seen.add(key)
            rots.append(key)
        shape_rotations.append(rots)
        shape_sizes.append(len(rots[0]) if rots else 0)

    areas = []
    for line in elements[-1].splitlines():
        # 47x48: 59 59 54 61 53 61
        width, height = map(int, line.split(':')[0].split('x'))
        counts = list(map(int, line.split(':')[1].split()))
        areas.append((width, height, counts))

    def does_area_fit_all_shapes(area: tuple[int, int, list[int]]) -> bool:
        width, height, counts = area

        # we need to fit counts[i] shapes of type shapes[i] into the area for all i simultaneously
        # shapes can be moved and rotated and may never overlap

        # ---- Z3 model: Bool var per possible placement; per-shape exact count; per-cell non-overlap ----
        solver = z3.Solver()

        # cell index -> [BoolVar, ...] for cardinality constraints
        cell_vars: list[list[z3.BoolRef]] = [[] for _ in range(width * height)]

        # For each shape type, create placement vars and constrain exactly 'count' of them
        for shape_i, rots in enumerate(shape_rotations):
            placement_vars: list[z3.BoolRef] = []
            for rot_i, cells in enumerate(rots):
                max_dx = max(dx for dx, _ in cells)
                max_dy = max(dy for _, dy in cells)
                max_x0 = width - (max_dx + 1)
                max_y0 = height - (max_dy + 1)

                for y0 in range(max_y0 + 1):
                    for x0 in range(max_x0 + 1):
                        v = z3.Bool(f'p_s{shape_i}_r{rot_i}_x{x0}_y{y0}')
                        placement_vars.append(v)
                        # add this placement to each covered cell's term list
                        for dx, dy in cells:
                            x = x0 + dx
                            y = y0 + dy
                            idx = y * width + x
                            cell_vars[idx].append(v)

            # Must choose exactly counts[shape_i] placements for this shape type
            k = counts[shape_i]
            if k == 0:
                continue

            # Count chosen placements for this shape type (native cardinality).
            solver.add(z3.Sum(*[z3.If(v, 1, 0) for v in placement_vars]) == k)

        # Per-cell non-overlap always; if exact cover, require every cell covered.
        for vars_for_cell in cell_vars:
            if not vars_for_cell:
                continue
            solver.add(z3.Sum(*[z3.If(v, 1, 0) for v in vars_for_cell]) <= 1)

        result = solver.check()
        print('Z3 stats:', solver.statistics())
        return result == z3.sat

    return sum(1 for area in areas if does_area_fit_all_shapes(area))


def solve1(input: str) -> str | int | None:
    elements = input.split('\n\n')
    shapes_sizes: list[int] = []
    for element in elements[:-1]:
        shape_size = sum(sum(c == '#' for c in line) for line in element.splitlines()[1:])
        shapes_sizes.append(shape_size)

    areas = []
    for line in elements[-1].splitlines():
        # 47x48: 59 59 54 61 53 61
        width, height = map(int, line.split(':')[0].split('x'))
        counts = list(map(int, line.split(':')[1].split()))
        areas.append((width, height, counts))

    def does_area_fit(width: int, height: int, counts: list[int]) -> bool:
        total_size = sum(counts[i] * shapes_sizes[i] for i in range(len(counts)))
        return total_size <= width * height

    return sum(1 for width, height, counts in areas if does_area_fit(width, height, counts))


if __name__ == '__main__':
    aoc(day=12, part=1, solve1=solve1, example=False)
