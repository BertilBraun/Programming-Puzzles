use std::{collections::HashMap, fmt::Debug};

// create class directory
struct directory {
    name: String,
    weight: u32,
    children: HashMap<String, directory>,
}

impl Debug for directory {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("directory")
            .field("name", &self.name)
            .field("weight", &self.weight)
            .field("children", &self.children.keys().collect::<Vec<_>>())
            .finish()
    }
}

// parse input into a vector of directories
fn parse_input(input: &str) -> directory {
    let mut root = directory {
        name: "/".to_string(),
        weight: 0,
        children: HashMap::new(),
    };
    let mut i = 0;
    let lines = input.lines().collect::<Vec<_>>();

    let mut stack = Vec::new();
    stack.push(&mut root);

    while i < lines.len() {
        let line = lines[i].chars().collect::<Vec<_>>();
        if line[0] == '$' {
            if line[2] == 'c' && line[3] == 'd' {
                if line[5] == '/' {
                    stack.clear();
                    stack.push(&mut root);
                } else if line[5] == '.' && line[6] == '.' {
                    stack.pop();
                } else {
                    let dir = line[5..].iter().collect::<String>();
                    if !stack.last().unwrap().children.contains_key(&dir) {
                        stack.last().unwrap().children.insert(
                            dir,
                            directory {
                                name: line[5..].iter().collect::<String>(),
                                weight: 0,
                                children: HashMap::new(),
                            },
                        );
                    }
                    let dir = line[5..].iter().collect::<String>();
                    println!("Found dir: {}", dir);
                    stack.push(stack.last().unwrap().children.get_mut(&dir).unwrap());
                }
                i += 1;
            }

            if line[2] == 'l' && line[3] == 's' {
                while i + 1 < lines.len() && !lines[i + 1].contains('$') {
                    i += 1;
                    if !lines[i].starts_with(&"dir") {
                        let (size, rest) = lines[i].split_at(lines[i].find(' ').unwrap());
                        stack.last().unwrap().weight += size.parse::<u32>().unwrap();
                    }
                }
                i += 1;
            }
        }
    }

    root
}

fn dir_size(dir: &directory) -> u32 {
    let mut size = dir.weight;
    for child in dir.children.values() {
        size += dir_size(child);
    }
    size
}

fn sum_size_less_than(dir: &directory, size: u32) -> u32 {
    let mut sum = 0;
    for child in dir.children.values() {
        if dir_size(child) < size {
            sum += dir_size(child);
        }
        sum += sum_size_less_than(child, size);
    }
    sum
}

pub fn part_one(input: &str) -> Option<u32> {
    let root = parse_input(input);

    println!("{:?}", root);

    Some(sum_size_less_than(&root, 100000))
}

pub fn part_two(input: &str) -> Option<u32> {
    None
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 7);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 7);
        assert_eq!(part_one(&input), None);
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 7);
        assert_eq!(part_two(&input), None);
    }
}
