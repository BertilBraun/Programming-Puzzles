from functools import cache


input = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

available = [x.strip() for x in input.split('\n\n')[0].split(', ')]
required = [x.strip() for x in input.split('\n\n')[1].split('\n')]

available.sort(key=lambda x: len(x), reverse=True)


@cache
def can_build(text):
    if not text:
        return 1
    return sum(can_build(text[len(a) :]) for a in available if text.startswith(a))


print(sum(can_build(x) for x in required))
