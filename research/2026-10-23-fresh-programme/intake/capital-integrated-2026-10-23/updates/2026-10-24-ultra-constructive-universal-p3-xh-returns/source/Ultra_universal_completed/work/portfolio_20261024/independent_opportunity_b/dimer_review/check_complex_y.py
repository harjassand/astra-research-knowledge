#!/usr/bin/env python3
"""Bounded exact complex/Y extension; not a general evaluator implementation.

Uses the copied owner's bond Fock vectors and matching enumerator, then checks
them against a separate symbolic determinant route. Complex conjugation,
filtered activities, the gas recursion, and Pauli Y are supplied here.
"""
from collections import defaultdict
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import sympy as sp

from check_dimer_contraction import bond_state, pmatch, pairing_graph, connected

R = sp.Rational
I = sp.I
expand = sp.expand


def overlap(a, b):
    return expand(sum(sp.conjugate(x) * b.get(k, 0) for k, x in a.items()))


def coefficient(f, matching):
    return expand(sp.prod(f[i][j] for i, j in matching))


def pair_state(f, sites):
    answer = defaultdict(lambda: sp.S.Zero)
    for matching in pmatch(f, sites):
        c = coefficient(f, matching)
        for mask, value in bond_state(matching).items():
            answer[mask] += c * value
    return {k: expand(v) for k, v in answer.items() if expand(v) != 0}


def pauli(a, site, name):
    answer = {}
    for mask, value in a.items():
        up = bool(mask & (1 << site))
        if name == "Z":
            key, phase = mask, 1 if up else -1
        elif name == "X":
            key, phase = mask ^ (1 << site), 1
        elif name == "Y":
            key, phase = mask ^ (1 << site), I if up else -I
        else:
            raise ValueError(name)
        answer[key] = expand(phase * value)
    return answer


def apply_filters(a, filters):
    out = dict(a)
    for site, name, strength in filters:
        changed = pauli(out, site, name)
        keys = set(out) | set(changed)
        out = {k: expand(out.get(k, 0) + strength * changed.get(k, 0))
               for k in keys}
        out = {k: v for k, v in out.items() if v != 0}
    return out


def weights(f, reference, filters):
    owner, ref, graph = pairing_graph(f, reference)
    m = len(reference)
    result = {}
    for support in range(1, 1 << m):
        if support.bit_count() < 2 or not connected(support, graph):
            continue
        cells = [v for v in range(m) if support >> v & 1]
        sites = {v for a in cells for v in reference[a]}
        local = [z for z in filters if z[0] in sites]
        baseline = apply_filters(bond_state(tuple(reference[a] for a in cells)), local)
        denominator = overlap(baseline, baseline)
        matchings = list(pmatch(f, sites))
        vectors = {p: apply_filters(bond_state(p), local) for p in matchings}
        coeffs = {p: coefficient(f, p) for p in matchings}
        total = 0
        for p in matchings:
            for q in matchings:
                active = 0
                used_graph = [set() for _ in reference]
                for i, j in p + q:
                    if (i, j) not in ref:
                        a, b = owner[i], owner[j]
                        active |= (1 << a) | (1 << b)
                        used_graph[a].add(b)
                        used_graph[b].add(a)
                if active == support and connected(support, used_graph):
                    total += (sp.conjugate(coeffs[p]) * coeffs[q]
                              * overlap(vectors[p], vectors[q]) / denominator)
        result[support] = expand(total)
        assert sp.im(result[support]) == 0
    return result, graph


def gas(polymer_weights, m):
    @lru_cache(None)
    def solve(mask):
        if not mask:
            return sp.S.One
        v = mask & -mask
        value = solve(mask ^ v)
        for c, w in polymer_weights.items():
            if c & v and c & mask == c:
                value += w * solve(mask ^ c)
        return expand(value)
    return solve((1 << m) - 1)


def checked_norm(f, reference, filters, rho):
    w, _ = weights(f, reference, filters)
    z0 = overlap(apply_filters(bond_state(reference), filters),
                 apply_filters(bond_state(reference), filters))
    target_state = apply_filters(pair_state(f, range(len(f))), filters)
    direct = overlap(target_state, target_state)
    assert expand(z0 * gas(w, len(reference)) - direct) == 0
    h = 2 * rho + rho**2
    factor = (R(21, 19)**4) if filters else 1
    for c, wc in w.items():
        assert abs(wc) <= (factor * h)**c.bit_count()
    return direct, w


def main():
    n = 6
    # Interleaved reference sites test the even-component fermionic factorization.
    reference = ((0, 3), (1, 4), (2, 5))
    f = [[sp.S.Zero for _ in range(n)] for _ in range(n)]
    refs = set(reference)
    phases = (1 + I, -1 + I, 1 - I, -1 - I, I, -I)
    lam = R(1, 65536)
    for i, j in combinations(range(n), 2):
        f[i][j] = f[j][i] = (1 if (i, j) in refs else
                             lam * phases[(3*i + j) % len(phases)])
    psi = pair_state(f, range(n))
    for up in combinations(range(n), n // 2):
        down = [j for j in range(n) if j not in up]
        minor = sp.Matrix([[f[i][j] for j in down] for i in up]).det()
        inversion = sum(j < i for i in up for j in down)
        signed = (-1)**((n//2)*(n//2-1)//2 + inversion) * minor
        assert expand(psi.get(sum(1 << i for i in up), 0) - signed) == 0
    rho = max(sum(abs(sp.re(f[i][j])) + abs(sp.im(f[i][j]))
                  for j in range(n)
                  if (min(i, j), max(i, j)) not in refs)
              for i in range(n))
    assert rho <= R(1, 384*2)
    norm, unfiltered_weights = checked_norm(f, reference, (), rho)
    observables = []
    for string in (((0, "Y"), (1, "Y")),
                   ((0, "X"), (1, "Y"), (3, "Z"))):
        t = R(1, 20)
        numerator = 0
        for signs in product((-1, 1), repeat=len(string)):
            filters = [(site, name, t*sign) for (site, name), sign in zip(string, signs)]
            z, _ = checked_norm(f, reference, filters, rho)
            numerator += sp.prod(signs) * z
        p = 2*t/(1+t*t)
        recovered = expand(numerator/(2**len(string)*(1+t*t)**len(string)*p**len(string)*norm))
        changed = psi
        for site, name in string:
            changed = pauli(changed, site, name)
        direct = expand(overlap(psi, changed)/norm)
        assert expand(recovered-direct) == 0
        observables.append({"string": str(string), "exact": str(direct),
                            "includes_Y": True, "nonzero": direct != 0})
    result = {
        "scope": "BOUNDED_EXACT_COMPLEX_AND_Y_EXTENSION",
        "fixture_n": n,
        "reference": reference,
        "rho_rational_L1_upper": str(rho),
        "norm": str(norm),
        "activities": {str(c): str(w) for c, w in unfiltered_weights.items()},
        "observables": observables,
        "all_checks_passed": True,
        "independence": "Owner copied bond Fock vectors/matching enumerator reused; independent symbolic determinant, complex conjugation, gas recursion, and Pauli/filter calculations.",
        "limits": "One n=6 fixture, not all-size proof, general gauge code, FPTAS implementation, runtime comparison or physical acquisition."
    }
    output = Path(__file__).with_name("COMPLEX_Y_RESULTS.json")
    output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
