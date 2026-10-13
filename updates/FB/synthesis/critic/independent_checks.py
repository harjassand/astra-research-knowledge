#!/usr/bin/env python3
"""Independent finite diagnostics for FB; no producer imports or outputs used.

Universal claims are supported by written proofs, never by this finite suite.
Run with work/research-venv/bin/python from any directory.  This script writes
only beside itself.  Energy units are those of the declared fixtures.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
import math
from itertools import product
import numpy as np
from scipy.linalg import eigh, expm
from scipy.special import logsumexp

OUT = Path(__file__).resolve().parent
PIN = "4025c5252f1ca992d3eae6ed422d6338ebe6c5a4"


def car(n):
    result = []
    for j in range(n):
        a = np.zeros((1 << n, 1 << n), complex)
        for b in range(1 << n):
            if (b >> j) & 1:
                a[b ^ (1 << j), b] = (-1) ** ((b & ((1 << j)-1)).bit_count())
        result.append(a)
    return result


def free_energy(h, beta):
    return -logsumexp(-beta * np.linalg.eigvalsh(h)) / beta


def onebody_impurity_energy(levels, kinds):
    hs, cols = [], []
    for channel, kind in enumerate(kinds):
        if kind == "L":
            poles, weights = [-.5, .5], [.5, .5]
        else:
            poles, weights = [0., -1., 1.], [.75, .125, .125]
        for pole, weight in zip(poles, weights):
            hs.append(pole)
            col = np.zeros(2)
            col[channel] = np.sqrt(weight)
            cols.append(col)
    v = np.array(cols).T
    full = np.block([[np.diag(levels), v], [v.T, np.diag(hs)]])
    e = np.linalg.eigvalsh(full)
    return float(np.minimum(e, 0).sum() - np.minimum(hs, 0).sum())


def shared_bath_falsifier():
    rows = []
    for kinds in [("L", "L"), ("H", "H"), ("H", "L"), ("L", "H")]:
        e0 = onebody_impurity_energy([0., 10.], kinds)
        e1 = onebody_impurity_energy([10., 0.], kinds)
        rows.append({"bath": "".join(kinds), "E0": e0, "E1": e1,
                     "contrast": e1-e0})
    assert abs(rows[0]["contrast"]) < 1e-12
    assert abs(rows[1]["contrast"]) < 1e-12
    assert rows[2]["contrast"] > 7/40
    assert rows[3]["contrast"] < -7/40
    # Exact inequalities used in the proof of R_0 > 11/40.
    assert Q(17, 10)**2 < 3
    assert Q(19, 10)**2 < 2+Q(17, 10)
    assert Q(9, 4)**2 > 5
    assert Q(19, 10) - (1+Q(9, 4))/2 == Q(11, 40)
    return rows


def bath_fixture(kind, delta):
    poles = [-.5, .5] if kind == "L" else [0., -1., 1.]
    weights = [.5, .5] if kind == "L" else [.75, .125, .125]
    annih = car(2+len(poles))
    nums = [a.conj().T @ a for a in annih]
    h0 = -.1*nums[0] + .3*nums[1]
    hop = annih[0].conj().T @ annih[1]
    h0 += .2*(hop+hop.conj().T) + 1.1*nums[0]@nums[1]
    x = delta*(nums[0]-nums[1]+.3*(hop+hop.conj().T))
    vector = np.array([1., .4j]) / np.sqrt(1.16)
    for j, (pole, weight) in enumerate(zip(poles, weights)):
        h0 += pole * nums[j+2]
        for i in range(2):
            y = vector[i]*np.sqrt(weight) * annih[i].conj().T @ annih[j+2]
            h0 += y+y.conj().T
    return h0, h0+x, annih[:2], np.array(poles), vector


def green(h, annih, beta, omega):
    energies, u = eigh(h)
    p = np.exp(-beta*(energies-energies.min()))
    p /= p.sum()
    amps = np.array([u.conj().T@a@u for a in annih])
    denom = 1j*omega + energies[:, None]-energies[None, :]
    weight = (p[:, None]+p[None, :])/denom
    g = np.einsum("anm,bnm,nm->ab", amps, amps.conj(), weight)
    return -(g-g.conj().T)/(2j)


def matrix_sqrt(a):
    e, u = eigh(a)
    return (u*np.sqrt(np.maximum(e, 0)))@u.conj().T


def thermal_contrast_checks():
    rows, green_rows = [], []
    n_terms = 4000
    for beta in [.1, .5, 1., 5.]:
        w = (2*np.arange(n_terms)+1)*np.pi/beta
        gl = w/(w*w+.25)
        gh = .75/w+.25*w/(w*w+1)
        logs = np.log1p(gh/w)-np.log1p(gl/w)
        universal = (2/beta)*logs.sum()
        tail = (2/beta)*.25*(beta/(2*np.pi))**6/(5*(n_terms-.5)**5)
        for delta in [0., .001, .05, 1.]:
            local_norm = delta*np.sqrt(1.09)
            xi = np.minimum(1., local_norm*(2*beta+4/w)*(1+gh/w))
            contrast_bound = (2/beta)*(xi*logs).sum()+tail
            contrasts, widths = [], []
            fs = []
            for kind in ["L", "H"]:
                h0, h1, annih, poles, vector = bath_fixture(kind, delta)
                f0, f1 = free_energy(h0, beta), free_energy(h1, beta)
                bath_f = -np.logaddexp(0., -beta*poles).sum()/beta
                fs.append([f0-bath_f, f1-bath_f])
                contrasts.append(f1-f0)
                for n in [0, 1, 5, 31]:
                    omega = (2*n+1)*np.pi/beta
                    gamma = (omega/(omega**2+.25) if kind == "L"
                             else .75/omega+.25*omega/(omega**2+1))
                    a = omega*np.eye(2)+gamma*np.outer(vector, vector.conj())
                    ah = matrix_sqrt(a)
                    m0, m1 = [green(h, annih, beta, omega) for h in [h0, h1]]
                    for m in [m0, m1]:
                        ev = np.linalg.eigvalsh(ah@m@ah)
                        assert ev.min() >= -1e-11 and ev.max() <= 1+1e-10
                    dnorm = float(np.linalg.norm(m1-m0, 2))
                    q = local_norm*(2*beta/omega+4/omega**2)
                    assert dnorm <= q+1e-11
                    green_rows.append({"beta": beta, "delta": delta,
                                       "bath": kind, "n": n,
                                       "observed_difference_norm": dnorm,
                                       "duhamel_bound": q})
            errors = [fs[0][i]-fs[1][i] for i in range(2)]
            for error in errors:
                assert error >= -1e-11 and error <= universal+tail+1e-10
            contrast_error = abs(contrasts[1]-contrasts[0])
            assert contrast_error <= min(contrast_bound, 2*local_norm)+1e-10
            rows.append({"beta": beta, "delta_input": delta,
                         "centered_difference_norm": local_norm,
                         "contrast_error": contrast_error,
                         "C_beta_with_tail": contrast_bound,
                         "R_beta_sum": universal, "tail": tail,
                         "individual_widths": errors})
    return {"interacting_fixtures": rows, "causal_and_duhamel_checks": green_rows,
            "matsubara_terms": n_terms}


def hierarchy_checks():
    exact, full_fock, vacuum = [], [], []
    for r in range(2, 10):
        eps = Q(1, 8*r)
        a = Q(r, 2*(4*r*r+1))
        trial_num = Q(r, 4*r*r)+eps-Q(1, 2*r)
        trial_norm = 1+Q(1, 4*r*r)
        assert trial_num/trial_norm == -a
        assert Q(r)*eps-Q(1, 4) == -Q(1, 8)
        assert Q(3*r)*eps-Q(1, 4) == Q(1, 8)
        exact.append({"r": r, "epsilon": str(eps), "a": str(a),
                      "design1_hidden_determinant": "-1/8",
                      "design0_hidden_determinant": "1/8"})
        if r <= 5:
            annih = car(r+1)
            nums = [c.conj().T@c for c in annih]
            bath0 = sum(nums[1:])
            all_full = np.eye(1 << (r+1), dtype=complex)
            for n in nums[1:]:
                all_full = all_full@n
            bath1 = bath0+float(-r+eps)*all_full
            coupling = .5*(annih[0].conj().T@annih[1]+annih[1].conj().T@annih[0])
            levels = []
            for bath in [bath0, bath1]:
                e1 = float(np.linalg.eigvalsh(bath+nums[0]+coupling).min())
                e0 = float(np.linalg.eigvalsh(bath+(2*r+1)*nums[0]+coupling-
                                            float(a/2)*np.eye(1 << (r+1))).min())
                levels.append({"E0": e0, "E1": e1, "contrast": e1-e0})
            assert abs(levels[0]["contrast"]-float(a/2)) < 1e-12
            assert levels[1]["contrast"] <= -float(a/2)+1e-12
            full_fock.append({"r": r, "quadratic": levels[0],
                              "interacting": levels[1]})
            # Exact equality of diagonal bath energies on N<=k, before any floats.
            k = r-1
            low = [b for b in range(1 << r) if b.bit_count() <= k]
            assert all(Q(b.bit_count()) == Q(b.bit_count())+
                       (-r+eps)*(b == (1 << r)-1) for b in low)
            # Nonzero k-particle vacuum word with independently chosen real times.
            cb = car(r)
            e0 = np.array([b.bit_count() for b in range(1 << r)], float)
            e1 = e0.copy(); e1[-1] = float(eps)
            times = np.linspace(.13, 1.47, 2*k)
            def word(energy):
                state = np.eye(1 << r, dtype=complex)[:, 0]
                ops = [(cb[j].conj().T, times[j]) for j in range(k)]
                ops += [(cb[j], times[2*k-1-j]) for j in reversed(range(k))]
                for op, time in ops:
                    evolved = np.exp(1j*energy[:, None]*time)*op*np.exp(-1j*energy[None, :]*time)
                    state = evolved@state
                return state[0]
            z0, z1 = word(e0), word(e1)
            assert abs(z0-z1) < 1e-12 and abs(z0) > .99
            vacuum.append({"r": r, "k": k, "low_sector_dimension": len(low),
                           "nonzero_word_difference": abs(z0-z1)})
    return {"rational_hidden_blocks": exact, "full_fock_reversals": full_fock,
            "vacuum_checks": vacuum}


def descent_and_locality():
    h = np.diag([0., 1., 4.]).astype(complex)
    b = np.zeros((3, 3), complex); b[0, 1:] = 1
    g = np.zeros_like(b); g[1, 2], g[2, 1] = -1j/6, 1j/6
    c = b.copy(); c[0, 2] = 2
    drift = b.conj().T@h@b - (b.conj().T@b@h+h@b.conj().T@b)/2
    repaired = drift+1j*(g@h-h@g)
    assert np.linalg.norm(repaired+c.conj().T@c) < 1e-14
    psi = np.array([0, -3., 1.])/np.sqrt(10)
    before, after = [float(np.vdot(psi, d@psi).real) for d in [drift, repaired]]
    assert abs(before-.2) < 1e-14 and abs(after+.1) < 1e-14
    # Independent local CPTP fixtures on a faithful entangled unique ground state.
    omega = np.array([np.sqrt(3)/2, 0, 0, .5])
    p = np.outer(omega, omega)
    hh = np.eye(4)-p
    rows = []
    for probability in [0., .0001, .01, .1, .5, 1.]:
        kraus = [np.diag([1, np.sqrt(1-probability)]),
                 np.array([[0, np.sqrt(probability)], [0, 0]])]
        adj_h = sum(np.kron(k, np.eye(2)).conj().T@hh@np.kron(k, np.eye(2))
                    for k in kraus)
        sigma = sum(np.kron(k, np.eye(2))@p@np.kron(k, np.eye(2)).conj().T
                    for k in kraus)
        epsilon = max(0., float(np.linalg.eigvalsh(adj_h-hh).max()))
        fidelity = float(np.trace(p@sigma).real)
        assert 1-fidelity <= epsilon+1e-12
        if probability:
            assert epsilon > 0
        # Diamond lower witness from |1>; does not claim to solve diamond SDP.
        witness = 2*probability
        upper = min(2., 2*np.sqrt(2*epsilon/.25))
        assert witness <= upper+1e-12
        rows.append({"damping_probability": probability, "worst_case_heating": epsilon,
                     "ground_fidelity": fidelity, "diamond_lower_witness": witness,
                     "rigidity_upper_bound": upper})
    # Instantaneous coercivity is sufficient, not necessary: this completed
    # nondegenerate star has rank-one Q on a two-dimensional excited space,
    # but its finite-window energy loss is strictly coercive.
    hh3 = np.diag([0., 1., 2.]).astype(complex)
    gg3 = np.zeros((3, 3), complex)
    gg3[1, 2] = .5j*(1-np.sqrt(2))/(1+np.sqrt(2))
    gg3[2, 1] = gg3[1, 2].conjugate()
    ht = hh3+gg3
    bb = b.conj().T@b
    ladj = (1j*(np.kron(np.eye(3), ht)-np.kron(ht.T, np.eye(3)))+
            np.kron(b.T, b.conj().T)-
            .5*(np.kron(np.eye(3), bb)+np.kron(bb.T, np.eye(3))))
    invsqrt = np.diag([1., 1/np.sqrt(2)])
    qs = np.outer([1., np.sqrt(2)], [1., np.sqrt(2)])
    assert abs(np.linalg.eigvalsh(invsqrt@qs@invsqrt).min()) < 1e-12
    windows = []
    for time in [.5, 1., 2., 4.]:
        et = (expm(time*ladj)@hh3.reshape(-1, order="F")).reshape((3, 3), order="F")
        gamma = hh3-et
        alpha = float(np.linalg.eigvalsh(invsqrt@gamma[1:, 1:]@invsqrt).min())
        assert alpha > 0 and alpha <= 1
        e2t = (expm(2*time*ladj)@hh3.reshape(-1, order="F")).reshape((3, 3), order="F")
        residual = (1-alpha)**2*hh3-e2t
        assert np.linalg.eigvalsh(residual).min() >= -1e-12
        windows.append({"T": time, "finite_window_coercivity": alpha})
    return {"three_level_before": before, "three_level_after": after,
            "local_entangled_fixtures": rows,
            "rank_one_instantaneous_but_finite_window_coercive": windows}


def repair_and_pauli_scope():
    eta = Q(3, 12500003)
    assert Q(4166667)*eta < 1 < Q(4166668)*eta
    threshold = 12482220
    bound = lambda n: -math.expm1(math.log(.05)/n)
    assert bound(threshold) < float(eta) < bound(threshold-1)
    # Two-action, two-state reward contract; four stationary policies are finite
    # diagnostics for the separately proved all-history potential argument.
    choices = [
        [([Q(1, 2), Q(1, 4)], Q(1, 2)),
         ([Q(7, 10), Q(1, 10)], Q(1, 5))],
        [([Q(1, 5), Q(1, 3)], Q(1, 4)),
         ([Q(0), Q(4, 5)], Q(1, 10))],
    ]
    v = [Q(2), Q(1)]
    for i in range(2):
        for row, reward in choices[i]:
            assert reward+sum(row[j]*v[j] for j in range(2)) <= v[i]
    policies = []
    for policy in product(range(2), repeat=2):
        p, r = zip(*(choices[i][policy[i]] for i in range(2)))
        aa, bb, cc, dd = 1-p[0][0], -p[0][1], -p[1][0], 1-p[1][1]
        det = aa*dd-bb*cc
        values = [(dd*r[0]-bb*r[1])/det, (-cc*r[0]+aa*r[1])/det]
        assert all(values[i] <= v[i] for i in range(2))
        policies.append({"policy": list(policy), "gain": list(map(str, values))})
    # The identity-exclusion issue is exact, not a floating discrepancy.
    # Conjugation characters for I,X,Y,Z acting on a candidate Z term.
    chi_z = [1, -1, -1, 1]
    valid_p = [Q(1, 4)*(1-chi) for chi in chi_z]
    identity_included_p = [Q(1, 4)*(1-Q(1, 2)*(1+chi)) for chi in chi_z]
    assert sum(valid_p) == 1
    assert sum(identity_included_p) == Q(1, 2)
    assert sum(valid_p[i]*chi_z[i] for i in range(4)) == -1
    return {"selected_input_eta": str(eta), "minimum_distinct_supply_for_phi_gt_1": 4166668,
            "zero_termination_trial_boundary": threshold, "stationary_policy_checks": policies,
            "nonidentity_candidate_probability_sum": str(sum(valid_p)),
            "identity_included_probability_sum": str(sum(identity_included_p)),
            "scope_correction": "Remove identity from candidate Pauli set and recount K."}


def main():
    result = {"capital_pin": PIN, "status": "finite_internal_diagnostics_only",
              "producer_imports": False,
              "shared_bath_falsifier": shared_bath_falsifier(),
              "thermal": thermal_contrast_checks(),
              "non_gaussian_hierarchy": hierarchy_checks(),
              "descent_locality": descent_and_locality(),
              "repair_and_pauli_scope": repair_and_pauli_scope()}
    text = json.dumps(result, indent=2, sort_keys=True)+"\n"
    (OUT/"independent_results.json").write_text(text)
    print(json.dumps({"all_checks_passed": True,
                      "shared_bath_fixtures": len(result["shared_bath_falsifier"]),
                      "thermal_fixtures": len(result["thermal"]["interacting_fixtures"]),
                      "green_checks": len(result["thermal"]["causal_and_duhamel_checks"]),
                      "hierarchy_full_fock_fixtures": len(result["non_gaussian_hierarchy"]["full_fock_reversals"]),
                      "hierarchy_rational_blocks": len(result["non_gaussian_hierarchy"]["rational_hidden_blocks"]),
                      "output": str(OUT/"independent_results.json")}, indent=2))


if __name__ == "__main__":
    main()
