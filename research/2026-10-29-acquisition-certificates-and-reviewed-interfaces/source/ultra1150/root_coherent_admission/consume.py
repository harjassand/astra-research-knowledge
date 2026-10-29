"""Exact finite diagnostics for identities, not a proof of asymptotic claims."""
from fractions import Fraction as Q
from itertools import combinations
import hashlib
import json
from pathlib import Path
import time


def components(mask, adj):
    todo = mask
    out = []
    while todo:
        seed = todo & -todo
        todo ^= seed
        comp, frontier = seed, seed
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            new = adj[bit.bit_length() - 1] & todo
            todo ^= new
            frontier |= new
            comp |= new
        out.append(comp)
    return out


def transform(values, n, inverse=False):
    out = values.copy()
    for i in range(n):
        for m in range(1 << n):
            if m & (1 << i):
                if inverse:
                    out[m] += out[m ^ (1 << i)]
                else:
                    out[m] -= out[m ^ (1 << i)]
    return out


def boolean_checks():
    graphs = cases = coefficients = cancelled = 0
    for n in range(1, 6):
        edges = list(combinations(range(n), 2))
        for e in range(1 << len(edges)):
            adj = [0] * n
            for j, (a, b) in enumerate(edges):
                if e & (1 << j):
                    adj[a] |= 1 << b
                    adj[b] |= 1 << a
            sizes = [[c.bit_count() for c in components(m, adj)]
                     for m in range(1 << n)]
            graphs += 1
            for d in range(1, n + 2):
                b = [int(any(z >= d for z in s)) for s in sizes]
                a = transform(b, n)
                assert transform(a, n, inverse=True) == b
                assert a[0] == 0
                for m, am in enumerate(a):
                    coefficients += 1
                    assert abs(am) <= (1 << m.bit_count())
                    if any(z < d for z in sizes[m]):
                        assert am == 0
                        cancelled += 1
                cases += 1
    return dict(graphs=graphs, graph_threshold_cases=cases,
                coefficients=coefficients, forced_zero_coefficients=cancelled)


def symplectic(a, b):
    return ((a[0] & b[1]).bit_count() +
            (a[1] & b[0]).bit_count()) % 2


def pauli(text):
    return (sum(1 << i for i, c in enumerate(text) if c in "XY"),
            sum(1 << i for i, c in enumerate(text) if c in "ZY"))


def multiply(a, b):
    return a[0] ^ b[0], a[1] ^ b[1]


def pauli_text(a, n=5):
    return "".join("IXZY"[((a[0] >> i) & 1) +
                          2 * ((a[1] >> i) & 1)] for i in range(n))


def memory_guardrail():
    generators = list(map(pauli, ["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"]))
    assert all(symplectic(a, b) == 0
               for a, b in combinations(generators, 2))
    stab = {(0, 0)}
    for g in generators:
        stab |= {multiply(s, g) for s in list(stab)}
    assert len(stab) == 16
    syndrome = lambda a: tuple(symplectic(a, g) for g in generators)
    corrections = {}
    for i in range(5):
        for p in "XYZ":
            a = pauli("I" * i + p + "I" * (4 - i))
            assert syndrome(a) not in corrections
            corrections[syndrome(a)] = a
    error = pauli("XXIII")
    correction = corrections[syndrome(error)]
    residual = multiply(error, correction)
    assert syndrome(residual) == (0, 0, 0, 0)
    assert residual not in stab
    assert (residual[0] | residual[1]).bit_count() == 3
    return dict(code="standard non-CSS [[5,1,3]], not the programme CSS seed",
                error=pauli_text(error), correction=pauli_text(correction),
                residual=pauli_text(residual),
                residual_is_nontrivial_logical=True,
                marked_slots=2, distance=3)


def finite_read_moments():
    # One seed/check, five blocks, theta=1/64. Enumerate ALL read and
    # virtual-occupancy words, including all nonempty forced-root sets.
    n, denom = 5, 64
    worst = Q(0)
    cases = 0
    for roots in range(1, 1 << n):
        r = roots.bit_count()
        free = [i for i in range(n) if not (roots >> i) & 1]
        total = 0
        for reads in range(1 << n):
            adj = [0] * n
            for i, j in combinations(range(n), 2):
                between = sum(1 << k for k in range(i + 1, j))
                if not reads & between:
                    adj[i] |= 1 << j
                    adj[j] |= 1 << i
            for word in range(1 << len(free)):
                occ = roots | sum(1 << i for k, i in enumerate(free)
                                 if (word >> k) & 1)
                union = 0
                for comp in components(occ, adj):
                    if comp & roots:
                        union |= comp
                successes = word.bit_count()
                total += ((denom - 1) ** (len(free) - successes)
                          * (1 << union.bit_count()))
                cases += 1
        expectation = Q(total, (1 << n) * denom ** len(free))
        ratio = expectation / (4 ** r)
        assert ratio <= 1
        worst = max(worst, ratio)
    return dict(blocks=n, b=1, K=1, theta="1/64", enumerated_words=cases,
                maximum_moment_to_4power_r=str(worst),
                scope="finite diagnostic only, not the general BFS proof")


def forced_forbidden_checks():
    # An intentionally nonproduct, signed scalar family. Check both
    # rearrangements for ALL 3^6 disjoint forced/forbidden specifications.
    n = 6
    full = (1 << n) - 1
    f = [Q((-1) ** m.bit_count() * (m * m + 3 * m + 7), 17)
         for m in range(1 << n)]
    phi = transform(f, n, inverse=True)
    inclusive = [sum(f[m] for m in range(1 << n) if m & r == r)
                 for r in range(1 << n)]
    cases = 0
    for assignment in range(3 ** n):
        word = assignment
        forced = forbidden = 0
        for j in range(n):
            label = word % 3
            word //= 3
            if label == 1:
                forced |= 1 << j
            elif label == 2:
                forbidden |= 1 << j
        direct = sum(f[m] for m in range(1 << n)
                     if m & forced == forced and not m & forbidden)
        from_inclusive = sum((-1) ** u.bit_count() * inclusive[forced | u]
                             for u in range(1 << n) if u & forbidden == u)
        active = full ^ forbidden
        from_physical = sum((-1) ** u.bit_count() * phi[active ^ u]
                            for u in range(1 << n) if u & forced == u)
        assert direct == from_inclusive == from_physical
        cases += 1
    return dict(slots=n, all_disjoint_specifications=cases,
                family="nonproduct signed rational",
                scope="exact map-coefficient identity only")


def run():
    started = time.perf_counter()
    c = Q(64, 61) * Q(16, 13)
    assert c == Q(1024, 793) and c < 2
    out = dict(status="EXACT_FINITE_DIAGNOSTICS_PASS",
               boolean=boolean_checks(), branching_constant=str(c),
               forced_forbidden=forced_forbidden_checks(),
               read_graph=finite_read_moments(),
               correctness_guardrail=memory_guardrail(),
               random_draws=0, physical_trajectories=0)
    out["elapsed_seconds"] = time.perf_counter() - started
    out["consumer_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    Path(__file__).with_name("EXECUTION.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    run()
