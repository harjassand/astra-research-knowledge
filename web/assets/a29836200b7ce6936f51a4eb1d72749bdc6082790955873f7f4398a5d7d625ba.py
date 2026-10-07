"""Finite check of OA113 Lemma 5.1's stated splitting rule, not a proof."""
from collections import Counter
import json


def audit(labels):
    m = len(labels)
    sets = [set((labels[(i - 1) % m], labels[i])) for i in range(m)]
    cells = []

    def good(arc):
        return len(arc) == 2 or bool(sets[arc[1]] & sets[arc[-2]])

    def admissible(arc):
        return (len(arc) - 1) % 2 == 1 and bool(sets[arc[0]] & sets[arc[-1]])

    def exterior(arc):
        direction = 1 if (arc[1] - arc[0]) % m == 1 else -1
        out = [arc[-1]]
        while out[-1] != arc[0]:
            out.append((out[-1] + direction) % m)
        return out

    def edge_labels(arc):
        return [labels[u] if (v-u) % m == 1 else labels[v]
                for u, v in zip(arc, arc[1:])]

    def split(arc):
        assert admissible(arc)
        s = len(arc)-1
        if s == 1:
            return
        P = min(sets[arc[0]] & sets[arc[-1]])
        ext = exterior(arc)
        a = edge_labels(arc)
        if good(ext):
            if P not in a:
                assert a[0] == a[-1]
                P = a[0]
            odds = [i for i, x in enumerate(a) if x == P and i % 2]
            hits = [i for i, x in enumerate(a) if x == P]
            if odds:
                p1, p2 = odds[0], odds[0]+1
            elif hits[0] > 0:
                p1, p2 = hits[0]-1, hits[0]
            elif hits[-1] < s-1:
                p1, p2 = hits[-1]+1, hits[-1]+2
            else:
                p1, p2 = 1, s-1
        else:
            if P in sets[ext[-2]]:
                arc = list(reversed(arc))
                ext = exterior(arc)
                a = edge_labels(arc)
            assert P not in sets[ext[-2]] and a[0] == P
            if a[-1] == P:
                p1, p2 = 1, s-1
            else:
                t = max(i for i, x in enumerate(a) if x == P)+1
                assert a[t] == a[-1]
                p1, p2 = (1, t) if t % 2 == 0 else (t, s-1)
        assert 0 < p1 < p2 < s and p1 % 2 == 1 and p2 % 2 == 0
        arcs = [arc[:p1+1], arc[p1:p2+1], arc[p2:], ext]
        assert all(admissible(J) for J in arcs)
        goods = list(map(good, arcs))
        longs = [len(J) > 2 for J in arcs]
        assert (goods[0] and goods[2]) or (goods[1] and goods[3])
        for i in range(2):
            if longs[i] and longs[i+2]:
                assert goods[1-i] and goods[3-i]
        covered = Counter(tuple(sorted((u, v)))
                          for J in arcs for u, v in zip(J, J[1:]))
        assert covered == Counter(tuple(sorted((i, (i+1) % m))) for i in range(m))
        cells.append(arcs)
        for J in arcs[:3]:
            split(J)

    split(list(range(m)))
    assert len(cells) == (m-2)//2


def closed_walks(neighbors, m):
    def extend(seq):
        if len(seq) == m:
            if seq[0] in neighbors[seq[-1]]:
                yield tuple(seq)
            return
        for nxt in neighbors[seq[-1]]:
            yield from extend(seq+[nxt])
    for first in neighbors:
        yield from extend([first])


trees = {
    "path3": {0: (0, 1), 1: (0, 1, 2), 2: (1, 2)},
    "path4": {0: (0, 1), 1: (0, 1, 2), 2: (1, 2, 3), 3: (2, 3)},
    "star4": {0: (0, 1, 2, 3), 1: (0, 1), 2: (0, 2), 3: (0, 3)},
}
counts = {}
for tree, neighbors in trees.items():
    for m in (4, 6, 8, 10):
        n = 0
        for labels in closed_walks(neighbors, m):
            audit(labels)
            n += 1
        counts[f"{tree}/m={m}"] = n
print(json.dumps({"status": "all checked instances passed", "counts": counts,
                  "total": sum(counts.values()), "scope": "Lemma 5.1 finite splitting check"}, indent=2))
