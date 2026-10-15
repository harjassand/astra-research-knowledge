#!/usr/bin/env python3
"""Exact rational checks. Synthetic fixtures; not a replay of producer files."""
from __future__ import annotations
import hashlib
import itertools
import json
from pathlib import Path
import platform
import random
import sys
import time

import mpmath as mp
import sympy as sp

OUT = Path(__file__).resolve().parent
RAT = sp.Rational
COUNTS = {}


def check(name, condition):
    if not bool(condition):
        raise AssertionError(name)
    COUNTS[name] = COUNTS.get(name, 0) + 1


def sub(mat, rows, cols):
    return mat.extract(list(rows), list(cols))


def reduction(q, retained):
    retained = list(retained)
    discarded = [i for i in range(q.rows) if i not in retained]
    if discarded:
        green = (-sub(q, discarded, discarded)).inv()
        qri = sub(q, retained, discarded)
        trace = sub(q, retained, retained) + qri * green * sub(q, discarded, retained)
        alpha = sp.ones(len(retained), 1) + qri * green * sp.ones(len(discarded), 1)
    else:
        green = sp.zeros(0, 0)
        trace = sub(q, retained, retained)
        alpha = sp.ones(len(retained), 1)
    reduced = sp.diag(*[1 / a for a in alpha]) * trace
    return discarded, green, trace, alpha, reduced


def moment_pair(nmat, mu, w, v):
    """Independent full-generator Markov reward second-moment equation."""
    return (mu * nmat * (sp.diag(*w) * nmat * v + sp.diag(*v) * nmat * w))[0]


