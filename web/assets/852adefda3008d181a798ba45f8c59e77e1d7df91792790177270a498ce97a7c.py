from itertools import combinations, permutations, product


def powerset_items(n):
    return [frozenset(i for i in range(n) if mask >> i & 1) for mask in range(1 << n)]


def part_matroid(n, blocks):
    blocks = [set(b) for b in blocks]
    def independent(S):
        return all(len(S & B) <= 1 for B in blocks)
    return independent


def greedy(M, S):
    # All elements have unit positive weight; tie break by identity.
    out = set()
    for e in sorted(S):
        if M(out | {e}):
            out.add(e)
    return frozenset(out)


def run_variant(mats, arrival, initial, target_i, mode):
    n = len(initial)
    C = set(i for i, b in enumerate(initial) if b)
    A = set()
    snaps = None
    for t, e in enumerate(arrival):
        if t == target_i:
            snaps = frozenset(C)
        Cp = C ^ {e} # real weight is complementary bit
        cur = [greedy(M, C) for M in mats]
        new = [greedy(M, Cp) for M in mats]
        if mode == 'all_finalized':
            F = set(arrival[:t])
        elif mode == 'accepted_only':
            F = A.copy()
        else:
            raise ValueError(mode)
        passes = all((g & F) == (gp & F) for g, gp in zip(cur, new))
        if passes:
            # A real item has upper value iff it was absent from the initial sample.
            if e not in C and all(e in gp for gp in new):
                A.add(e)
            C = Cp
    return snaps, frozenset(A)


def partitions(n):
    # restricted growth strings enumerate set partitions
    def rec(a, maxv):
        if len(a) == n:
            yield tuple(a)
            return
        for v in range(maxv + 2):
            yield from rec(a + [v], max(maxv, v))
    yield from rec([], -1)


def main():
    for n in range(3, 7):
        parts = list(partitions(n))
        mats = [part_matroid(n, [[i for i, x in enumerate(p) if x == b] for b in set(p)]) for p in parts]
        # Test pairs of partition matroids and all arrival orders, both target times.
        for ia, M1 in enumerate(mats):
            for M2 in mats[ia:]:
                # Require a common-independent set containing every item, so the upper vector's optimum is all items.
                if not all(M1({i}) and M2({i}) for i in range(n)):
                    continue
                for order in permutations(range(n)):
                    for target_i in range(n):
                        counts = {}
                        for init in product((0, 1), repeat=n):
                            snap, A = run_variant((M1, M2), order, init, target_i, 'accepted_only')
                            counts[snap] = counts.get(snap, 0) + 1
                        if len(set(counts.values())) > 1:
                            print('NONUNIFORM', n, 'partition ids', ia, parts[ia], parts.index(next(p for p, m in zip(parts,mats) if m is M2)), 'order', order, 't', target_i, 'counts', counts)
                            return
        print('partition pairs uniform for n=', n)

if __name__ == '__main__':
    main()
