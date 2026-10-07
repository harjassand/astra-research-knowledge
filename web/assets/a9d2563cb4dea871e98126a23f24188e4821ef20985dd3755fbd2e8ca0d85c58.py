#!/usr/bin/env python3
"""Exact factorized n=12 counterexample to local moves plus global complement."""
from fractions import Fraction
from itertools import combinations, permutations
import json
from pathlib import Path
import sys

N = 6
O = (1, 3, 5)
E = (0, 2, 4)

def sign(p):
    return -1 if sum(p[a] > p[b] for a in range(3) for b in range(a + 1, 3)) % 2 else 1

def det3(a):
    return sum((Fraction(sign(p)) * a[0][p[0]] * a[1][p[1]] * a[2][p[2]] for p in permutations(range(3))), Fraction(0))

def fstr(x):
    return f"{x.numerator}/{x.denominator}"

def run(bits):
    eps = Fraction(1, 2**bits)
    F = [[Fraction(0) for _ in range(N)] for _ in range(N)]
    for i in range(N):
        F[i][(i + 1) % N] = 1
        F[i][(i - 1) % N] = eps
    states = list(combinations(range(N), 3))
    amp, weight = {}, {}
    for I in states:
        J = tuple(j for j in range(N) if j not in I)
        amp[I] = det3([[F[i][j] for j in J] for i in I])
        weight[I] = amp[I] ** 2
    support = [I for I in states if weight[I] > 0]
    Z6 = sum((weight[I] for I in states), Fraction(0))
    a = weight[O]
    assert weight[E] == a == (1 + eps**3) ** 2
    assert Z6 == 2 * a + 6 * eps**2 + 6 * eps**4

    # Two block-diagonal 6-cycles, fixed total rank k=6. A nonzero minor
    # must choose exactly 3 row-lines in each block, so the microstates factor.
    Z12 = Z6**2
    S_mass = 2 * a**2 / Z12  # states (O,O) and (E,E)
    assert S_mass < Fraction(1, 2)

    # There are 36 global one-line exchange proposals from a basis: 18
    # cross-block moves have zero determinant; each block contributes the
    # n=6 neighbor weights (3 eps^2 + 3 eps^4).
    phi_local = (eps**2 + eps**4) / (6 * a)
    # M_local is the symmetric 1/36 proposal Metropolis chain.
    # R_global complements the whole 12-site configuration; it preserves S.
    # Q=(M_local+R_global)/2. Pair kernel P=(Swap+Q_A+Q_B)/3.
    global_Q_conductance = phi_local / 2
    pair_cut_mass = S_mass**2
    pair_cut_conductance = phi_local / 3
    blockwise_Q_exit = (1 + phi_local) / 2
    assert pair_cut_mass < Fraction(1, 2)
    pair_energy = S_mass * phi_local / 3
    variance_f = S_mass * (1 - S_mass)
    required_L = variance_f / pair_energy

    # Check exact support, complement invariance of S, and all 6x6 minor groups.
    product_support = [(I, J) for I in support for J in support]
    assert len(product_support) == 14**2
    def is_in_S(I, J):
        return (I, J) in ((O, O), (E, E))
    for I, J in product_support:
        Ibar = tuple(sorted(set(range(N)) - set(I)))
        Jbar = tuple(sorted(set(range(N)) - set(J)))
        assert is_in_S(I, J) == is_in_S(Ibar, Jbar)

    # Any within-block one-exchange neighbor of a mode has amplitude <= eps;
    # a cross-block exchange has an unequal row/column count and determinant 0.
    O_neighbors = []
    for removed in O:
        for added in E:
            T = tuple(sorted((set(O) - {removed}) | {added}))
            O_neighbors.append(amp[T])
    assert sorted(O_neighbors) == sorted([Fraction(0)] * 3 + [eps] * 3 + [eps**2] * 3)

    return {
        "b": bits,
        "epsilon": fstr(eps),
        "block_partition_Z6": fstr(Z6),
        "two_block_partition_Z12": fstr(Z12),
        "positive_microstates": len(product_support),
        "even_mode_cut_mass": fstr(S_mass),
        "even_mode_cut_mass_decimal": float(S_mass),
        "single_replica_local_exit_from_cut": fstr(phi_local),
        "global_complement_chain_conductance": fstr(global_Q_conductance),
        "pair_cut_mass_S_squared": fstr(pair_cut_mass),
        "pair_cut_conductance_S_squared": fstr(pair_cut_conductance),
        "blockwise_complement_chain_exit_from_S": fstr(blockwise_Q_exit),
        "global_complement_preserves_cut": True,
        "pair_additive_variance_exact": fstr(variance_f),
        "pair_additive_dirichlet_exact": fstr(pair_energy),
        "required_energy_constant_exact": fstr(required_L),
        "required_energy_constant_decimal": float(required_L),
    }

if __name__ == "__main__":
    values = [run(int(x)) for x in (sys.argv[1:] or [4, 8, 16])]
    out = Path(__file__).with_name("global_complement_counter_results.json")
    out.write_text(json.dumps({"results": values}, indent=2) + "\n")
    print(json.dumps({"output": str(out), "results": values}, indent=2))