def audit_chain(seed, ntrans=5):
    rng = random.Random(seed)
    total = ntrans + 2
    q = sp.zeros(total)
    for i in range(ntrans):
        for j in range(ntrans):
            if i != j:
                q[i, j] = rng.randrange(0, 5)
        # Both causes have a positive rate from every transient state.
        q[i, ntrans] = rng.randrange(1, 4)
        q[i, ntrans + 1] = rng.randrange(1, 4)
        q[i, i] = -sum(q[i, j] for j in range(total) if j != i)
    aa = list(range(ntrans))
    nmat = (-sub(q, aa, aa)).inv()
    mu = sp.zeros(1, ntrans)
    mu[0, 0] = 1
    eta = mu * nmat
    rewards = [sp.ones(ntrans, 1), sp.Matrix([(-1)**i * (i + 1) for i in aa]),
               sp.Matrix([i - 2 for i in aa])]
    candidates = list(range(1, ntrans))
    vcache = {}
    for bits in itertools.product([0, 1], repeat=len(candidates)):
        selected = frozenset(j for j, b in zip(candidates, bits) if b)
        retained = sorted({0, ntrans, ntrans + 1} | set(selected))
        ss = [i for i in retained if i < ntrans]
        sidx = [retained.index(i) for i in ss]
        discarded, green, trace, alpha, reduced = reduction(q, retained)
        mu_s = sp.zeros(1, len(ss))
        mu_s[0, ss.index(0)] = 1
        ns = (-sub(trace, sidx, sidx)).inv()
        qhat_s = sub(reduced, sidx, sidx)
        mean_true = (mu * nmat * sp.ones(ntrans, 1))[0]
        mean_hat = (mu_s * (-qhat_s).inv() * sp.ones(len(ss), 1))[0]
        check("mean_preservation", mean_true == mean_hat)
        check("trace_occupation", mu_s * ns == sub(eta, [0], ss))
        if discarded:
            eta_i = sub(eta, [0], discarded)
            m = green * sp.ones(len(discarded), 1)
            vv = 2 * (eta_i * m)[0]
            m2 = 2 * green * m
            vv_reduced = (mu_s * ns * sub(q, ss, discarded) * m2)[0]
            check("certificate_reduced_formula", vv == vv_reduced)
        else:
            eta_i, m, vv = sp.zeros(1, 0), sp.zeros(0, 1), sp.Integer(0)
        vcache[selected] = vv
        errors = []
        for f in rewards:
            fi = sub(f, discarded, [0])
            fr = sp.Matrix([f[i] if i < ntrans else 0 for i in retained])
            br = fr + sub(q, retained, discarded) * green * fi
            error = f.copy()
            for i in ss:
                error[i] -= br[retained.index(i)]
            errors.append(error)
            check("signed_reward_mean", (mu * nmat * error)[0] == 0)
        covariance = sp.zeros(len(rewards))
        for fno, gno in itertools.combinations_with_replacement(range(len(rewards)), 2):
            fi, gi = sub(rewards[fno], discarded, [0]), sub(rewards[gno], discarded, [0])
            expected = (eta_i * (sp.diag(*fi) * green * gi + sp.diag(*gi) * green * fi))[0]
            independent = moment_pair(nmat, mu, errors[fno], errors[gno])
            check("signed_covariance", expected == independent)
            covariance[fno, gno] = covariance[gno, fno] = expected
        check("clock_second_moment", covariance[0, 0] == vv)
        for size in [1, 2, 3]:
            for idx in itertools.combinations(range(3), size):
                check("covariance_psd_principal_minor", sub(covariance, idx, idx).det() >= 0)
        conditional_v = []
        for cause in [ntrans, ntrans + 1]:
            c = nmat * sub(q, aa, [cause])
            p = c[0]
            ha = sp.diag(*c)
            qc = sp.zeros(ntrans + 1)
            qc[:ntrans, :ntrans] = ha.inv() * sub(q, aa, aa) * ha
            qc[:ntrans, ntrans] = ha.inv() * sub(q, aa, [cause])
            nc = (-qc[:ntrans, :ntrans]).inv()
            muc = mu * ha / p
            etac = muc * nc
            check("conditioned_occupation", etac == eta * ha / p)
            retained_c = ss + [ntrans]
            _, gc, kc, ac, qhc = reduction(qc, retained_c)
            ci = sub(c, discarded, [0])
            cs = sub(c, ss, [0])
            if discarded:
                hi = sp.diag(*ci)
                check("conditioned_green", gc == hi.inv() * green * hi)
            good_original_indices = [retained.index(i) for i in ss] + [retained.index(cause)]
            hr = sp.diag(*list(cs), 1)
            check("trace_conditioning_commutes", kc == hr.inv() * sub(trace, good_original_indices, good_original_indices) * hr)
            ac_formula = sp.ones(len(ss), 1) + sp.diag(*[1 / z for z in cs]) * sub(q, ss, discarded) * green * ci
            check("conditioned_clock_formula", ac[:len(ss), :] == ac_formula)
            true_conditional_mean = sub(nc * sp.ones(ntrans, 1), ss, [0])
            reduced_conditional_mean = (-qhc[:len(ss), :len(ss)]).inv() * sp.ones(len(ss), 1)
            check("conditioned_mean_all_retained_starts", true_conditional_mean == reduced_conditional_mean)
            vc = 2 * (eta_i * green * ci)[0] / p
            conditional_v.append((p, vc))
            cond_errors = []
            for f in rewards:
                fi = sub(f, discarded, [0])
                fc_r = sp.Matrix([f[i] for i in ss] + [0])
                bc = fc_r + sub(qc, retained_c, discarded) * gc * fi
                errc = f.copy()
                for i in ss:
                    errc[i] -= bc[retained_c.index(i)]
                cond_errors.append(errc)
                check("conditioned_signed_mean", (muc * nc * errc)[0] == 0)
            for fno, gno in itertools.combinations_with_replacement(range(len(rewards)), 2):
                fi = sub(rewards[fno], discarded, [0])
                gi = sub(rewards[gno], discarded, [0])
                expected = (eta_i * (sp.diag(*fi) * green * sp.diag(*ci) * gi + sp.diag(*gi) * green * sp.diag(*ci) * fi))[0] / p
                independent = moment_pair(nc, muc, cond_errors[fno], cond_errors[gno])
                check("conditioned_signed_covariance", expected == independent)
                if fno == gno == 0:
                    check("conditioned_clock_covariance", expected == vc)
            # Uniqueness claim is checked through the exact conditional Poisson system.
            ordinary_clock = sub(alpha, sidx, [0])
            ordinary_conditional_mean = (-kc[:len(ss), :len(ss)]).inv() * ordinary_clock
            check("common_clock_iff", (ordinary_conditional_mean == true_conditional_mean) == (ordinary_clock == ac_formula))
        check("cause_covariance_accounting", sum(p * v for p, v in conditional_v) == vv)
        for j in discarded:
            jj = discarded.index(j)
            score = 2 * m[jj] * (eta_i * green)[jj] / green[jj, jj]
            more = sorted(set(retained) | {j})
            di, gg, _, _, _ = reduction(q, more)
            vmore = 2 * (sub(eta, [0], di) * gg * sp.ones(len(di), 1))[0]
            check("retained_marginal", vv - vmore == score)
    for selected, value in vcache.items():
        for j in candidates:
            if j not in selected:
                check("certificate_monotonicity", value >= vcache[selected | {j}])
        missing = [j for j in candidates if j not in selected]
        for j, k in itertools.combinations(missing, 2):
            check("certificate_supermodularity", value - vcache[selected | {j}] >= vcache[selected | {k}] - vcache[selected | {j, k}])
    return {"seed": seed, "Q": [[str(x) for x in row] for row in q.tolist()],
            "all_retained_set_certificates": {",".join(map(str, sorted(k))): str(v) for k, v in vcache.items()}}


