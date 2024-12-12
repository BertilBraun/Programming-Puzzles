use std::vec;

#[derive(Debug)]
struct Packet {
    value: Option<u32>,
    list: Vec<Packet>,
}

fn parse_line(line: &str) -> Packet {
    let mut packets = vec![];

    for mut token in line.split(",") {
        while !token.is_empty() && token.chars().nth(0).unwrap() == '[' {
            packets.push(Packet {
                value: None,
                list: vec![],
            });
            token = &token[1..];
        }

        let mut to_pop = 0;
        while !token.is_empty() && token.chars().nth(token.len() - 1).unwrap() == ']' {
            to_pop += 1;
            token = &token[..token.len() - 1];
        }

        if !token.is_empty() {
            packets.last_mut().unwrap().list.push(Packet {
                value: Some(token.parse::<u32>().unwrap()),
                list: vec![],
            });
        }

        for _ in 0..to_pop {
            let last = packets.pop().unwrap();
            if packets.is_empty() {
                return last;
            }
            packets.last_mut().unwrap().list.push(last);
        }
    }

    Packet {
        value: None,
        list: vec![],
    }
}

fn create_wrapped_packet(value: u32) -> Packet {
    Packet {
        value: None,
        list: vec![Packet {
            value: Some(value),
            list: vec![],
        }],
    }
}

fn equals_packet(a: &Packet, b: &Packet) -> bool {
    a.value == b.value
        && a.list.len() == b.list.len()
        && a.list
            .iter()
            .enumerate()
            .all(|(i, packet)| equals_packet(packet, &b.list[i]))
}

fn compare_packets(a: &Packet, b: &Packet) -> std::cmp::Ordering {
    if a.value.is_some() && b.value.is_some() {
        return a.value.unwrap().cmp(&b.value.unwrap());
    }

    if a.value.is_some() {
        return compare_packets(&create_wrapped_packet(a.value.unwrap()), b);
    }
    if b.value.is_some() {
        return compare_packets(a, &create_wrapped_packet(b.value.unwrap()));
    }

    for (i, packet) in b.list.iter().enumerate() {
        if i >= a.list.len() {
            return std::cmp::Ordering::Less;
        }

        let result = compare_packets(&a.list[i], packet);
        if result != std::cmp::Ordering::Equal {
            return result;
        }
    }

    if a.list.len() > b.list.len() {
        return std::cmp::Ordering::Greater;
    }

    std::cmp::Ordering::Equal
}

fn in_correct_order(block: &str) -> bool {
    let lines = block.lines().collect::<Vec<&str>>();
    let first = parse_line(lines[0]);
    let second = parse_line(lines[1]);

    compare_packets(&first, &second) == std::cmp::Ordering::Less
}

pub fn part_one(input: &str) -> Option<u32> {
    let blocks = input.split("\n\n").collect::<Vec<&str>>();
    let mut sum = 0;

    for (i, block) in blocks.iter().enumerate() {
        if in_correct_order(block) {
            sum += i + 1;
        }
    }

    Some(sum as u32)
}

pub fn part_two(input: &str) -> Option<u32> {
    let mut packets = input
        .replace("\n\n", "\n")
        .lines()
        .map(parse_line)
        .collect::<Vec<Packet>>();

    packets.push(create_wrapped_packet(2));
    packets.push(create_wrapped_packet(6));

    packets.sort_by(|a, b| compare_packets(a, b));

    let first_index = packets
        .iter()
        .position(|packet| equals_packet(packet, &create_wrapped_packet(2)))
        .unwrap();
    let second_index = packets
        .iter()
        .position(|packet| equals_packet(packet, &create_wrapped_packet(6)))
        .unwrap();

    Some(((first_index + 1) * (second_index + 1)) as u32)
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 13);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 13);
        assert_eq!(part_one(&input), None);
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 13);
        assert_eq!(part_two(&input), None);
    }
}
