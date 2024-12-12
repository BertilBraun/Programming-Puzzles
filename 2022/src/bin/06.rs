use std::collections::HashMap;

fn find_marker_of_length(input: &str, length: usize) -> Option<u32> {
    let mut chars: HashMap<char, u32> = HashMap::new();
    for i in 0..length {
        *chars.entry(input.chars().nth(i).unwrap()).or_insert(0) += 1;
    }
    for i in length..input.len() {
        let c = input.chars().nth(i).unwrap();
        *chars.entry(c).or_insert(0) += 1;
        let c = input.chars().nth(i - length).unwrap();
        *chars.entry(c).or_insert(0) -= 1;

        if chars.values().all(|&v| v == 1 || v == 0) {
            return Some(i as u32 + 1);
        }
    }
    Some(input.len() as u32)
}

pub fn part_one(input: &str) -> Option<u32> {
    find_marker_of_length(input, 4)
}

pub fn part_two(input: &str) -> Option<u32> {
    find_marker_of_length(input, 14)
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 6);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 6);
        assert_eq!(part_one(&input), None);
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 6);
        assert_eq!(part_two(&input), None);
    }
}
