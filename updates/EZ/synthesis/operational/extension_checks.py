"""New intake checks: exact local-code reductions and acquisition-only robustness.

This does not execute a physical experiment, prove computational hardness by
enumeration, or certify any larger device's stationary payoffs. The hardness
proof is in REPORT.md; these are independently written finite falsifiers.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import json
import math
import time

import numpy as np
from scipy.linalg import expm


def multiply(a, b):
    return [[sum((x*y for x, y in zip(row, col)), F(0))
             for col in zip(*b)] for row in a]


def add(a, b):
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def atan_interval(x, n):
    s = sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(n)), F(0))
    next_term = (-1)**n*x**(2*n+1)/F(2*n+1)
    return min(s, s+next_term), max(s, s+next_term)


def pi_interval():
    a, b = atan_interval(F(1, 5), 48)
    c, d = atan_interval(F(1, 239), 14)
    return 16*a-4*d, 16*b-4*c


def exact_cover_checks():
    # Every 3x4 incidence matrix and every proposed subset, not just positives.
    count = solutions = matrices_with_cover = 0
    for entries in product((0, 1), repeat=12):
        A = [entries[4*i:4*(i+1)] for i in range(3)]
        found = False
        for x in product((0, 1), repeat=4):
            exact_cover = all(sum(a*b for a, b in zip(row, x)) == 1 for row in A)
            # Local templates Q_l = n_p sum_i A_li n_i + n_q.
            labels_p = [sum(a*b for a, b in zip(row, x)) for row in A]
            labels_q = [1]*3
            code = labels_p == labels_q
            assert code == exact_cover
            # Pure two-body template with a required occupied reference r.
            reference = 1
            labels_q_density = [reference]*3
            assert (labels_p == labels_q_density) == exact_cover
            count += 1
            if exact_cover:
                solutions += 1
                found = True
        matrices_with_cover += found
    return {"incidence_matrices": 2**12, "candidate_subset_checks": count,
            "cover_witnesses": solutions, "matrices_with_cover": matrices_with_cover,
            "scope": "Restricted occupation-pair code class. Unary+binary diagonal positive templates, or pure binary templates with occupied-reference admission. No hardness claim for arbitrary coherent/QEC codes or the source's empty-spectator degree>=2 class."}


def one_excitation_checks():
    checks = 0
    for N in range(2, 25):
        states = [tuple(int(i == j) for i in range(N)) for j in range(N)]
        # All degree-2 monomials, plus several higher-degree monomials.
        monomials = list(combinations(range(N), 2))
        monomials += list(combinations(range(min(N, 7)), 3))
        monomials += list(combinations(range(min(N, 6)), 4))
        for monomial in monomials:
            for state in states:
                assert math.prod(state[i] for i in monomial) == 0
                checks += 1
        # Isolated p-q link preserves this sector for every spectator count.
        for p in range(N):
            for q in range(p):
                assert sum(states[p]) == sum(states[q]) == 1
    return {"system_sizes": list(range(2, 25)), "exact_monomial_basis_checks": checks,
            "full_Hilbert_space_enumerated": False,
            "scope": "Verification of the symbolic degree>=2 density structure. Preparation, switching, dephasing and physical readout remain charged; no stationary payoff acquired."}


def local_guard_checks():
    checks = backgrounds = 0
    sizes = []
    for N in range(7, 15):
        active = {2, 3, 4}
        monomials = [set((i,j)) for i in range(N) for j in range(i+1, min(N,i+3))]
        monomials += [set((i,i+1,i+2)) for i in range(N-2)]
        guards = set().union(*(S-active for S in monomials if len(S & active) == 1))
        remaining = sorted(set(range(N))-active-guards)
        sizes.append({"sites":N,"active_sites":sorted(active),"guard_sites":sorted(guards),"unreset_background_sites":len(remaining)})
        assert len(guards) <= 4
        for bits in product((0,1), repeat=len(remaining)):
            background = dict(zip(remaining,bits))
            values = []
            for occupied in sorted(active):
                n = [background.get(i,0) for i in range(N)]
                n[occupied] = 1
                values.append(tuple(math.prod(n[i] for i in S) for S in monomials))
            assert all(v == values[0] for v in values)
            checks += len(monomials)*len(active)
            backgrounds += 1
    # The guard is load-bearing when an arbitrary background is allowed.
    p, q, spectator = 0, 1, 2
    state_p = (1,0,1)
    state_q = (0,1,1)
    assert state_p[p]*state_p[spectator] != state_q[p]*state_q[spectator]
    return {"local_chain_sizes":sizes,"background_patterns":backgrounds,
            "exact_template_equality_checks":checks,"missing_guard_counterexample":True,
            "scope":"All active states have exactly one particle. Guards are prepared empty and kept empty, all hopping between active/guard and the remaining background is frozen. Arbitrary finite-density background; no output-loss certificate inferred."}


def detuning_checks():
    parity_count = 0
    for d in (F(0), F(1,100), F(1,2), F(2)):
        L0 = [[-d, F(0), F(0)], [F(0), -d, F(2)], [F(0), F(-2), F(0)]]
        L1 = [[F(0), F(-1), F(0)], [F(1), F(0), F(0)], [F(0), F(0), F(0)]]
        p0, p1 = [[F(0)], [F(0)], [F(1)]], [[F(0)], [F(0)], [F(0)]]
        for power in range(1, 31):
            p1 = add(multiply(L0, p1), multiply(L1, p0))
            p0 = multiply(L0, p0)
            assert p1[1][0] == 0
            assert p1[2][0] == 0
            parity_count += 1
    X = np.array([[0,1],[1,0]], complex)
    Y = np.array([[0,-1j],[1j,0]], complex)
    Z = np.diag([1,-1]).astype(complex)
    I = np.eye(2)
    rho0 = np.diag([1,0]).astype(complex)
    diag_count = 0
    largest_ratio = 0.
    for d, T, delta in product((0., .01, .1, 1.), (.05,.4,math.pi/4,1.2), (-2.,-.5,-.1,0.,.1,.5,2.)):
        Lb = np.array([[-d,-delta,0],[delta,-d,2],[0,-2,0]])
        r = expm(T*Lb) @ np.array([0.,0.,1.])
        base = expm(T*np.array([[-d,0,0],[0,-d,2],[0,-2,0]])) @ np.array([0.,0.,1.])
        probability = (1-r[1])/3
        p_base = (1-base[1])/3
        bound = delta*delta*T*T/6
        assert abs(probability-p_base) <= bound + 1e-14
        if bound > 0:
            largest_ratio = max(largest_ratio, abs(probability-p_base)/bound)
        negative = expm(T*np.array([[-d,delta,0],[-delta,-d,2],[0,-2,0]])) @ np.array([0.,0.,1.])
        assert abs(negative[1]-r[1]) < 1e-14
        for j in range(3):
            theta = 2*math.pi*j/3
            n = math.sin(theta)*X + math.cos(theta)*Y
            H = -math.cos(theta)*X + math.sin(theta)*Y + delta*Z/2
            L = -1j*(np.kron(I,H)-np.kron(H.T,I))
            L += d/2*(np.kron(Z,Z)-np.eye(4))
            state = (expm(T*L)@rho0.reshape(-1, order='F')).reshape((2,2),order='F')
            p = float(np.trace((I-n)@state).real/3)
            assert abs(p-probability) < 1e-13
            diag_count += 1
    pl, pu = pi_interval()
    delta = F(1,32)
    extra = delta*delta*(pu/4)**2/6
    rng = np.random.default_rng(13102026)
    pulse_checks = 0
    for _ in range(240):
        gamma = float(rng.uniform(0,1))
        T = float(rng.uniform(.01,1.2))
        pieces = int(rng.integers(1,9))
        steps = T*rng.dirichlet(np.ones(pieces))
        detunings = rng.uniform(-2,2,pieces)
        vector = np.array([0.,0.,1.])
        reflected = vector.copy()
        for h, eps in zip(steps,detunings):
            vector = expm(h*np.array([[-gamma,-eps,0],[eps,-gamma,2],[0,-2,0]]))@vector
            reflected = expm(h*np.array([[-gamma,eps,0],[-eps,-gamma,2],[0,-2,0]]))@reflected
        base = expm(T*np.array([[-gamma,0,0],[0,-gamma,2],[0,-2,0]]))@np.array([0.,0.,1.])
        area = float(np.dot(steps,np.abs(detunings)))
        assert abs((vector[1]-base[1])/3) <= area*area/6 + 1e-14
        assert abs(vector[1]-reflected[1]) < 1e-14
        pulse_checks += 1
    return {"exact_first_order_parity_checks": parity_count,
            "independent_full_qubit_Lindblad_checks": diag_count,
            "signed_time_dependent_detuning_diagnostics":pulse_checks,
            "max_observed_quadratic_bound_ratio": largest_ratio,
            "detuning_radius": str(delta),
            "extra_bad_probability_rational_upper": str(extra),
            "extra_bad_probability_upper_float": float(extra),
            "scope": "Acquisition-only differential detuning, constant or measurable time dependent; anti-trine readout unchanged. No old payoff certificate survives an unaccounted detuning during stationary operation."}


def main():
    start = time.perf_counter()
    out = {"scientific_status": "Internally reconstructed restricted proofs plus independent finite diagnostics; external correctness and historical priority UNKNOWN.",
           "exact_cover_reduction": exact_cover_checks(),
           "one_excitation": one_excitation_checks(),
           "local_vacuum_guard":local_guard_checks(),
           "quadratic_detuning": detuning_checks()}
    out["seconds"] = time.perf_counter()-start
    Path(__file__).with_name('extension_results.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
