input = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

reports = [list(map(int, line.split())) for line in input.split('\n')]


def is_report_save(report):
    # The levels are either all increasing or all decreasing.
    # Any two adjacent levels differ by at least one and at most three.
    direction = 'inc' if report[1] > report[0] else 'dec'
    for i in range(1, len(report)):
        if direction == 'inc':
            if report[i] - report[i - 1] < 1 or report[i] - report[i - 1] > 3:
                return False
        else:
            if report[i] - report[i - 1] > -1 or report[i] - report[i - 1] < -3:
                return False
    return True


save = 0
for report in reports:
    if is_report_save(report):
        save += 1
    else:
        for i in range(len(report)):
            if is_report_save(report[:i] + report[i + 1 :]):
                save += 1
                break
print(save)
