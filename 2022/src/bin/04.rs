pub fn part_one(input: &str) -> Option<u32> {
    let mut res = 0;

    for line in input.lines() {
        let (first, second) = line.split_once(',').unwrap();
        let (fstart, fend) = first.split_once('-').unwrap();
        let (sstart, send) = second.split_once('-').unwrap();

        let fstart = fstart.parse::<u32>().unwrap();
        let fend = fend.parse::<u32>().unwrap();
        let sstart = sstart.parse::<u32>().unwrap();
        let send = send.parse::<u32>().unwrap();

        if fstart <= sstart && fend >= send {
            res += 1;
        } else if sstart <= fstart && send >= fend {
            res += 1;
        }
    }

    Some(res)
}

pub fn part_two(input: &str) -> Option<u32> {
    let mut res = 0;

    for line in input.lines() {
        let (first, second) = line.split_once(',').unwrap();
        let (fstart, fend) = first.split_once('-').unwrap();
        let (sstart, send) = second.split_once('-').unwrap();

        let fstart = fstart.parse::<u32>().unwrap();
        let fend = fend.parse::<u32>().unwrap();
        let sstart = sstart.parse::<u32>().unwrap();
        let send = send.parse::<u32>().unwrap();

        // if they overlap at all increase the result
        if sstart <= fend && fend <= send || fstart <= send && send <= fend {
            res += 1;
        }
    }

    Some(res)
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 4);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 4);
        assert_eq!(part_one(&input), None);
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 4);
        assert_eq!(part_two(&input), None);
    }
}
