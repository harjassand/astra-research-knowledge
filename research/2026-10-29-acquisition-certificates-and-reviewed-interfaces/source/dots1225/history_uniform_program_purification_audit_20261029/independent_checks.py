"""Independent exact checks of the history-envelope / capped-restart theorem.

The source snapshot is read-only input. Run this file with Python 3 + SymPy.
No quantum device is simulated; these are finite rational CP/instrument checks.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import hashlib
import json
import numpy as np
import sympy as s

HERE = Path(__file__).resolve().parent


def exterior_check():
    """Construct projector columns before reducing to dark-occupation sectors.

    On each total-label block U, P=ss^T/(k+1), with s the wedge signs.
    Build (I-P)|I,j> explicitly and trace the new register. Checking x=0
    and x=1/9 proves the affine-in-x instrument identity on the whole line.
    """
    column_checks = 0
    sector_checks = 0
    for k in range(1, 8):
        old = list(combinations(range(9), k))
        nxt = list(combinations(range(9), k + 1))
        # Distinct U have disjoint product-basis support; each normalized
        # wedge column has exactly k+1 entries of absolute value 1/sqrt(k+1).
        supports = set()
        for U in nxt:
            for j in U:
                ij = (tuple(l for l in U if l != j), j)
                assert ij not in supports
                supports.add(ij)
        assert len(supports) == (k + 1) * comb(9, k + 1)
        for x in [F(0), F(1, 9)]:
            a = (1 - x) / 8
            lam = [x] + [a] * 8
            for c in [0, 1]:
                selected = [I for I in old if int(0 in I) == c]
                succ = defaultdict(F)
                fail = defaultdict(F)
                for I in selected:
                    for j in range(9):
                        weight = lam[j] / len(selected)
                        if j in I:
                            amps = {(I, j): F(1)}
                            ps = F(0)
                        else:
                            U = tuple(sorted(I + (j,)))
                            sj = (-1) ** sum(i > j for i in I)
                            amps = {}
                            for l in U:
                                J = tuple(i for i in U if i != l)
                                sl = (-1) ** sum(i > l for i in J)
                                amps[J, l] = F(int(l == j)) - F(sj * sl, k + 1)
                            ps = F(1, k + 1)
                            succ[U] += weight * ps
                        assert sum(z * z for z in amps.values()) + ps == 1
                        column_checks += 1
                        # Partial trace is performed from amplitudes. Any
                        # same-new-label off-diagonal term would be retained.
                        for (J, l), z in amps.items():
                            for (K, m), w in amps.items():
                                if l == m:
                                    fail[J, K] += weight * z * w
                assert all(z == 0 for (J, K), z in fail.items() if J != K)
                Sgot = [sum(p for U, p in succ.items() if int(0 in U) == cc) for cc in [0, 1]]
                Fgot = [sum(p for (J, K), p in fail.items() if J == K and int(0 in J) == cc) for cc in [0, 1]]
                S = [[(8-k)*a/(k+1), F(0)], [x/(k+1), (9-k)*a/(k+1)]]
                f01, f10 = k*x/(k+1)**2, (9-k)*a/(k+1)**2
                FF = [[1-S[0][0]-S[1][0]-f01, f10], [f01, 1-S[1][1]-f10]]
                assert Sgot == [S[cc][c] for cc in [0, 1]]
                assert Fgot == [FF[cc][c] for cc in [0, 1]]
                # Stronger than occupation totals: each output sector is
                # exactly maximally mixed, preserving the claimed isotropy.
                for cc in [0, 1]:
                    us = [U for U in nxt if int(0 in U) == cc]
                    js = [J for J in old if int(0 in J) == cc]
                    if us:
                        assert all(succ[U] == Sgot[cc] / len(us) for U in us)
                    assert all(fail[J, J] == Fgot[cc] / len(js) for J in js)
                sector_checks += 1
    return {"dimension": 9, "exact_projector_column_checks": column_checks,
            "exact_input_sector_checks": sector_checks,
            "affine_basis_values_x": ["0", "1/9"],
            "all_two_sector_maps_and_sector_isotropy_match": True}


def scalar_proofs():
    x = s.symbols('x', real=True)
    a = (1-x)/8
    rows = []
    for k in range(1, 8):
        S = s.Matrix([[(8-k)*a/(k+1), 0], [x/(k+1), (9-k)*a/(k+1)]])
        f01, f10 = k*x/(k+1)**2, (9-k)*a/(k+1)**2
        FF = s.Matrix([[1-sum(S[:, 0])-f01, f10], [f01, 1-sum(S[:, 1])-f10]])
        det = s.factor(FF.det())
        # Independent positivity certificate: each determinant is concave
        # quadratic, so its minimum lies at an endpoint, not a sample grid.
        assert s.diff(det, x, 2) < 0
        assert det.subs(x, 0) > 0 and det.subs(x, s.Rational(1, 9)) > 0
        b = k*x/((9-k)*a+k*x)
        bp = (k+1)*x/((8-k)*a+(k+1)*x)
        z = s.Matrix([1-b, b])
        sv, fv = S*z, FF*z
        assert s.factor(sv[1]-bp*sum(sv)) == 0
        residual = s.factor(fv[1]-b*sum(fv))
        claimed = k*(9-k)*a*x*(x-a)/((k+1)*((9-k)*a+k*x)**2)
        assert s.factor(residual-claimed) == 0
        rows.append({"k": k, "failure_determinant": str(det),
                     "determinant_at_zero": str(det.subs(x, 0)),
                     "determinant_at_one_ninth": str(det.subs(x, s.Rational(1, 9))),
                     "strict_concavity": str(s.diff(det, x, 2))})
    return rows


def swap_check():
    u, v = s.symbols('u v', real=True)
    out = []
    for d in [2, 4, 9]:
        # Direct diagonal quantum states; P_sym rho P_sym followed by trace.
        # The i,i population is (rho_i+sigma_i+2rho_i sigma_i)/4.
        r = d-1
        rho = [1-u] + [u/r]*r
        sigma = [1-v] + [v/r]*r
        retained = [s.factor((ri+si+2*ri*si)/4) for ri, si in zip(rho, sigma)]
        p = s.factor(sum(retained))
        f = s.factor(sum(retained[1:])/p)
        assert s.factor(p-(1+(1-u)*(1-v)+u*v/r)/2) == 0
        expected = (u+v+2*u*v/r)/(4-2*(u+v)+2*d*u*v/r)
        assert s.factor(f-expected) == 0
        num, den = s.fraction(s.factor(s.diff(f, u)))
        # Derivative numerator depends only on v and is concave with positive
        # endpoints on [0,r/(r+1)]; denominator is a positive squared term.
        assert not num.has(u)
        assert s.diff(num, v, 2) < 0
        assert num.subs(v, 0) > 0 and num.subs(v, s.Rational(r, r+1)) > 0
        assert s.factor(s.diff(p, u)-(-1+s.Rational(d, r)*v)/2) == 0
        out.append({"d": d, "d_error_du": str(s.factor(s.diff(f, u))),
                    "derivative_numerator_endpoint_values": [str(num.subs(v, 0)), str(num.subs(v, s.Rational(r, r+1)))]})
    return out


def dense_swap_check():
    rng = np.random.default_rng(921507)
    worst = 0.0
    cases = 0
    for d in [2, 4, 9]:
        swap = np.zeros((d*d, d*d))
        for i in range(d):
            for j in range(d):
                swap[j*d+i, i*d+j] = 1
        sym = (np.eye(d*d)+swap)/2
        for fraction_u, fraction_v in [(0, 0), (0, .8), (.2, .7), (.97, .01), (1, 1)]:
            c = rng.normal(size=d)+1j*rng.normal(size=d)
            c /= np.linalg.norm(c)
            pc = np.outer(c, c.conj())
            u, v = fraction_u*(d-1)/d, fraction_v*(d-1)/d
            rho = (1-u)*pc+u/(d-1)*(np.eye(d)-pc)
            sigma = (1-v)*pc+v/(d-1)*(np.eye(d)-pc)
            actual = sym @ np.kron(rho, sigma) @ sym
            actual = np.trace(actual.reshape(d, d, d, d), axis1=1, axis2=3)
            p = (1+(1-u)*(1-v)+u*v/(d-1))/2
            f = (u+v+2*u*v/(d-1))/(4-2*(u+v)+2*d*u*v/(d-1))
            expected = p*((1-f)*pc+f/(d-1)*(np.eye(d)-pc))
            error = float(np.max(np.abs(actual-expected)))
            assert error < 3e-14
            worst = max(worst, error)
            cases += 1
    return {"seed": 921507, "unequal_input_dense_instrument_cases": cases,
            "maximum_entry_residual": worst}


def step(v, eta):
    x, a, q = eta/(8+eta), 1/(8+eta), (8+eta)/18
    w = defaultdict(F)
    completed = [F(0), F(0)]
    for (k, c), mass in v.items():
        if k == 8:
            w[k, c] += mass
            continue
        w[k, c] += mass*(1-q)
        if k == 0:
            w[1, 0] += mass*q*(1-x)
            w[1, 1] += mass*q*x
            continue
        f01, f10 = k*x/(k+1)**2, (9-k)*a/(k+1)**2
        if c == 0:
            S = [(8-k)*a/(k+1), x/(k+1)]
            FF = [1-sum(S)-f01, f01]
        else:
            S = [F(0), (9-k)*a/(k+1)]
            FF = [f10, 1-sum(S)-f10]
        for cc in [0, 1]:
            w[k+1, cc] += mass*q*S[cc]
            w[k, cc] += mass*q*FF[cc]
            if k == 7:
                completed[cc] += mass*q*S[cc]
    assert sum(w.values()) == 1
    return w, completed


def cap_checks():
    M0 = F(9, 4)*(1+sum((F(8*(k+1), 8-k) for k in range(1, 8)), F(0)))
    assert M0 == F(41481, 140)
    L = -(-(2*M0).numerator//(2*M0).denominator)
    out = []
    for eta in [F(0), F(1, 100), F(1, 2), F(99, 100)]:
        v = {(0, 0): F(1)}
        envelope = 8*eta/(1+8*eta)
        rows = []
        completed_time_checks = 0
        for n in range(1, L+1):
            v, completed = step(v, eta)
            pn = sum(completed)
            if pn:
                assert completed[1] <= envelope*pn
                completed_time_checks += 1
            if n in [8, 32, 128, L]:
                p = v.get((8, 0), F(0))+v.get((8, 1), F(0))
                z = v.get((8, 1), F(0))
                assert z <= envelope*p
                if n == 8:
                    assert z == envelope*p
                rows.append({"ordinary_call_cap": n, "readiness": float(p),
                             "conditional_infidelity": float(z/p) if p else None})
        p = v[(8, 0)]+v[(8, 1)]
        assert 1-p <= F(1, 2)
        assert (1-p)**7 <= F(1, 128)
        # On eight calls, only eight minus flags and seven successes can
        # finish, so the finite-time envelope is sharp (not just sufficient).
        assert abs(rows[0]['conditional_infidelity']-float(envelope)) < 1e-14
        out.append({"eta": str(eta), "uniform_error_bound": str(envelope),
                    "completion_time_conditioned_checks": completed_time_checks,
                    "cap_data": rows, "seven_fresh_attempt_abort_probability": float((1-p)**7)})
    return {"uniform_mean_call_bound": str(M0), "single_attempt_cap": L, "cases": out}


def schedule_checks():
    # Independent integer-grid recurrence: no imported author functions and
    # no floating-point decisions. A ceil quotient rounds outward exactly.
    def ceildiv(a, b):
        return (a+b-1)//b
    rows = json.loads((HERE/'source_snapshot'/'exact_schedule.json').read_text())
    for row in rows:
        eta, target = F(row['eta_upper']), F(row['target'])
        g = 1 << row['rounding_bits']
        E = ceildiv(8*eta.numerator*g, eta.denominator+8*eta.numerator)
        M = ceildiv(41481*g, 140)
        j = 0
        while E*target.denominator > target.numerator*g:
            dd = 16*g*g-16*E*g+9*E*E
            nE = ceildiv(g*E*(8*g+E), dd)
            nM = ceildiv(32*M*g*g, dd)
            assert 9*E < 8*g and nE < E
            E, M = nE, nM
            j += 1
        assert j == row['levels']
        assert F(E, g) == F(row['uniform_error_upper'])
        assert F(M, g) == F(row['expected_calls_upper'])
        assert ceildiv(2*M, g) == row['attempt_call_cap']
        assert row['total_call_cap'] == 7*row['attempt_call_cap']
    return {"exact_integer_schedule_cases_reproduced": len(rows), "all_fields_match": True}


def main():
    result = {"exterior_instrument": exterior_check(),
              "scalar_invariant_certificates": scalar_proofs(),
              "heterogeneous_swap": swap_check(),
              "dense_heterogeneous_swap": dense_swap_check(),
              "physical_source_call_caps": cap_checks(),
              "integer_schedules": schedule_checks(),
              "scope": "Exact mathematical IID-family checks; not a hardware run, arbitrary-memory theorem, or downstream gate/PBT receipt."}
    target = HERE/'INDEPENDENT_CHECKS.json'
    target.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
