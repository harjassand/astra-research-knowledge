"""Small exact diagnostic for the counting family; not a proof substitute."""
import json
from math import prod


def linear(columns, value):
    result = 0
    for i, column in enumerate(columns):
        if (value >> i) & 1:
            result ^= column
    return result


def check(n):
    matrices = []

    def grow(columns, span):
        if len(columns) == n:
            matrices.append(columns)
            return
        for value in range(1, 1 << n):
            if value not in span:
                grow(columns + [value], span | {v ^ value for v in span})

    grow([1], {0, 1})
    maps, laws = set(), set()
    for columns in matrices:
        inverse = {linear(columns, x): x for x in range(1 << n)}
        f = tuple(linear(columns, (inverse[1 << i] << 1) & ((1 << n) - 1))
                  for i in range(n))
        maps.add(f)
        # Quotient by the fixed noise span of bit zero.
        laws.add(tuple(column & ~1 for column in f))
    assert len(matrices) == prod((1 << n) - (1 << j) for j in range(1, n))
    assert len(maps) == len(matrices)
    assert len(laws) * (1 << n) >= len(matrices)
    return dict(n=n, fixed_first_column_T=len(matrices),
                distinct_F=len(maps), distinct_laws=len(laws))


if __name__ == '__main__':
    print(json.dumps([check(n) for n in range(1, 5)], indent=2))
