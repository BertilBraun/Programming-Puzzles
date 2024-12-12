use std::ops::Rem;

fn inc_cycle(cycle: &mut i32, sum: &mut i32, cur_val: i32) {
    let check_cycles = vec![20, 60, 100, 140, 180, 220];

    *cycle += 1;
    if check_cycles.contains(&*cycle) {
        *sum += *cycle * cur_val;
    }
}

pub fn part_one(input: &str) -> Option<u32> {
    let mut sum = 0;
    let mut cur_val = 1;
    let mut cycle = 0;

    for line in input.lines() {
        if line == "noop" {
            inc_cycle(&mut cycle, &mut sum, cur_val);
        } else {
            let val = line.replace("addx ", "").parse::<i32>().unwrap();
            inc_cycle(&mut cycle, &mut sum, cur_val);
            inc_cycle(&mut cycle, &mut sum, cur_val);
            cur_val += val;
        }
    }

    Some(sum as u32)
}

pub fn part_two(input: &str) -> Option<String> {
    let mut res: String = String::new();
    let mut cur_val = 1;
    let mut cycle = 0;

    for line in input.lines() {
        if line == "noop" {
            inc_cycle_two(&mut cycle, cur_val, &mut res);
        } else {
            let val = line.replace("addx ", "").parse::<i32>().unwrap();
            inc_cycle_two(&mut cycle, cur_val, &mut res);
            inc_cycle_two(&mut cycle, cur_val, &mut res);
            cur_val += val;
        }
    }

    Some(res)
}

fn inc_cycle_two(cycle: &mut i32, cur_val: i32, res: &mut String) {
    if abs(cur_val - (*cycle).rem(40)) <= 1 {
        *res += "#";
    } else {
        *res += ".";
    }
    *cycle += 1;
    if cycle.rem(40) == 0 {
        *res += "\n";
    }
}

fn abs(cycle: i32) -> i32 {
    if cycle < 0 {
        return -cycle;
    }
    cycle
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 10);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 10);
        assert_eq!(part_one(&input), None);
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 10);
        assert_eq!(part_two(&input), None);
    }
}
