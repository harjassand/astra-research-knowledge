"""Finite falsification of one-site color/replicated-program guards.

The mathematical claim is for the infinite checkerboard; this torus check is
only a bounded implementation test.  L=6 exceeds the 4x4 gate read box.
"""

from itertools import product


L = 6
SITES = tuple(product(range(L), repeat=2))


def add(x, y, dx, dy):
    return ((x + dx) % L, (y + dy) % L)


def true_color(x, y):
    return (x & 1, y & 1)


def color_box(anchor):
    x, y = anchor
    return tuple(add(x, y, dx, dy) for dx, dy in product(range(-1, 3), repeat=2))


def valid_guard(colors, anchor):
    box = set(color_box(anchor))
    if colors[anchor] not in ((0, 0), (1, 1)):
        return False
    for x, y in box:
        if add(x, y, 1, 0) in box:
            if colors[add(x, y, 1, 0)] != (colors[x, y][0] ^ 1, colors[x, y][1]):
                return False
        if add(x, y, 0, 1) in box:
            if colors[add(x, y, 0, 1)] != (colors[x, y][0], colors[x, y][1] ^ 1):
                return False
    return True


def inferred_from_ne(colors, site):
    x, y = site
    n = colors[add(x, y, 1, 0)]
    e = colors[add(x, y, 0, 1)]
    return (n[0] ^ 1, n[1]), (e[0], e[1] ^ 1)


def main():
    clean = {site: true_color(*site) for site in SITES}
    clean_guards = {anchor for anchor in SITES if valid_guard(clean, anchor)}
    assert clean_guards == {site for site in SITES if site[0] % 2 == site[1] % 2}
    checks = 0
    for site in SITES:
        for corrupt in product(range(2), repeat=2):
            if corrupt == clean[site]:
                continue
            colors = dict(clean)
            colors[site] = corrupt
            n, e = inferred_from_ne(colors, site)
            assert n == e == clean[site], (site, corrupt, n, e)
            for other in SITES:
                if other == site:
                    continue
                n, e = inferred_from_ne(colors, other)
                assert not (n == e and n != colors[other]), (site, corrupt, other, n, e)
            accepted = {anchor for anchor in SITES if valid_guard(colors, anchor)}
            expected = {anchor for anchor in clean_guards if site not in color_box(anchor)}
            assert accepted == expected, (site, corrupt, accepted ^ expected)
            checks += 1
    for original in range(4):
        for corrupt in range(4):
            if corrupt == original:
                continue
            for position in range(4):
                words = [original] * 4
                words[position] = corrupt
                majority = max(set(words), key=words.count)
                assert majority == original
                assert len({words[i] for i in range(4) if i != position}) == 1
    print("PASS", checks, "one-color-fault patterns; fourfold program majority")


if __name__ == "__main__":
    main()
