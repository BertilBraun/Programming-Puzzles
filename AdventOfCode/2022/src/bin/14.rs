fn parse_grid(input: &str) -> Vec<Vec<bool>> {
    let mut grid = vec![vec![false; 200]; 1000];

    for line in input.lines() {
        let parts = line
            .split(" -> ")
            .map(|s| {
                s.split(',')
                    .map(|s| s.parse::<u32>().unwrap())
                    .collect::<Vec<_>>()
            })
            .collect::<Vec<_>>();

        for i in 1..parts.len() {
            let (lx, ly) = (parts[i - 1][0], parts[i - 1][1]);
            let (rx, ry) = (parts[i][0], parts[i][1]);

            if lx != rx && ly != ry {
                panic!("Invalid input");
            }

            if lx == rx {
                for y in ly.min(ry)..=ly.max(ry) {
                    grid[lx as usize][y as usize] = true;
                }
            } else {
                for x in lx.min(rx)..=lx.max(rx) {
                    grid[x as usize][ly as usize] = true;
                }
            }
        }
    }

    grid
}

fn simulate_one(grid: &mut Vec<Vec<bool>>) -> (i32, i32) {
    let mut pos: (i32, i32) = (500, 0);

    while pos.1 < 200 {
        if force_down_one(&mut pos, grid) {
            return pos;
        }
    }
    pos
}

fn force_down_one(pos: &mut (i32, i32), grid: &mut Vec<Vec<bool>>) -> bool {
    grid[pos.0 as usize][pos.1 as usize] = false;

    for (off_x, off_y) in &[(0, 1), (-1, 1), (1, 1)] {
        let (x, y) = (pos.0 + off_x, pos.1 + off_y);

        if x < 0 || y < 0 || x >= 1000 || y >= 200 {
            continue;
        }

        if !grid[x as usize][y as usize] {
            grid[x as usize][y as usize] = true;
            *pos = (x, y);
            return false;
        }
    }

    grid[pos.0 as usize][pos.1 as usize] = true;
    true
}

fn find_max_y(grid: &Vec<Vec<bool>>) -> usize {
    let mut max_y = 0;
    for row in grid {
        for (i, &cell) in row.iter().enumerate() {
            if cell {
                max_y = max_y.max(i);
            }
        }
    }
    max_y
}

pub fn part_one(input: &str) -> Option<u32> {
    let mut grid = parse_grid(input);

    for i in 0..100000 {
        if simulate_one(&mut grid).1 == 199 {
            return Some(i);
        }
    }

    None
}

pub fn part_two(input: &str) -> Option<u32> {
    let mut grid = parse_grid(input);

    let max_y = find_max_y(&grid);

    println!("max_y: {}", max_y);

    for x in 0..1000 {
        grid[x][max_y + 2] = true;
    }

    for i in 0..100000000 {
        if simulate_one(&mut grid) == (500, 0) {
            return Some(i + 1);
        }
    }

    None
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 14);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 14);
        assert_eq!(part_one(&input), None);
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 14);
        assert_eq!(part_two(&input), None);
    }
}