def mp_number(value):
    return mp.mpf(str(sp.N(value, 95)))


def exact_exp_negative_interval(x, degree=20):
    """Taylor sign remainder, range-reduced to x/m <= 1; rational endpoints."""
    x = RAT(x)
    count = max(1, int(sp.ceiling(x)))
    y = x/count
    upper = sum((-y)**j/sp.factorial(j) for j in range(degree+1))
    lower = upper + (-y)**(degree+1)/sp.factorial(degree+1)
    assert 0 < lower <= upper
    return lower**count, upper**count


def rational_deadline_certificate():
    e1l, e1u = exact_exp_negative_interval(1)
    e100l, e100u = exact_exp_negative_interval(100)
    truel = (e1l-RAT(1, 100)*e100u)/RAT(99, 100)
    trueu = (e1u-RAT(1, 100)*e100l)/RAT(99, 100)
    bandl = exact_exp_negative_interval(RAT(110, 101))[0]-RAT(1, 50)
    bandu = exact_exp_negative_interval(RAT(90, 101))[1]+RAT(1, 50)
    check("rare_deadline_exact_rational_enclosure", 0 < bandl <= truel <= trueu <= bandu < 1)
    check("rare_deadline_true_interval_width", trueu-truel < RAT(1, 10**18))
    certificate = {"method": "Degree 20/21 signed Taylor remainder for exp(-x/m), m=ceil(x), followed by monotone interval powering; all arithmetic rational.",
                   "true_conditional_survival_interval": [str(truel), str(trueu)],
                   "certified_conditional_risk_band": [str(bandl), str(bandu)],
                   "joint_multiplier": "1/1000000", "exact_order_verified": True}
    target = OUT/"rare_deadline_rational_certificate.json"
    target.write_text(json.dumps(certificate, indent=2)+"\n")
    return {"path": str(target), "sha256": hashlib.sha256(target.read_bytes()).hexdigest(), "exact_order_verified": True}


def survival_sum(t, mean):
    mean = mp_number(mean)
    if mean == 1:
        return mp.exp(-t) * (1 + t)
    return (mean * mp.exp(-t / mean) - mp.exp(-t)) / (mean - 1)


