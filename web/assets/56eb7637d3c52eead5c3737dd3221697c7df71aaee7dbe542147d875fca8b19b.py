#!/usr/bin/env python3
"""Exact audit of a paired cross-replica one-coordinate worm augmentation."""
from fractions import Fraction
from itertools import combinations, permutations
import json
from pathlib import Path
import sys

N, K = 6, 3
ODD = (1, 3, 5)
EVEN = (0, 2, 4)

def parity(p):
    return -1 if sum(p[a] > p[b] for a in range(len(p)) for b in range(a + 1, len(p))) % 2 else 1

def det3(a):
    return sum((Fraction(parity(p)) * a[0][p[0]] * a[1][p[1]] * a[2][p[2]] for p in permutations(range(3))), Fraction(0))

def run(bits):
    eps = Fraction(1, 2**bits)
    F = [[Fraction(0) for _ in range(N)] for _ in range(N)]
    for i in range(N):
        F[i][(i + 1) % N] = 1
        F[i][(i - 1) % N] = eps
    states = list(combinations(range(N), K))
    amp, wt = {}, {}
    for I in states:
        J = tuple(j for j in range(N) if j not in I)
        amp[I] = det3([[F[i][j] for j in J] for i in I])
        wt[I] = amp[I] ** 2
    support = [I for I in states if wt[I] > 0]
    Z = sum((wt[I] for I in states), Fraction(0))
    pi = {I: wt[I] / Z for I in support}
    p = pi[ODD]

    expected_groups = {
        Fraction(1) + eps**3: {EVEN, ODD},
        eps: {(0, 1, 3), (0, 2, 5), (0, 3, 4), (1, 2, 4), (1, 4, 5), (2, 3, 5)},
        eps**2: {(0, 1, 4), (0, 2, 3), (0, 3, 5), (1, 2, 5), (1, 3, 4), (2, 4, 5)},
        Fraction(0): {(0, 1, 2), (0, 1, 5), (0, 4, 5), (1, 2, 3), (2, 3, 4), (3, 4, 5)},
    }
    assert set().union(*expected_groups.values()) == set(states)
    for amp_value, members in expected_groups.items():
        assert {I for I in states if amp[I] == amp_value} == members

    def add_move(row, target, prob):
        row[target] = row.get(target, Fraction(0)) + prob

    # One-replica symmetric-proposal Metropolis kernel.
    M = {}
    for I in support:
        row = {}
        for i in I:
            for j in set(range(N)) - set(I):
                J = tuple(sorted((set(I) - {i}) | {j}))
                q = Fraction(1, 9)
                acc = min(Fraction(1), wt[J] / wt[I]) if wt[J] else Fraction(0)
                add_move(row, J, q * acc)
                add_move(row, I, q * (1 - acc))
        assert sum(row.values(), Fraction(0)) == 1
        M[I] = row

    # Pair states and exact Metropolis rows. Mixture: replica swap, local A,
    # local B, cross-replica exchange, each selected with probability 1/4.
    pairs = [(A, B) for A in support for B in support]
    pair_pi = {(A, B): pi[A] * pi[B] for A, B in pairs}
    def G(x):
        return int(x[0] == ODD) + int(x[1] == ODD)
    energy = Fraction(0)
    pair_row_exit = None
    rows = {}
    for A, B in pairs:
        x = (A, B)
        row = {}
        add_move(row, (B, A), Fraction(1, 4))
        for target, prob in M[A].items():
            add_move(row, (target, B), prob / 4)
        for target, prob in M[B].items():
            add_move(row, (A, target), prob / 4)
        diff_ab = set(A) - set(B)
        diff_ba = set(B) - set(A)
        if diff_ab:
            assert len(diff_ab) == len(diff_ba)
            q = Fraction(1, len(diff_ab) ** 2)
            for i in diff_ab:
                for j in diff_ba:
                    A2 = tuple(sorted((set(A) - {i}) | {j}))
                    B2 = tuple(sorted((set(B) - {j}) | {i}))
                    ratio = wt[A2] * wt[B2] / (wt[A] * wt[B]) if wt[A2] and wt[B2] else Fraction(0)
                    acc = min(Fraction(1), ratio)
                    add_move(row, (A2, B2), q * acc / 4)
                    add_move(row, x, q * (1 - acc) / 4)
        else:
            add_move(row, x, Fraction(1, 4))
        assert sum(row.values(), Fraction(0)) == 1
        rows[x] = row
        if x == (ODD, ODD):
            pair_row_exit = sum((prob for target, prob in row.items() if target != x), Fraction(0))
        for y, prob in row.items():
            energy += pair_pi[x] * prob * (G(x) - G(y)) ** 2 / 2
    for x, row in rows.items():
        for y, prob in row.items():
            if prob == 0:
                continue
            assert pair_pi[x] * prob == pair_pi[y] * rows[y].get(x, Fraction(0))
    variance_f = p * (1 - p)
    ratio = variance_f / energy
    phi_one = (eps**2 + eps**4) / (3 * (1 + eps**3) ** 2)
    assert pair_row_exit == phi_one / 2
    assert variance_f > 0 and energy > 0
    return {
        "b": bits,
        "epsilon": f"{eps.numerator}/{eps.denominator}",
        "positive_microstates": len(support),
        "positive_pair_states": len(pairs),
        "exact_amplitude_table": [
            {"I": list(I), "amplitude": f"{amp[I].numerator}/{amp[I].denominator}",
             "weight": f"{wt[I].numerator}/{wt[I].denominator}"}
            for I in states
        ],
        "pair_kernel_detailed_balance_exact": True,
        "Z": f"{Z.numerator}/{Z.denominator}",
        "pi_odd": f"{p.numerator}/{p.denominator}",
        "pi_odd_decimal": float(p),
        "pair_mode_mass": f"{(p*p).numerator}/{(p*p).denominator}",
        "pair_mode_exit_exact": f"{pair_row_exit.numerator}/{pair_row_exit.denominator}",
        "pair_mode_exit_decimal": float(pair_row_exit),
        "additive_variance_exact": f"{variance_f.numerator}/{variance_f.denominator}",
        "additive_dirichlet_exact": f"{energy.numerator}/{energy.denominator}",
        "required_L_exact": f"{ratio.numerator}/{ratio.denominator}",
        "required_L_decimal": float(ratio),
    }

if __name__ == "__main__":
    results = [run(int(x)) for x in (sys.argv[1:] or [4, 8])]
    out = Path(__file__).with_name("cross_worm_energy_results.json")
    out.write_text(json.dumps({"results": results}, indent=2) + "\n")
    print(json.dumps({"output": str(out), "results": results}, indent=2))
