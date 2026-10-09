"""Exact finite interface diagnostics, not a verifier of quantified claims."""
from fractions import Fraction as F
from itertools import combinations, product
from collections import defaultdict
from math import comb, log
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent
PROOF_HASH = "de2fa4f741505a52fc5d11b147dfa22e24596fc6692d46542e187502ecdd212c"


def tv(p, q):
    return sum(abs(p.get(k, F(0)) - q.get(k, F(0))) for k in p.keys() | q.keys()) / 2


def entropy(p):
    return -sum(float(x) * log(float(x)) for x in p.values() if x)


def marginal(p, j):
    out = defaultdict(F)
    for k, v in p.items():
        out[k[j]] += v
    return dict(out)


def stationary_example(n):
    subsets = [frozenset(s) for s in combinations(range(n), n // 2)]
    m = len(subsets)
    a_s = [('S', tuple(sorted(s))) for s in subsets]
    a_i = [('i', i) for i in range(n)]
    blank = ('blank',)
    init, done = ('init',), ('done',)
    hidden = [init] + a_i + [done]
    pi = {init: F(1, 3), done: F(1, 3)} | {i: F(1, 3*n) for i in a_i}
    kernel = {}
    for a, s in zip(a_s, subsets):
        for i in s:
            kernel[(a, ('i', i), init)] = F(2, m*n)
    for i in a_i:
        kernel[(i, done, i)] = F(1)
    kernel[(blank, init, done)] = F(1)
    for z in hidden:
        assert sum(v for (a, zn, zp), v in kernel.items() if zp == z) == 1
    pi_next = defaultdict(F)
    for (a, zn, zp), v in kernel.items():
        pi_next[zn] += pi[zp] * v
    assert dict(pi_next) == pi
    two = defaultdict(F)
    two_hidden = defaultdict(F)
    outgoing = defaultdict(list)
    for (a, zn, zp), t in kernel.items():
        outgoing[zp].append((a, zn, t))
    for (a, w, z0), t1 in kernel.items():
        for b, z2, t2 in outgoing[w]:
            weight = pi[z0] * t1 * t2
            two[(a, b)] += weight
            two_hidden[(a, b, w)] += weight
    two = dict(two)
    assert sum(two.values()) == 1
    p1, p2 = marginal(two, 0), marginal(two, 1)
    assert p1 == p2
    for a, s in zip(a_s, subsets):
        assert p1[a] == F(1, 3*m)
        for i in range(n):
            conditional = two.get((a, ('i', i)), F(0)) / p1[a]
            assert conditional == (F(2, n) if i in s else F(0))
    assert abs(entropy(pi) - (log(3) + log(n)/3)) < 1e-12
    mi = entropy(p1) + entropy(p2) - entropy(two)
    assert abs(mi - (log(3) + log(2)/3)) < 1e-12
    # These scalar exact inequalities are the support-count gate of B3a.
    rectangle_ratios = []
    for t in range(1, n//2 + 1):
        ratio = F(m*n, 2*t*comb(n-t, n//2-t))
        assert ratio >= n
        rectangle_ratios.append(str(ratio))
    assert rectangle_ratios[0] == str(n)
    # All target/center likelihood ratios are exactly 4 on support.
    center = {init: F(1, 4), done: F(1, 4)} | {i: F(1, 2*n) for i in a_i}
    for s in subsets:
        assert all(F(2, n) / center[('i', i)] == 4 for i in s)
    assert F(1) / center[init] == F(1) / center[done] == 4
    average = {init: F(1, 4), done: F(1, 4)} | {i: F(0) for i in a_i}
    for s in subsets:
        for i in s:
            average[('i', i)] += F(1, 2*m) * F(2, n)
    assert average == center
    # Nontrivial perturbation plus a zero-row case exercise conditional TV.
    independent = {(a, blank): pa for a, pa in p1.items()}
    for mix in (F(1, 100), F(1, 2), F(1)):
        q = {k: (1-mix)*two.get(k, F(0))+mix*independent.get(k, F(0))
             for k in two.keys() | independent.keys()}
        check_conditional(two, q, a_s)
    check_conditional(two, {(blank, blank): F(1)}, a_s)
    # Truncation gate checked at eta=.8 to actually discard the middle phase.
    h, eta = entropy(pi), 0.8
    keep = {w for w, pw in pi.items() if -log(float(pw)) <= h/eta}
    tail_mass = sum(pw for w, pw in pi.items() if w not in keep)
    assert float(tail_mass) <= eta
    assert len(keep) <= __import__('math').exp(h/eta)
    q_trunc = defaultdict(F)
    tail_past = defaultdict(F)
    for (a, b, w), v in two_hidden.items():
        if w in keep:
            q_trunc[(a, b)] += v
        else:
            tail_past[a] += v
    for a, v in tail_past.items():
        q_trunc[(a, blank)] += v
    trunc_tv = tv(two, dict(q_trunc))
    assert trunc_tv <= tail_mass
    return {"N": n, "subset_outputs": m, "total_outputs": m+n+1,
            "TP_and_stationarity": True, "center_ratios_exact": 4,
            "capacity_all_priors_analytic": "ln 4",
            "basis_hidden_entropy": entropy(pi), "two_output_MI": mi,
            "rectangle_ratios": rectangle_ratios,
            "truncation_tail": str(tail_mass), "truncation_TV": str(trunc_tv)}


def check_conditional(p, q, subset_labels):
    p1, q1 = marginal(p, 0), marginal(q, 0)
    p_rows, q_rows = defaultdict(dict), defaultdict(dict)
    for (a, b), v in p.items():
        if v:
            p_rows[a][b] = v
    for (a, b), v in q.items():
        if v:
            q_rows[a][b] = v
    lhs = F(0)
    for a in subset_labels:
        pp = {b: v/p1[a] for b, v in p_rows[a].items()}
        if q1.get(a, F(0)):
            qq = {b: v/q1[a] for b, v in q_rows[a].items()}
        else:
            qq = {('blank',): F(1)}
        lhs += p1[a] * tv(pp, qq)
    assert lhs <= tv(p, q) + tv(p1, q1)
    assert lhs <= 2*tv(p, q)


def matrix_trace_product(a, b):
    return sum(a[i][j]*b[j][i] for i in range(2) for j in range(2))


def quantum_reset_example():
    # Original memory stays in {rho0,rho1}; Gamma's prepared basis states
    # and Gamma(rho0)=I/2 leave that family. This tests the hybrid gate.
    rho = [((F(1, 2), F(1, 8)), (F(1, 8), F(1, 2))),
           ((F(3, 4), F(0)), (F(0), F(1, 4)))]
    effects = [((F(1, 2), F(1, 4)), (F(1, 4), F(1, 2))),
               ((F(1, 2), -F(1, 4)), (-F(1, 4), F(1, 2)))]
    states_z = [((F(1), F(0)), (F(0), F(0))),
                ((F(0), F(0)), (F(0), F(1)))]
    kernel = {(a, zn, zp): matrix_trace_product(effects[a], states_z[zp])*rho[a][zn][zn]
              for a, zn, zp in product(range(2), repeat=3)}
    for zp in range(2):
        assert sum(v for (a, zn, z), v in kernel.items() if z == zp) == 1
    epsilon = F(1, 8)
    rows = []
    for n in range(1, 8):
        p, q = {}, {}
        for word in product(range(2), repeat=n):
            state, pp = rho[0], F(1)
            classical = {0: F(1, 2), 1: F(1, 2)}
            for a in word:
                pp *= matrix_trace_product(effects[a], state)
                state = rho[a]
                classical = {zn: sum(classical[zp]*kernel[(a, zn, zp)] for zp in range(2))
                             for zn in range(2)}
            p[word], q[word] = pp, sum(classical.values())
            assert q[word] == F(1, 2**n)
        assert sum(p.values()) == sum(q.values()) == 1
        dist = tv(p, q)
        assert dist <= n*epsilon
        rows.append({"horizon": n, "TV_exact": str(dist), "bound": str(n*epsilon)})
    return {"original_reachable_family_size": 2,
            "reset_states_leave_original_family": True, "rows": rows}


def main():
    assert hashlib.sha256((BASE/'TRANSFER_PROOFS.txt').read_bytes()).hexdigest() == PROOF_HASH
    result = {"status": "FINITE_INTERFACE_CHECKS_PASS",
              "scope": "Exact finite factors and examples; NOT a formal theorem verifier.",
              "proof_sha256": PROOF_HASH,
              "stationary_examples": [stationary_example(8), stationary_example(16)],
              "quantum_reset": quantum_reset_example()}
    (BASE/'diagnostics.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({"status": result['status'], "N": [8, 16], "horizons": 7,
                      "proof_sha256": PROOF_HASH, "universal_quantifiers_verified": False}))


if __name__ == '__main__':
    main()