def two_cause(p, mc, md):
    q = sp.zeros(5)
    q[0, 1], q[0, 2], q[0, 0] = p, 1-p, -1
    q[1, 3], q[1, 1] = 1/mc, -1/mc
    q[2, 4], q[2, 2] = 1/md, -1/md
    _, _, _, alpha, _ = reduction(q, [0, 3, 4])
    check("two_cause_clock", alpha[0] == 1+p*mc+(1-p)*md)
    vc, vd = 2*mc**2, 2*md**2
    check("two_cause_mixture_certificate", p*vc+(1-p)*vd == 2*(p*mc**2+(1-p)*md**2))
    nmat = (-q[:3, :3]).inv()
    eta = sp.Matrix([[1, 0, 0]])*nmat
    c = nmat*q[:3, 3]
    check("zero_committor_support", c == sp.Matrix([p, 1, 0]))
    discarded, green, _, _, _ = reduction(q, [0, 3, 4])
    check("zero_committor_clock_certificate", 2*(eta[:, 1:3]*green*c[1:3, :])[0]/p == vc)
    # Condition only on positive states; the decoy state has c=0 and is excluded.
    pos = [0, 1]
    hp = sp.diag(*[c[i] for i in pos])
    qc = sp.zeros(3)
    qc[:2, :2] = hp.inv()*sub(q, pos, pos)*hp
    qc[:2, 2] = hp.inv()*sub(q, pos, [3])
    nc = (-qc[:2, :2]).inv()
    muc = sp.Matrix([[1, 0]])
    signed = sp.Matrix([-2, 3, -5])
    signedi = signed[1:3, :]
    signed_correction = signed[0]+(sub(q, [0], discarded)*green*sp.diag(*list(c[1:3, :]))*signedi)[0]/p
    signed_error = sp.Matrix([signed[0]-signed_correction, signed[1]])
    signed_variance = 2*(eta[:, 1:3]*sp.diag(*list(signedi))*green*sp.diag(*list(c[1:3, :]))*signedi)[0]/p
    check("zero_committor_signed_covariance", signed_variance == moment_pair(nc, muc, signed_error, signed_error))
    return {"p_C": str(p), "mean_trap_C": str(mc), "mean_trap_D": str(md),
            "alpha": str(alpha[0]), "alpha_C": str(1+mc), "alpha_D": str(1+md),
            "V_C": str(vc), "V_D": str(vd), "V": str(p*vc+(1-p)*vd)}


def moment_indistinguishability():
    eps = RAT(1, 100)
    rows = []
    baseline = [RAT(1, 3)] * 3
    for mm in [10, 100, 1000, 10000, 100000]:
        mm = sp.Integer(mm)
        slow = 1/(12*mm**2)
        weights = [RAT(1, 3)-(mm-2)*(mm-3)/(24*mm**2),
                   RAT(1, 3)+(mm-1)*(mm-3)/(12*mm**2),
                   RAT(1, 3)-(mm-1)*(mm-2)/(24*mm**2)]
        check("moment_family_weights", sum(weights)+slow == 1 and min(weights) > 0)
        means = [eps, 2*eps, 3*eps]
        for r in [0, 1, 2]:
            old = sum(w*a**r for w, a in zip(baseline, means))
            new = sum(w*a**r for w, a in zip(weights, means))+slow*(eps*mm)**r
            check("moment_family_matching", old == new)
        # Check through full killed-generator solves, independently of mixture identities.
        values = []
        for ww, trapmeans in [([RAT(1, 6), RAT(1, 3), RAT(1, 3), RAT(1, 6)], means+[eps]),
                              (weights+[slow], means+[eps*mm])]:
            q = sp.zeros(6)
            q[0, 0] = -1
            check("moment_family_all_traps_reachable", min(ww) > 0)
            for i, (w, a) in enumerate(zip(ww, trapmeans), 1):
                q[0, i] = w
                q[i, i], q[i, 5] = -1/a, 1/a
            nmat = (-q[:5, :5]).inv()
            mu = sp.Matrix([[1, 0, 0, 0, 0]])
            eta = mu*nmat
            _, g, k, a, qhat = reduction(q, [0, 5])
            v = 2*(eta[:, 1:5]*g*sp.ones(4, 1))[0]
            mt = (mu*nmat*sp.ones(5, 1))[0]
            mt2 = 2*(mu*nmat*nmat*sp.ones(5, 1))[0]
            values.append((k, a, qhat, v, mt, mt2))
        check("identical_reduced_model_certificate_moments", values[0] == values[1])
        t = mp_number(eps)*int(mm)
        old_s = sum(mp_number(w)*survival_sum(t, a) for w, a in zip(baseline, means))
        new_s = sum(mp_number(w)*survival_sum(t, a) for w, a in zip(weights, means))+mp_number(slow)*survival_sum(t, eps*mm)
        rows.append({"M": str(mm), "epsilon": str(eps), "weights": list(map(str, weights)),
                     "slow_weight": str(slow), "alpha": str(values[0][1][0]), "V": str(values[0][3]),
                     "mean_T": str(values[0][4]), "second_moment_T": str(values[0][5]),
                     "deadline": mp.nstr(t, 20), "baseline_survival": mp.nstr(old_s, 30),
                     "modified_survival": mp.nstr(new_s, 30), "survival_ratio": mp.nstr(new_s/old_s, 30)})
    return rows


