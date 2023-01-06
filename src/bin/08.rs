fn read_grid(input: &str) -> Vec<Vec<u32>> {
    input
        .lines()
        .map(|line| {
            line.chars()
                .map(|s| s.to_string().parse().unwrap())
                .collect::<Vec<u32>>()
        })
        .collect::<Vec<Vec<u32>>>()
}

pub fn part_one(input: &str) -> Option<u32> {
    let grid = read_grid(input);
    let mut seen: Vec<Vec<bool>> = vec![vec![false; grid.len()]; grid.len()];

    let mut visible = 4 * grid.len() as u32 - 4;
    for i in 0..grid.len() {
        seen[i][0] = true;
        seen[i][grid.len() - 1] = true;
        seen[0][i] = true;
        seen[grid.len() - 1][i] = true;
    }

    // linear search from each direction, increase visible count if not seen if all previous are lower

    // left
    for i in 0..grid.len() {
        let mut max = 0;
        for j in 0..grid.len() {
            if grid[i][j] > max {
                max = grid[i][j];
                if !seen[i][j] {
                    visible += 1;
                    seen[i][j] = true;
                }
            }
        }
    }

    // right
    for i in 0..grid.len() {
        let mut max = 0;
        for j in (0..grid.len()).rev() {
            if grid[i][j] > max {
                max = grid[i][j];
                if !seen[i][j] {
                    visible += 1;
                    seen[i][j] = true;
                }
            }
        }
    }

    // up
    for i in 0..grid.len() {
        let mut max = 0;
        for j in 0..grid.len() {
            if grid[j][i] > max {
                max = grid[j][i];
                if !seen[j][i] {
                    visible += 1;
                    seen[j][i] = true;
                }
            }
        }
    }

    // down
    for i in 0..grid.len() {
        let mut max = 0;
        for j in (0..grid.len()).rev() {
            if grid[j][i] > max {
                max = grid[j][i];
                if !seen[j][i] {
                    visible += 1;
                    seen[j][i] = true;
                }
            }
        }
    }

    Some(visible)
}

pub fn part_two(input: &str) -> Option<u32> {
    let grid = read_grid(input);

    let mut max_view_distance = 0;

    let mut scores: Vec<Vec<Vec<u32>>> = vec![vec![vec![0; 5]; grid.len()]; grid.len()];

    for i in 0..grid.len() {
        for j in 0..grid.len() {
            let mut view_distance = 1;

            // left
            let mut max_distance1 = 0;
            for k in (0..j).rev() {
                max_distance1 += 1;
                if grid[i][k] >= grid[i][j] {
                    break;
                }
            }
            view_distance *= max_distance1;

            // right
            let mut max_distance2 = 0;
            for k in j + 1..grid.len() {
                max_distance2 += 1;
                if grid[i][k] >= grid[i][j] {
                    break;
                }
            }
            view_distance *= max_distance2;

            // up
            let mut max_distance3 = 0;
            for k in (0..i).rev() {
                max_distance3 += 1;
                if grid[k][j] >= grid[i][j] {
                    break;
                }
            }
            view_distance *= max_distance3;

            // down
            let mut max_distance4 = 0;
            for k in i + 1..grid.len() {
                max_distance4 += 1;
                if grid[k][j] >= grid[i][j] {
                    break;
                }
            }
            view_distance *= max_distance4;

            scores[i][j] = vec![
                view_distance,
                max_distance1,
                max_distance2,
                max_distance3,
                max_distance4,
            ];

            max_view_distance = max_view_distance.max(view_distance);
        }
    }

    for row in scores.iter() {
        for col in row.iter() {
            print!("{:?}", col);
        }
        println!();
    }

    Some(max_view_distance)
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 8);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 8);
        assert_eq!(part_one(&input), None);
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 8);
        assert_eq!(part_two(&input), None);
    }
}
