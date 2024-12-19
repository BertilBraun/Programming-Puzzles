input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


ordering_rules = [tuple(map(int, line.split('|'))) for line in input.split('\n\n')[0].split('\n')]

pages = [list(map(int, line.split(','))) for line in input.split('\n\n')[1].split('\n')]


def is_correctly_ordered(page):
    for first, second in ordering_rules:
        if first not in page or second not in page:
            continue
        if page.index(first) > page.index(second):
            return False

    return True


def fix_page(page):
    for first, second in ordering_rules:
        if first not in page or second not in page:
            continue
        first_index = page.index(first)
        second_index = page.index(second)
        if first_index > second_index:
            page[first_index], page[second_index] = page[second_index], page[first_index]
            return fix_page(page)

    return page


print(sum(fix_page(page)[len(page) // 2] for page in pages if not is_correctly_ordered(page)))
