use regex::Regex;

fn parse_sensor_and_beacon(input: &str) -> ((i64, i64), (i64, i64)) {
    // Sensor at x=3482210, y=422224: closest beacon is at x=2273934, y=-2022000000439
    let regex =
        Regex::new(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
            .unwrap();
    let parts = regex.captures(input).unwrap();
    let sensor = (
        parts.get(1).unwrap().as_str().parse().unwrap(),
        parts.get(2).unwrap().as_str().parse().unwrap(),
    );
    let beacon = (
        parts.get(3).unwrap().as_str().parse().unwrap(),
        parts.get(4).unwrap().as_str().parse().unwrap(),
    );
    (sensor, beacon)
}

pub fn part_one(input: &str) -> Option<i64> {
    let sensor_and_beacon = input
        .lines()
        .map(parse_sensor_and_beacon)
        .collect::<Vec<_>>();

    let line_y = 2000000;

    let covered = get_covered_for_y(sensor_and_beacon, line_y);

    Some(get_covered_area(&covered))
}

fn get_covered_for_y(
    sensor_and_beacon: Vec<((i64, i64), (i64, i64))>,
    line: i64,
) -> Vec<(i64, i64)> {
    let mut covered = vec![];
    for (sensor, beacon) in sensor_and_beacon {
        let dist = (sensor.0 - beacon.0).abs() + (sensor.1 - beacon.1).abs();
        let line_dist = (sensor.1 - line).abs();

        if dist < line_dist {
            // The sensor is inside the circle
            continue;
        }

        let p1 = sensor.0 - (dist - line_dist);
        let p2 = sensor.0 + (dist - line_dist);

        if p1 > p2 {
            covered.push((p2, p1));
        } else {
            covered.push((p1, p2));
        }
    }
    covered
}

fn merge_ranges(ranges: &Vec<(i64, i64)>) -> Vec<(i64, i64)> {
    let mut ranges = ranges.clone();
    ranges.sort_by(|a, b| a.0.cmp(&b.0));

    let mut merged = vec![];
    let mut current_end = -100000000000;

    for (start, end) in ranges {
        if start > current_end {
            // This range does not overlap with the previous one, so we can just add it to the merged list
            merged.push((start, end));
            current_end = end;
        } else {
            // This range overlaps with the previous one, so we need to update the current end point to the maximum of the two end points
            if end > current_end {
                merged.last_mut().unwrap().1 = end;
                current_end = end;
            }
        }
    }
    merged
}

fn get_covered_area(covered: &Vec<(i64, i64)>) -> i64 {
    let merged = merge_ranges(covered);
    merged.iter().map(|(start, end)| end - start).sum()
}

pub fn part_two(input: &str) -> Option<i64> {
    let size = 4000000;

    let sensor_and_beacon = input
        .lines()
        .map(parse_sensor_and_beacon)
        .collect::<Vec<_>>();

    for y in 0..size {
        let covered = get_covered_for_y(sensor_and_beacon.clone(), y);
        let merged = merge_ranges(&covered);

        if merged.len() > 1 {
            let hole = merged[0].1 + 1;
            return Some(hole * 4000000 + y);
        }
    }

    None
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 15);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 15);
        assert_eq!(part_one(&input), None);
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 15);
        assert_eq!(part_two(&input), None);
    }
}
