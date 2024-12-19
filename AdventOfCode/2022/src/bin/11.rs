use std::ops::Rem;

struct Monkey {
    items: Vec<u64>,
    op: Box<dyn Fn(u64) -> u64>,
    test_divisible: u64,
    true_monkey: u64,
    false_monkey: u64,
    count: u64,
}

fn add(a: u64) -> impl Fn(u64) -> u64 {
    move |b: u64| a + b
}

fn mult(a: u64) -> impl Fn(u64) -> u64 {
    move |b: u64| a * b
}

impl Monkey {
    fn from_string(input: &str) -> Monkey {
        let lines = input.lines().collect::<Vec<_>>();

        let items = lines[1]
            .replace("  Starting items: ", "")
            .split(',')
            .map(|x| x.trim())
            .map(|x| x.parse::<u64>().unwrap())
            .collect::<Vec<_>>();

        let operator = lines[2].chars().collect::<Vec<_>>()["  Operation: new = old ".len()];
        let factor = lines[2].chars().collect::<Vec<_>>()["  Operation: new = old ".len() + 2..]
            .iter()
            .collect::<String>();

        let op: Box<dyn Fn(u64) -> u64>;
        if factor.contains("old") {
            op = match operator {
                '+' => Box::new(|x| x + x),
                '*' => Box::new(|x| x * x),
                _ => panic!("Unknown operation"),
            };
        } else {
            let factor = factor.trim().parse::<u64>().unwrap();
            op = match operator {
                '+' => Box::new(add(factor)),
                '*' => Box::new(mult(factor)),
                _ => panic!("Unknown operation"),
            };
        }

        let test_divisible = lines[3]
            .replace("  Test: divisible by ", "")
            .parse::<u64>()
            .unwrap();
        let true_monkey = lines[4]
            .replace("    If true: throw to monkey ", "")
            .parse::<u64>()
            .unwrap();
        let false_monkey = lines[5]
            .replace("    If false: throw to monkey ", "")
            .parse::<u64>()
            .unwrap();

        Monkey {
            items: items,
            op: op,
            test_divisible: test_divisible,
            true_monkey: true_monkey,
            false_monkey: false_monkey,
            count: 0,
        }
    }
}

pub fn part_one(input: &str) -> Option<u64> {
    let mut monkeys = input
        .split("\n\n")
        .map(|x| Monkey::from_string(x))
        .collect::<Vec<_>>();

    for _ in 0..20 {
        for i in 0..monkeys.len() {
            for item in monkeys[i].items.clone().iter() {
                let new_item = (monkeys[i].op)(*item) / 3;
                monkeys[i].count += 1;

                if new_item % monkeys[i].test_divisible == 0 {
                    let true_monkey = monkeys[i].true_monkey;
                    monkeys[true_monkey as usize].items.push(new_item);
                } else {
                    let false_monkey = monkeys[i].false_monkey;
                    monkeys[false_monkey as usize].items.push(new_item);
                }
            }
            monkeys[i].items.clear();
        }
    }

    monkeys.sort_by(|a, b| b.count.cmp(&a.count));
    Some(monkeys[0].count * monkeys[1].count)
}

pub fn part_two(input: &str) -> Option<u64> {
    let mut monkeys = input
        .split("\n\n")
        .map(|x| Monkey::from_string(x))
        .collect::<Vec<_>>();

    let mut modulo: u64 = 1;
    for monkey in monkeys.iter() {
        modulo *= monkey.test_divisible;
    }

    for _ in 0..10000 {
        for i in 0..monkeys.len() {
            for item in monkeys[i].items.clone().iter() {
                let new_item = (monkeys[i].op)(*item).rem(modulo);
                monkeys[i].count += 1;

                if new_item % monkeys[i].test_divisible == 0 {
                    let true_monkey = monkeys[i].true_monkey;
                    monkeys[true_monkey as usize].items.push(new_item);
                } else {
                    let false_monkey = monkeys[i].false_monkey;
                    monkeys[false_monkey as usize].items.push(new_item);
                }
            }
            monkeys[i].items.clear();
        }
    }

    monkeys.sort_by(|a, b| b.count.cmp(&a.count));
    Some(monkeys[0].count * monkeys[1].count)
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 11);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 11);
        assert_eq!(part_one(&input), None);
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 11);
        assert_eq!(part_two(&input), None);
    }
}
