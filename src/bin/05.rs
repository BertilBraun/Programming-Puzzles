fn parse_move(lines: &Vec<&str>, i: usize) -> (u32, u32, u32) {
    let (cnt, rest) = lines[i].split_at(lines[i].find(" from ").unwrap());
    let cnt = cnt.replace("move ", "").parse::<u32>().unwrap();
    let (from, to) = rest.split_at(rest.find(" to ").unwrap());
    let from = from.replace(" from ", "").parse::<u32>().unwrap();
    let to = to.replace(" to ", "").parse::<u32>().unwrap();
    (cnt, from, to)
}

fn parse_stacks(max_height: usize, size: usize, lines: &Vec<&str>, stacks: &mut Vec<Vec<char>>) {
    for i in 0..max_height {
        for j in 0..size {
            let char = lines[i].chars().nth(4 * j + 1).unwrap();
            if char != ' ' {
                stacks[j].push(char);
            }
        }
    }
    for i in 0..size {
        stacks[i].reverse();
    }
}

fn format_result(size: usize, stacks: Vec<Vec<char>>) -> String {
    let mut result: String = String::new();
    for i in 0..size {
        if stacks[i].len() == 0 {
            continue;
        }
        result += stacks[i][stacks[i].len() - 1].to_string().as_str();
    }
    result
}

pub fn part_one(input: &str) -> Option<String> {
    let size = 9;
    let max_height = 8;
    let mut stacks = vec![vec![]; size];

    let lines = input.lines().collect::<Vec<_>>();

    parse_stacks(max_height, size, &lines, &mut stacks);

    for i in max_height + 2..lines.len() {
        let (cnt, from, to) = parse_move(&lines, i);

        for _ in 0..cnt {
            let disc = stacks[from as usize - 1].pop().unwrap();
            stacks[to as usize - 1].push(disc);
        }
    }

    Some(format_result(size, stacks))
}

pub fn part_two(input: &str) -> Option<String> {
    let size = 9;
    let max_height = 8;
    let mut stacks = vec![vec![]; size];

    let lines = input.lines().collect::<Vec<_>>();

    parse_stacks(max_height, size, &lines, &mut stacks);

    for i in max_height + 2..lines.len() {
        let (cnt, from, to) = parse_move(&lines, i);

        let mut temp = vec![];
        for _ in 0..cnt {
            temp.push(stacks[from as usize - 1].pop().unwrap());
        }
        temp.reverse();

        stacks[to as usize - 1].append(&mut temp);
    }

    Some(format_result(size, stacks))
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 5);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 5);
        assert_eq!(part_one(&input), None);
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 5);
        assert_eq!(part_two(&input), None);
    }
}
