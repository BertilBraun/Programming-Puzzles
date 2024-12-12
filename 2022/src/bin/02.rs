pub fn part_one(input: &str) -> Option<u32> {
    let game = input
        .lines()
        .map(|line| line.split(' ').collect::<Vec<_>>());

    let mut score = 0;

    for line in game {
        let a = line[0];
        let b = line[1];

        if b == "X" {
            score += 1;
            if a == "A" {
                score += 3;
            }
            if a == "B" {
                score += 0;
            }
            if a == "C" {
                score += 6;
            }
        }
        if b == "Y" {
            score += 2;
            if a == "A" {
                score += 6;
            }
            if a == "B" {
                score += 3;
            }
            if a == "C" {
                score += 0;
            }
        }
        if b == "Z" {
            score += 3;
            if a == "A" {
                score += 0;
            }
            if a == "B" {
                score += 6;
            }
            if a == "C" {
                score += 3;
            }
        }
    }

    Some(score)
}

pub fn part_two(input: &str) -> Option<u32> {
    let game = input
        .lines()
        .map(|line| line.split(' ').collect::<Vec<_>>());

    let mut score = 0;

    for line in game {
        let a = line[0];
        let b = line[1];

        if b == "X" {
            score += 0;
            if a == "A" {
                score += 3;
            }
            if a == "B" {
                score += 1;
            }
            if a == "C" {
                score += 2;
            }
        }
        if b == "Y" {
            score += 3;
            if a == "A" {
                score += 1;
            }
            if a == "B" {
                score += 2;
            }
            if a == "C" {
                score += 3;
            }
        }
        if b == "Z" {
            score += 6;
            if a == "A" {
                score += 2;
            }
            if a == "B" {
                score += 3;
            }
            if a == "C" {
                score += 1;
            }
        }
    }

    Some(score)
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 2);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 2);
        assert_eq!(part_one(&input), None);
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 2);
        assert_eq!(part_two(&input), None);
    }
}
