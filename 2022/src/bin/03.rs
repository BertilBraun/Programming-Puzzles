fn count(input: &str) -> Vec<u32> {
    let mut counts = vec![0; 52];
    for c in input.chars() {
        if c <= 'Z' && c >= 'A' {
            counts[c as usize - 'A' as usize + 26] += 1;
        } else {
            counts[c as usize - 'a' as usize] += 1;
        }
    }
    counts
}

pub fn part_one(input: &str) -> Option<u32> {
    let backpacks = input.lines().collect::<Vec<_>>();
    let mut sum: u32 = 0;

    for backpack in backpacks {
        let (comp1, comp2) = backpack.split_at(backpack.len() / 2);

        let counts1 = count(comp1);
        let counts2 = count(comp2);

        for i in 0..52 {
            if counts1[i] > 0 && counts2[i] > 0 {
                sum += i as u32 + 1;
            }
        }
    }

    Some(sum)
}

pub fn part_two(input: &str) -> Option<u32> {
    let backpacks = input.lines().collect::<Vec<_>>();
    let mut sum: u32 = 0;

    for i in 0..backpacks.len() / 3 {
        let back1 = backpacks[3 * i];
        let back2 = backpacks[3 * i + 1];
        let back3 = backpacks[3 * i + 2];

        let cnt1 = count(back1);
        let cnt2 = count(back2);
        let cnt3 = count(back3);

        for i in 0..52 {
            if cnt1[i] > 0 && cnt2[i] > 0 && cnt3[i] > 0 {
                sum += i as u32 + 1;
            }
        }
    }

    Some(sum)
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 3);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 3);
        assert_eq!(part_one(&input), None);
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 3);
        assert_eq!(part_two(&input), None);
    }
}
