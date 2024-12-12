pub fn part_one(input: &str) -> Option<u32> {
    let lines = input
        .lines()
        .map(|line| line.parse::<u32>().ok())
        .collect::<Vec<_>>();

    let groups = lines
        .split(|line| line.is_none())
        .map(|group| group.iter().map(|line| line.unwrap()).sum::<u32>());

    groups.max()
}

pub fn part_two(input: &str) -> Option<u32> {
    let lines = input
        .lines()
        .map(|line| line.parse::<u32>().ok())
        .collect::<Vec<_>>();

    let mut groups = lines
        .split(|line| line.is_none())
        .map(|group| group.iter().map(|line| line.unwrap()).sum::<u32>())
        .collect::<Vec<_>>();

    groups.sort();
    groups.reverse();

    Some(groups[0..3].iter().sum::<u32>())
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 1);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 1);
        assert_eq!(part_one(&input), None);
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 1);
        assert_eq!(part_two(&input), None);
    }
}
