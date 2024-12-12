use std::collections::HashSet;

pub fn part_one(input: &str) -> Option<u32> {
    let mut seen = HashSet::new();

    let mut h: (i32, i32) = (0, 0);
    let mut t: (i32, i32) = (0, 0);
    seen.insert(t);

    for line in input.lines() {
        let (dir, num) = line.split_at(1);
        let num = num.split_at(1).1.parse::<i32>().unwrap();

        for _ in 0..num {
            match dir {
                "R" => h.0 += 1,
                "L" => h.0 -= 1,
                "U" => h.1 += 1,
                "D" => h.1 -= 1,
                _ => panic!("Invalid direction"),
            }

            t = follow(t, h);
            seen.insert(t);
        }
    }

    Some(seen.len() as u32)
}

fn follow(t_in: (i32, i32), h: (i32, i32)) -> (i32, i32) {
    let old_t = t_in;
    let mut t = t_in;
    if (h.0 - old_t.0).abs() == 2 {
        t.0 += (h.0 - old_t.0).signum();
    }
    if (h.1 - old_t.1).abs() == 2 {
        t.1 += (h.1 - old_t.1).signum();
    }
    if (h.0 - old_t.0).abs() + (h.1 - old_t.1).abs() == 3 {
        if (h.0 - old_t.0).abs() == 2 {
            t.1 += (h.1 - old_t.1).signum();
        } else {
            t.0 += (h.0 - old_t.0).signum();
        }
    }
    t
}

pub fn part_two(input: &str) -> Option<u32> {
    let mut seen = HashSet::new();

    let mut list = Vec::new();
    for _ in 0..10 {
        list.push((0, 0) as (i32, i32));
    }
    seen.insert((0, 0));

    for line in input.lines() {
        let (dir, num) = line.split_at(1);
        let num = num.split_at(1).1.parse::<i32>().unwrap();

        for _ in 0..num {
            match dir {
                "R" => list[0].0 += 1,
                "L" => list[0].0 -= 1,
                "U" => list[0].1 += 1,
                "D" => list[0].1 -= 1,
                _ => panic!("Invalid direction"),
            }

            for i in 1..list.len() {
                list[i] = follow(list[i], list[i - 1]);
            }

            seen.insert(list[list.len() - 1]);
        }
    }

    Some(seen.len() as u32)
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 9);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 9);
        assert_eq!(part_one(&input), None);
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 9);
        assert_eq!(part_two(&input), None);
    }
}