def main():
    start = time.monotonic()
    mp.mp.dps = 90
    fixtures = [audit_chain(s) for s in [11, 29, 47, 83, 107, 131]]
    ordinary = two_cause(RAT(1, 4), sp.Integer(2), sp.Integer(4))
    rare = two_cause(RAT(1, 10**6), RAT(1, 100), sp.Integer(1000))
    p, alpha_c, vc = mp.mpf("1e-6"), mp.mpf("1.01"), mp.mpf(".0002")
    deadline, tolerance = mp.mpf(1), mp.mpf(".1")
    rare.update({"deadline": "1", "tolerance": ".1", "true_conditional_survival": mp.nstr(survival_sum(deadline, RAT(1, 100)), 30),
                 "ordinary_reduced_conditional_survival": mp.nstr(mp.exp(-deadline/mp_number(sp.Rational(rare["alpha"]))), 30),
                 "cause_reduced_conditional_survival": mp.nstr(mp.exp(-deadline/alpha_c), 30),
                 "conditional_lower_bound": mp.nstr(max(0, mp.exp(-(deadline+tolerance)/alpha_c)-vc/tolerance**2), 30),
                 "conditional_upper_bound": mp.nstr(min(1, mp.exp(-(deadline-tolerance)/alpha_c)+vc/tolerance**2), 30)})
    lower = mp.mpf(rare["conditional_lower_bound"])
    true = mp.mpf(rare["true_conditional_survival"])
    upper = mp.mpf(rare["conditional_upper_bound"])
    check("rare_cause_deadline_band_diagnostic", lower <= true <= upper)
    rare["joint_risk_true"] = mp.nstr(p*true, 30)
    rare["joint_risk_lower"] = mp.nstr(p*lower, 30)
    rare["joint_risk_upper"] = mp.nstr(p*upper, 30)
    rare["rational_interval_certificate"] = rational_deadline_certificate()
    moment_family = moment_indistinguishability()
    result = {"status": "PASS", "scope": "Exact rational synthetic fixtures except explicitly marked decimal survival diagnostics; general proof remains PROOFS.md.",
              "runtime": {"python": sys.version, "platform": platform.platform(), "sympy": sp.__version__, "mpmath": mp.__version__, "wall_seconds": time.monotonic()-start},
              "counts": COUNTS, "fixtures": fixtures, "two_cause_incompatibility": ordinary,
              "rare_cause_deadline_example": rare, "finite_moment_indistinguishability": moment_family,
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    target = OUT / "results.json"
    target.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"], "counts": COUNTS, "wall_seconds": result["runtime"]["wall_seconds"], "results": str(target)}, indent=2))


if __name__ == "__main__":
    main()
