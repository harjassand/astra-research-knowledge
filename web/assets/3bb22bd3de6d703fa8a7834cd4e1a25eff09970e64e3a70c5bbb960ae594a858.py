#!/usr/bin/env python3
"""Finite exact diagnostics; these are not formal or external validation.

Implemented after authorized candidate exposure. The independently frozen
orthogonality baseline is never rewritten by this file.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, log, log2
from pathlib import Path
import hashlib
import json
import random

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASELINE = ROOT / "work/agents/complexity_proof_recon/cycle04_memory_blind/INDEPENDENT_BASELINE.txt"
CANDIDATE = ROOT / "work/agents/foundational_transfer_sol/cycle04_transfers/TRANSFER_PROOFS.txt"
EXPECTED_BASELINE = "342987893f1a0101d905afa6f35b0a3de067cfae431a208495dd034f6780ff55"
EXPECTED_CANDIDATE = "de2fa4f741505a52fc5d11b147dfa22e24596fc6692d46542e187502ecdd212c"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dot(x, y):
    return (x & y).bit_count() & 1


def span(basis):
    result = {0}
    for x in basis:
        result |= {v ^ x for v in tuple(result)}
    return result


def dimension(vectors):
    pivots = {}
    for x in vectors:
        while x:
            p = x.bit_length() - 1
            if p not in pivots:
                pivots[p] = x
                break
            x ^= pivots[p]
    return len(pivots)


def entropy_bits(probs):
    return -sum(float(p) * log2(float(p)) for p in probs if p)


def h2(p):
    if p in (0, 1):
        return 0.0
    return -p * log2(p) - (1-p) * log2(1-p)


def orthogonality_checks():
    checks = []
    for m in range(3, 9):
        N, d = 2**m-1, 2**(m-1)-1
        rows = [sum(1 << (y-1) for y in range(1, N+1) if not dot(x, y))
                for x in range(1, N+1)]
        assert all(row.bit_count() == d for row in rows)
        c, a = 2**(m-2)-1, 2**(m-2)
        assert all((rows[x] & rows[z]).bit_count() == (d if x == z else c)
                   for x in range(N) for z in range(N))
        assert d*d == a+c*N
        assert F(N, d) < 4
        assert F(a, d*d) <= F(2, 9)
        rec = {"m": m, "N": N, "d": d,
               "capacity_nats_numeric": log(N/d),
               "two_step_Doeblin_beta_exact": str(F(a, d*d)),
               "gram_identity": "PASS"}
        if m <= 4:
            allmask = (1 << N)-1
            intersections = [allmask] * (1 << N)
            maximum = 0
            for mask in range(1, 1 << N):
                lowbit = mask & -mask
                intersections[mask] = intersections[mask ^ lowbit] & rows[lowbit.bit_length()-1]
                maximum = max(maximum, mask.bit_count()*intersections[mask].bit_count())
            B = (2**(m//2)-1)*(2**((m+1)//2)-1)
            assert maximum == B
            rec.update(exhaustive_rectangle_maximum=maximum,
                       row_support_subsets_checked=(1 << N)-1)
        if m <= 6:
            r = m//2
            subspaces = {tuple(sorted(span(basis)))
                         for basis in combinations(range(1, N+1), r)
                         if dimension(basis) == r}
            incidences = Counter()
            B = (2**r-1)*(2**(m-r)-1)
            for U in subspaces:
                xs = [x for x in U if x]
                ys = [y for y in range(1, N+1) if all(not dot(x, y) for x in U)]
                assert len(xs)*len(ys) == B
                incidences.update(product(xs, ys))
            assert len(incidences) == N*d
            assert len(set(incidences.values())) == 1
            assert sum(incidences.values()) == len(subspaces)*B
            rec.update(subspaces_enumerated=len(subspaces),
                       Wyner_witness_edge_incidence=int(next(iter(incidences.values()))),
                       Wyner_witness_uniformity="PASS")
        checks.append(rec)
    return checks


def parity_entropy_checks():
    rng = random.Random(41003)
    count = 0
    for m in range(3, 7):
        V = list(range(1, 2**m))
        N = len(V)
        for r in range(1, m):
            U = [x for x in V if x < 2**r]
            W = [y for y in V if y % 2**r == 0]
            for noise_a, noise_b in product([F(0), F(1,100), F(1,20), F(1,5)], repeat=2):
                wa = [rng.randrange(1, 8) for _ in U]
                wb = [rng.randrange(1, 8) for _ in W]
                a0 = dict(zip(U, [F(v, sum(wa)) for v in wa]))
                b0 = dict(zip(W, [F(v, sum(wb)) for v in wb]))
                a = {x: (1-noise_a)*a0.get(x, 0)+noise_a/N for x in V}
                b = {y: (1-noise_b)*b0.get(y, 0)+noise_b/N for y in V}
                bad = {y: sum(a[x] for x in V if dot(x, y)) for y in V}
                eta = F(1,20)
                G = [y for y in V if bad[y] <= eta]
                tau = sum(b[y] for y in V if y not in G)
                e = sum(b[y]*bad[y] for y in V)
                assert tau <= e/eta
                rank = dimension(G)
                actual = entropy_bits(a.values())+entropy_bits(b.values())
                h = h2(float(eta))
                rhs = (1+h+(1-h)*float(tau))*m+(1-h)*h2(float(tau))
                assert actual <= rhs+1e-10, (m, r, noise_a, noise_b, actual, rhs, rank)
                count += 1
    delta, eta = .01, .05
    alpha = 1-2*delta-h2(eta)-(1-h2(eta))*delta/eta
    constant = 2+h2(delta)+(1-h2(eta))*h2(delta/eta)
    assert alpha > .54 and constant < 4
    assert all(alpha*m-constant >= m/2-4 for m in range(3, 1001))
    return {"seeded_product_components_checked": count,
            "floating_entropy_diagnostic_only": True,
            "alpha_at_0_01": alpha, "constant_at_0_01": constant,
            "clean_bound_checked_m_3_to_1000": "PASS"}


def incidence_checks():
    checks = []
    for N in [8, 16, 32, 64, 128]:
        M = comb(N, N//2)
        max_rectangle = max(t*comb(N-t, N//2-t) for t in range(1, N//2+1))
        assert max_rectangle == M//2
        for t in range(1, N//2+1):
            assert M >= 2**t*comb(N-t, N//2-t)
            assert 2**(t-1) >= t
        diagonal, off = M//2, comb(N-2, N//2-2)
        assert diagonal-off == M*N//(4*(N-1))
        assert diagonal > off
        rec = {"N": N, "M": M,
               "maximum_incidence_rectangle": max_rectangle,
               "Gram_positive_diagonal_increment": diagonal-off,
               "exact_full_pair_matrix_rank": N+2,
               "Wyner_lower_ratio_exact": N}
        if N <= 16:
            subsets = [sum(1 << i for i in S) for S in combinations(range(N), N//2)]
            code = []
            for S in subsets:
                if all((S ^ T).bit_count() >= N//4 for T in code):
                    code.append(S)
            assert len(code) >= 2**(N*(1-h2(.25)))/(N+1)
            rec.update(greedy_code_size=len(code),
                       greedy_pairwise_separation="PASS")
        checks.append(rec)
    return checks


def advance(law, kernel):
    result = defaultdict(F)
    for (word, state), p in law.items():
        for symbol, target, q in kernel[state]:
            result[word+(symbol,), target] += p*q
    return dict(result)


def output_marginal(law):
    result = defaultdict(F)
    for (word, state), p in law.items():
        result[word] += p
    return dict(result)


def balanced_stationarity_checks():
    N = 8
    subsets = [sum(1 << i for i in S) for S in combinations(range(N), N//2)]
    M = len(subsets)
    blank = ("B", 0)
    edge = {"init": [(("S", S), ("i", i), F(2, M*N))
                     for S in subsets for i in range(N) if S >> i & 1],
            "done": [(blank, "init", F(1))]}
    edge.update({("i", i): [(("i", i), "done", F(1))] for i in range(N)})
    pi_edge = {"init": F(1,3), "done": F(1,3)}
    pi_edge.update({("i", i): F(1, 3*N) for i in range(N)})
    moore = {"blank": [(blank, ("Sphase", i), F(1,N)) for i in range(N)]}
    for i in range(N):
        moore[("Sphase", i)] = [(("S", S), ("iphase", i), F(2,M))
                                for S in subsets if S >> i & 1]
        moore[("iphase", i)] = [(("i", i), "blank", F(1))]
    pi_moore = {"blank": F(1,3)}
    pi_moore.update({(phase, i): F(1,3*N)
                    for phase in ["Sphase", "iphase"] for i in range(N)})
    for kernel, pi in [(edge, pi_edge), (moore, pi_moore)]:
        assert all(sum(q for a, z, q in kernel[state]) == 1 for state in kernel)
        stationary = defaultdict(F)
        for state, p in pi.items():
            for a, target, q in kernel[state]:
                stationary[target] += p*q
        assert dict(stationary) == pi
    law_edge = {((), state): p for state, p in pi_edge.items()}
    law_moore = {((), state): p for state, p in pi_moore.items()}
    sizes = []
    for n in range(1,5):
        law_edge, law_moore = advance(law_edge, edge), advance(law_moore, moore)
        p, q = output_marginal(law_edge), output_marginal(law_moore)
        assert p == q and sum(p.values()) == 1
        sizes.append({"horizon": n, "nonzero_words": len(p)})
    assert abs(entropy_bits(pi_edge.values())-(log2(3)+log2(N)/3)) < 1e-10
    assert abs(entropy_bits(pi_moore.values())-(log2(3)+2*log2(N)/3)) < 1e-10
    return {"N": N, "edge_states": len(edge), "Moore_states": len(moore),
            "stationarity_exact": "PASS", "same_output_laws_exact": sizes,
            "entropy_bits_numeric_edge": entropy_bits(pi_edge.values()),
            "entropy_bits_numeric_Moore": entropy_bits(pi_moore.values())}


def simulator_hybrid_checks():
    # Noncommuting two-state prepare-and-measure instrument: tau_a have x Bloch
    # coordinate +/-1/10, z coordinate +/-1/2. Gamma dephases z, error 1/20.
    # L_a measures x then prepares tau_a. Gamma(tau_a) is outside the original
    # finite reachable family; the audited hybrid still uses only tau_a.
    epsilon = F(1,20)
    output = []
    for n in range(1,11):
        words = list(product([0,1], repeat=n))
        prefix = {}
        for word in words:
            p = F(1)
            current = 0
            seq = [p]
            for symbol in word:
                p0 = F(1,2)+(epsilon if current == 0 else -epsilon)
                p *= p0 if symbol == 0 else 1-p0
                current = symbol
                seq.append(p)
            prefix[word] = seq
        hybrids = [{word: prefix[word][j]*F(1,2**(n-j)) for word in words}
                   for j in range(n+1)]
        assert all(sum(h.values()) == 1 for h in hybrids)
        distances = [sum(abs(hybrids[j][w]-hybrids[j+1][w]) for w in words)/2
                     for j in range(n)]
        assert all(distance == epsilon for distance in distances)
        final_tv = sum(abs(hybrids[0][w]-hybrids[n][w]) for w in words)/2
        assert final_tv <= n*epsilon
        output.append({"horizon": n, "TV_exact": str(final_tv),
                       "adjacent_hybrid_TV_exact": str(epsilon),
                       "bound_exact": str(n*epsilon)})
    return {"Gamma_reachable_states_not_in_original_family": True,
            "statewise_epsilon_exact": str(epsilon), "checks": output}


def main():
    assert sha(BASELINE) == EXPECTED_BASELINE
    assert sha(CANDIDATE) == EXPECTED_CANDIDATE
    report = {"status": "PASS_FINITE_DIAGNOSTICS_ONLY",
              "baseline_sha256": sha(BASELINE), "candidate_sha256": sha(CANDIDATE),
              "implemented_after_authorized_exposure": True,
              "orthogonality": orthogonality_checks(),
              "parity_entropy": parity_entropy_checks(),
              "balanced_incidence": incidence_checks(),
              "balanced_stationary_models": balanced_stationarity_checks(),
              "supplied_simulator_hybrids": simulator_hybrid_checks(),
              "formal_validation": "NOT_RUN", "external_validation": "NOT_OBTAINED"}
    (HERE / "checks.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"],
                      "parity_components": report["parity_entropy"]["seeded_product_components_checked"],
                      "output": str(HERE / "checks.json")}, indent=2))


if __name__ == "__main__":
    main()
