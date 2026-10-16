"""Falsification search for modulo crossed-plaquette controller claims.

Enumerates clean reachable 4x4 states to a bounded integer height, then checks
all alternative one-site residues and searches a two-fault repair trap.
"""

from collections import deque
from itertools import combinations

from check_execution_surface import tiles, successors


L = 4
Q = 8
MAX_HEIGHT = 5
LAYERS = (tiles(L, 0), tiles(L, 1))
INCIDENT = {
    v: tuple((p, tile) for p in (0, 1) for tile in LAYERS[p] if v in tile)
    for v in range(L * L)
}


def valid_mod(vals, parity):
    vals = {x % Q for x in vals}
    if len(vals) == 1:
        return True
    return any(vals == {a, (a + 1) % Q} and a % 2 != parity
               for a in range(Q))


def local_valid(s, v):
    return all(valid_mod((s[i] for i in tile), p) for p, tile in INCIDENT[v])


def valid(s):
    return all(local_valid(s, v) for v in range(L * L))


def candidates(s, v):
    out = []
    for z in range(Q):
        t = list(s)
        t[v] = z
        if local_valid(t, v):
            out.append(z)
    return tuple(out)


def repairable(s):
    for v in range(L * L):
        cs = candidates(s, v)
        if len(cs) == 1 and cs[0] != s[v]:
            yield v, cs[0]


def clean_states():
    start = (0,) * (L * L)
    seen = {start}
    q = deque([start])
    while q:
        s = q.popleft()
        yield s
        for t, _ in successors(s, LAYERS):
            if max(t) <= MAX_HEIGHT and t not in seen:
                seen.add(t)
                q.append(t)


def main():
    states = list(clean_states())
    checks = 0
    for h in states:
        s = tuple(x % Q for x in h)
        assert valid(s), ("invalid clean", h)
        for v in range(L * L):
            for z in range(Q):
                if z == s[v]:
                    continue
                t = list(s)
                t[v] = z
                t = tuple(t)
                assert not valid(t), ("undetected", h, v, z)
                assert candidates(t, v) == (s[v],), ("wrong target", h, v, z, candidates(t, v))
                for w, c in repairable(t):
                    assert (w, c) == (v, s[v]), ("false repair", h, v, z, w, c)
                checks += 1
    print("one-fault modulo PASS", "clean states", len(states), "fault trials", checks)

    zero = (0,) * (L * L)
    trap = None
    for a, b in combinations(LAYERS[0][0], 2):
        t = list(zero)
        t[a] = t[b] = 1
        t = tuple(t)
        if not valid(t) and not list(repairable(t)):
            trap = (a, b, t)
            break
    assert trap is not None
    print("two-fault unique-repair trap", trap[:2], "repairable", list(repairable(trap[2])))

    # Four simultaneous false advances counterfeit a real even-tile gate.
    t = list(zero)
    for v in LAYERS[0][0]:
        t[v] = 1
    assert valid(tuple(t))
    print("four-fault counterfeit gate PASS", LAYERS[0][0])


if __name__ == "__main__":
    main()
