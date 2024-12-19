pub fn part_one(input: &str) -> Option<u32> {
    let (grid, start, end) = parse_grid(input);

    return bfs(start, end, grid);
}

fn parse_grid(input: &str) -> (Vec<Vec<i32>>, (i32, i32), (i32, i32)) {
    let mut start: (i32, i32) = (0, 0);
    let mut end: (i32, i32) = (0, 0);

    for (i, line) in input.lines().enumerate() {
        for (j, c) in line.chars().enumerate() {
            if c == 'S' {
                start = (j as i32, i as i32);
            }
            if c == 'E' {
                end = (j as i32, i as i32);
            }
        }
    }

    let mut input = input.to_string();
    input = input.replace('S', "a");
    input = input.replace('E', "z");

    let lines = input.lines().collect::<Vec<_>>();

    let n = lines.len();
    let m = lines[0].len();

    let mut grid = vec![vec![0 as i32; m]; n];

    for (y, line) in lines.iter().enumerate() {
        for (x, c) in line.chars().enumerate() {
            grid[y][x] = c as i32 - 'a' as i32;
        }
    }

    (grid, start, end)
}

fn bfs(start: (i32, i32), end: (i32, i32), grid: Vec<Vec<i32>>) -> Option<u32> {
    let mut queue = std::collections::VecDeque::new();
    queue.push_back((start, 0));

    let mut visited = std::collections::HashSet::new();
    visited.insert(start);

    let n = grid.len() as i32;
    let m = grid[0].len() as i32;

    while let Some(((x, y), steps)) = queue.pop_front() {
        if (x, y) == end {
            return Some(steps);
        }

        for (nx, ny) in vec![(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)] {
            if nx < 0 || nx >= m || ny < 0 || ny >= n as i32 {
                continue;
            }
            if visited.contains(&(nx, ny)) {
                continue;
            }
            if grid[ny as usize][nx as usize] - grid[y as usize][x as usize] > 1 {
                continue;
            }
            visited.insert((nx, ny));
            queue.push_back(((nx, ny), steps + 1));
        }
    }

    None
}

pub fn part_two(input: &str) -> Option<u32> {
    let (grid, _, end) = parse_grid(input);

    let mut minimum = 100000000;

    for (i, row) in grid.iter().enumerate() {
        for (j, v) in row.iter().enumerate() {
            if v.eq(&0) {
                if let Some(v) = bfs((j as i32, i as i32), end, grid.clone()) {
                    minimum = minimum.min(v);
                }
            }
        }
    }

    Some(minimum)
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 12);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 12);
        assert_eq!(part_one(&input), None);
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 12);
        assert_eq!(part_two(&input), None);
    }
}
