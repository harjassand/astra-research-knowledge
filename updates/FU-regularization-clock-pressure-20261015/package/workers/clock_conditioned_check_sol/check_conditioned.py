#!/usr/bin/env python3
"""Exact rational audits of conditioned CTMC trace clocks.

Only supplied mathematical models are checked. No rate acquisition, novelty,
physical validation, or computational advantage is inferred from this audit.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path
import random

import sympy as s

OUT = Path(__file__).resolve().parent


def sub(M, rows, cols):
    return M.extract(list(rows), list(cols))


def dotrow(a, b):
    return (a * b)[0]


def scalar(v):
    return s.cancel(v)


def rat(v):
    return str(s.cancel(v))


def must_equal(a, b):
    if isinstance(a, s.MatrixBase):
        assert a.shape == b.shape
        assert all(s.cancel(x-y) == 0 for x, y in zip(a, b)), (a, b)
    else:
        assert s.cancel(a-b) == 0, (a, b)


def branch_chain(prob_b, mean_b, mean_a=None):
    """r -> A or iB -> B; optional separate iA -> A."""
    if mean_a is None:
        Q = s.zeros(4)
        Q[0, 1], Q[0, 2], Q[0, 0] = prob_b, 1-prob_b, -1
        Q[1, 3], Q[1, 1] = 1/mean_b, -1/mean_b
        return Q, [0, 1], [2, 3]
    Q = s.zeros(5)
    Q[0, 1], Q[0, 2], Q[0, 0] = 1-prob_b, prob_b, -1
    Q[1, 3], Q[1, 1] = 1/mean_a, -1/mean_a
    Q[2, 4], Q[2, 2] = 1/mean_b, -1/mean_b
    return Q, [0, 1, 2], [3, 4]


def audit_random():
    rng = random.Random(2026101501)
    counts = dict(retained_sets=0, conditioned_trace=0, conditioned_means=0,
                  covariance_entries=0, conditional_marginals=0,
                  supermodular_comparisons=0)
    all_worst = []
    for trial in range(4):
        n, k = 5, 3
        Q = s.zeros(n+k)
        for i in range(n):
            for j in range(n+k):
                if i != j:
                    Q[i, j] = rng.randint(1, 5)
            Q[i, i] = -sum(Q[i, j] for j in range(n+k) if j != i)
        A = Q[:n, :n]
        H = (-A).inv()
        mu = s.zeros(1, n)
        mu[0, 0] = 1
        eta = mu*H
        committors = [H*Q[:n, n+a] for a in range(k)]
        rewards = [s.ones(n, 1), s.Matrix([1, -2, 3, -4, 5]),
                   s.Matrix([-2, 3, -1, 2, -3])]
        vals = {}
        for mask in range(1 << (n-1)):
            S = [0]+[j for j in range(1, n) if mask & (1 << (j-1))]
            I = [j for j in range(1, n) if j not in S]
            R = S+list(range(n, n+k))
            qSI = sub(Q, S, I)
            G = (-sub(Q, I, I)).inv() if I else s.zeros(0)
            K = sub(Q, R, R)+sub(Q, R, I)*G*sub(Q, I, R)
            counts['retained_sets'] += 1
            for a, c in enumerate(committors):
                p = c[0]
                C = s.diag(*list(c))
                Ac = C.inv()*A*C
                Hc = (-Ac).inv()
                muc = mu*C/p
                etac = muc*Hc
                must_equal(etac, eta*C/p)
                cI, cS = sub(c, I, [0]), sub(c, S, [0])
                u = G*cI
                alpha = s.ones(len(S), 1)+s.diag(*list(cS)).inv()*qSI*u
                # Independently eliminate the already-conditioned full chain.
                ci_plus = s.diag(*list(cI)) if I else s.zeros(0)
                cR = s.Matrix(list(cS)+[s.Integer(int(x == a)) for x in range(k)])
                # On transient retained states only; zero-committor targets are omitted.
                CS = s.diag(*list(cS))
                Kc = CS.inv()*K[:len(S), :len(S)]*CS
                direct = sub(Ac, S, S)
                if I:
                    direct += sub(Ac, S, I)*(-sub(Ac, I, I)).inv()*sub(Ac, I, S)
                must_equal(Kc, direct)
                counts['conditioned_trace'] += 1
                reduced_mean = (-Kc).inv()*alpha
                must_equal(reduced_mean, sub(Hc*s.ones(n, 1), S, [0]))
                counts['conditioned_means'] += 1
                V = scalar(2*dotrow(sub(eta, [0], I), u)/p)
                vals[(mask, a)] = V
                ds, us = [], []
                for f in rewards:
                    fI = sub(f, I, [0])
                    hfI = G*s.diag(*list(cI))*fI if I else s.zeros(0, 1)
                    d = f.copy()
                    dS = -CS.inv()*qSI*hfI
                    for index, j in enumerate(S):
                        d[j] = dS[index]
                    uf = Hc*d
                    must_equal(sub(uf, S, [0]), s.zeros(len(S), 1))
                    ds.append(d)
                    us.append(uf)
                for fi in range(len(rewards)):
                    for gi in range(fi, len(rewards)):
                        f, g = rewards[fi], rewards[gi]
                        direct_cov = dotrow(etac, s.matrix_multiply_elementwise(ds[fi], us[gi])
                                            + s.matrix_multiply_elementwise(ds[gi], us[fi]))
                        hcg = G*s.diag(*list(cI))*sub(g, I, [0]) if I else s.zeros(0, 1)
                        hcf = G*s.diag(*list(cI))*sub(f, I, [0]) if I else s.zeros(0, 1)
                        integrand = s.matrix_multiply_elementwise(sub(f, I, [0]), hcg)
                        integrand += s.matrix_multiply_elementwise(sub(g, I, [0]), hcf)
                        formula = dotrow(sub(eta, [0], I), integrand)/p
                        must_equal(direct_cov, formula)
                        if fi == gi == 0:
                            must_equal(formula, V)
                        counts['covariance_entries'] += 1
                if I:
                    z = G.T*sub(eta, [0], I).T
                    for jindex, j in enumerate(I):
                        J = [l for l in I if l != j]
                        Gj = (-sub(Q, J, J)).inv() if J else s.zeros(0)
                        vj = 2*dotrow(sub(eta, [0], J), Gj*sub(c, J, [0]))/p
                        marginal = 2*z[jindex]*u[jindex]/(p*G[jindex, jindex])
                        must_equal(V-vj, marginal)
                        counts['conditional_marginals'] += 1
        # Decreasing supermodularity: adding j has a larger reduction earlier.
        for a in range(k):
            for m1 in range(16):
                for m2 in range(16):
                    if (m1 & m2) != m1:
                        continue
                    for j in range(4):
                        bit = 1 << j
                        if m2 & bit:
                            continue
                        d1 = vals[m1, a]-vals[m1 | bit, a]
                        d2 = vals[m2, a]-vals[m2 | bit, a]
                        assert d1 >= d2 >= 0
                        counts['supermodular_comparisons'] += 1
        all_worst.append(max(vals[0, a] for a in range(k)))
    return {"counts": counts, "initial_worst_conditional_V": [rat(v) for v in all_worst]}


def exp_upper(x, terms):
    """Exact rational upper bound on exp(x), x >= 0."""
    assert x >= 0 and terms+2 > x
    term, partial = s.Integer(1), s.Integer(1)
    for j in range(1, terms+1):
        term *= x/j
        partial += term
    nxt = term*x/(terms+1)
    return scalar(partial+nxt/(1-x/(terms+2)))


def uniformized_cause_cdf(A, mu, c, t, terms=90, exp_terms=110):
    """Exact enclosure for p - mu exp(A t)c on a rational killed chain.

    A must have nonnegative off-diagonal entries, nonpositive row sums, and
    Ac <= 0. Uniformization then gives 0 <= mu P^j c <= p.
    """
    n = A.rows
    assert all(A[i, j] >= 0 for i in range(n) for j in range(n) if i != j)
    assert all(x <= 0 for x in A*s.ones(n, 1))
    assert all(x <= 0 for x in A*c)
    assert all(x >= 0 for x in mu) and all(x >= 0 for x in c)
    lam = max(-A[i, i] for i in range(n))
    assert lam > 0
    P = s.eye(n)+A/lam
    assert all(x >= 0 for x in P)
    x = scalar(lam*t)
    Uexp = exp_upper(x, exp_terms)
    coeff, S, Z = s.Integer(1), s.Integer(1), dotrow(mu, c)
    v, p = c, dotrow(mu, c)
    for j in range(1, terms+1):
        v = P*v
        coeff *= x/j
        S += coeff
        Z += coeff*dotrow(mu, v)
    lo, hi = scalar((p*S-Z)/Uexp), scalar(p-Z/Uexp)
    assert 0 <= lo <= hi <= p
    return {"lower": lo, "upper": hi, "p": p, "lambda": lam,
            "t": t, "poisson_terms": terms, "exp_terms": exp_terms,
            "poisson_tail_upper": scalar(1-S/Uexp)}


def json_interval(v):
    return {key: (rat(x) if isinstance(x, (s.Expr, int)) else x) for key, x in v.items()} | {
        "lower_float": float(v['lower']), "upper_float": float(v['upper']),
        "width_float": float(v['upper']-v['lower'])}


def branch_risks(prob_b, mean_a, mean_b, extra_retained=()):
    Q, U, B = branch_chain(prob_b, mean_b, mean_a)
    A, mu = Q[:3, :3], s.Matrix([[1, 0, 0]])
    H = (-A).inv()
    eta = mu*H
    I = [j for j in [1, 2] if j not in extra_retained]
    G = (-sub(Q, I, I)).inv() if I else s.zeros(0)
    vs = []
    ps = []
    for b in B:
        c = H*Q[:3, b]
        p = dotrow(mu, c)
        ps.append(p)
        vs.append(scalar(2*dotrow(sub(eta, [0], I), G*sub(c, I, [0]))/p))
    return vs, scalar(sum(p*v for p, v in zip(ps, vs)))


def saturated_greedy(Q, transient_count, mu, I, cause_targets, quotas, costs):
    """Exact saturated-cover selector with shared Green-matrix rank-one updates.

    Causes are lists of target indices; all costs are positive and additive.
    Quotas are conditional clock variances. No actual CDF guarantee is inferred
    until deadline enclosures have also been evaluated.
    """
    n = transient_count
    H = (-Q[:n, :n]).inv()
    eta = mu*H
    cs = [H*sum((Q[:n, b] for b in bs), s.zeros(n, 1)) for bs in cause_targets]
    ps = [dotrow(mu, c) for c in cs]
    assert all(p > 0 for p in ps) and all(costs[j] > 0 for j in I)
    I = list(I)
    G = (-sub(Q, I, I)).inv() if I else s.zeros(0)
    z = G.T*sub(eta, [0], I).T
    us = [G*sub(c, I, [0]) for c in cs]
    vs = [scalar(2*dotrow(sub(eta, [0], I), u)/p) for u, p in zip(us, ps)]
    steps = []
    while any(v > q for v, q in zip(vs, quotas)):
        if not I:
            raise AssertionError("Nonzero remaining error after all states retained")
        # Verify the rank-one-maintained quantities against the actual block.
        must_equal(G, (-sub(Q, I, I)).inv())
        must_equal(z, G.T*sub(eta, [0], I).T)
        for u, c, v, p in zip(us, cs, vs, ps):
            must_equal(u, G*sub(c, I, [0]))
            must_equal(v, 2*dotrow(sub(eta, [0], I), u)/p)
        candidate = []
        for ji, j in enumerate(I):
            deltas = [scalar(2*z[ji]*u[ji]/(p*G[ji, ji])) for u, p in zip(us, ps)]
            benefit = sum(min(d, max(s.Integer(0), v-q))
                          for d, v, q in zip(deltas, vs, quotas))
            candidate.append((scalar(benefit/costs[j]), -j, ji, deltas))
        score, _, ji, deltas = max(candidate)
        assert score > 0
        chosen = I[ji]
        steps.append({"state": chosen, "score": rat(score),
                      "before_V": [rat(v) for v in vs],
                      "delta_V": [rat(d) for d in deltas]})
        remaining = [l for l in range(len(I)) if l != ji]
        gjj = G[ji, ji]
        col, row = sub(G, remaining, [ji]), sub(G, [ji], remaining)
        z = sub(z, remaining, [0])-row.T*z[ji]/gjj
        us = [sub(u, remaining, [0])-col*u[ji]/gjj for u in us]
        G = sub(G, remaining, remaining)-col*row/gjj
        I = [j for j in I if j != chosen]
        vs = [scalar(v-d) for v, d in zip(vs, deltas)]
    return {"steps": steps, "final_V": [rat(v) for v in vs],
            "remaining_discarded": I, "quotas": [rat(q) for q in quotas]}


def examples():
    eps, M = s.Rational(1, 1000), s.Integer(10)
    Q, U, B = branch_chain(eps, M)
    A, H = Q[:2, :2], (-Q[:2, :2]).inv()
    mu = s.Matrix([[1, 0]])
    eta, cB = mu*H, H*Q[:2, B[1]]
    alpha, alphaB = 1+eps*M, 1+M
    incompatible = {
        "state_order": ["r", "iB", "A", "B"],
        "Q": [[rat(x) for x in row] for row in Q.tolist()],
        "p_B": rat(eps), "unconditional_alpha_r": rat(alpha),
        "alpha_A_r": "1", "alpha_B_r": rat(alphaB),
        "true_mean_A": "1", "true_mean_B": rat(1+M),
        "ordinary_reduced_mean_A_and_B": rat(alpha),
        "unconditional_V": rat(2*eps*M*M), "conditional_V_B": rat(2*M*M),
        "ordinary_joint_B_CDF_at_10": json_interval(uniformized_cause_cdf(
            s.Matrix([[-1/alpha]]), s.Matrix([[eps]]), s.Matrix([1]), s.Integer(10))),
        "full_joint_B_CDF_at_10": json_interval(uniformized_cause_cdf(A, mu, cB, s.Integer(10))),
        "cause_specific_joint_B_CDF_at_10": json_interval(uniformized_cause_cdf(
            s.Matrix([[-1/alphaB]]), s.Matrix([[eps]]), s.Matrix([1]), s.Integer(10)))
    }
    # Max over two independent cause errors is not supermodular.
    worst_max = {"V_A_V_B_empty": ["2", "2"],
                 "V_A_V_B_retain_iA": ["0", "2"],
                 "V_A_V_B_retain_iB": ["2", "0"],
                 "V_A_V_B_retain_both": ["0", "0"],
                 "max_benefit_empty": "0", "max_benefit_singletons": "0",
                 "max_benefit_pair": "2",
                 "submodularity_violation": "0 + 0 < 2 + 0"}
    for retained, expected in [((), [2, 2]), ((1,), [0, 2]),
                               ((2,), [2, 0]), ((1, 2), [0, 0])]:
        actual, _ = branch_risks(s.Rational(1, 2), s.Integer(1), s.Integer(1), retained)
        assert actual == expected
    # One slot: average error spends it on common cause; worst-cause on rare cause.
    choice = {"p_A": "999/1000", "p_B": "1/1000",
              "mean_iA": "2", "mean_iB": "10",
              "conditional_V_before": {"A": "8", "B": "200"},
              "unconditional_V_before": "1024/125",
              "unconditional_improvement_iA": "999/125",
              "unconditional_improvement_iB": "1/5",
              "unconditional_choice": "iA", "worst_cause_choice": "iB",
              "worst_error_after_unconditional_choice": "200",
              "worst_error_after_worst_cause_choice": "8"}
    base_v, base_avg = branch_risks(eps, s.Integer(2), M)
    va, avga = branch_risks(eps, s.Integer(2), M, (1,))
    vb, avgb = branch_risks(eps, s.Integer(2), M, (2,))
    assert base_v == [8, 200] and va == [0, 200] and vb == [8, 0]
    must_equal(base_avg, s.Rational(1024, 125))
    must_equal(base_avg-avga, s.Rational(999, 125))
    must_equal(base_avg-avgb, s.Rational(1, 5))
    Qchoice, _, _ = branch_chain(eps, M, s.Integer(2))
    cover_rare = saturated_greedy(Qchoice, 3, s.Matrix([[1, 0, 0]]), [1, 2],
                                  [[3], [4]], [s.Integer(8), s.Integer(8)],
                                  {1: s.Integer(1), 2: s.Integer(1)})
    assert [step['state'] for step in cover_rare['steps']] == [2]
    Qboth, _, _ = branch_chain(s.Rational(1, 2), s.Integer(1), s.Integer(1))
    cover_both = saturated_greedy(Qboth, 3, s.Matrix([[1, 0, 0]]), [1, 2],
                                  [[3], [4]], [s.Integer(0), s.Integer(0)],
                                  {1: s.Integer(1), 2: s.Integer(1)})
    assert [step['state'] for step in cover_both['steps']] == [1, 2]
    # Fast-discarded excursion: a nontrivial deadline enclosure.
    Qf, _, Bf = branch_chain(s.Rational(1, 2), s.Rational(1, 100))
    Af, muf = Qf[:2, :2], s.Matrix([[1, 0]])
    cf = (-Af).inv()*Qf[:2, Bf[1]]
    Vc, delta = s.Rational(1, 5000), s.Rational(1, 10)
    penalty = Vc/(Vc+delta*delta)
    p, ah = s.Rational(1, 2), s.Rational(101, 100)
    redA, redmu, redc = s.Matrix([[-1/ah]]), s.Matrix([[1]]), s.Matrix([1])
    low_red = uniformized_cause_cdf(redA, redmu, redc, 1-delta, 50, 70)
    high_red = uniformized_cause_cdf(redA, redmu, redc, 1+delta, 50, 70)
    jointlo = max(s.Integer(0), p*(low_red['lower']-penalty))
    jointhi = min(p, p*(high_red['upper']+penalty))
    full = uniformized_cause_cdf(Af, muf, cf, s.Integer(1), 250, 290)
    assert jointlo <= full['lower'] <= full['upper'] <= jointhi
    deadline = {"delta": rat(delta), "conditional_V": rat(Vc),
                "conditional_Cantelli_penalty": rat(penalty),
                "certificate_joint_lower": rat(jointlo), "certificate_joint_upper": rat(jointhi),
                "certificate_joint_lower_float": float(jointlo),
                "certificate_joint_upper_float": float(jointhi),
                "full_reference": json_interval(full),
                "lower_reduced_CDF": json_interval(low_red),
                "upper_reduced_CDF": json_interval(high_red)}
    # Signed reward cancellation can be lost on retaining a state.
    Qs = s.Matrix([[-1, 1, 0, 0], [0, -1, 1, 0],
                   [0, 0, -1, 1], [0, 0, 0, 0]])
    etas = s.Matrix([[1, 0, 0]])*(-Qs[:3, :3]).inv()
    fs = s.Matrix([0, 1, -2])
    signed_vars = []
    cov_matrices = []
    for Is in [[1, 2], [2]]:
        Gs = (-sub(Qs, Is, Is)).inv()
        fIs, etaIs = sub(fs, Is, [0]), sub(etas, [0], Is)
        signed_vars.append(scalar(2*dotrow(etaIs,
            s.matrix_multiply_elementwise(fIs, Gs*fIs))))
        Fs = s.Matrix([[int(i == 1), int(i == 2)] for i in Is])
        Deta = s.diag(*list(etaIs))
        cov_matrices.append(Fs.T*(Deta*Gs+Gs.T*Deta)*Fs)
    assert signed_vars == [6, 8]
    delta_cov = cov_matrices[0]-cov_matrices[1]
    assert delta_cov.det() == -1
    signed_failure = {"state_order": ["r", "i1", "i2", "B"],
                      "all_forward_rates": "1", "reward": ["0", "1", "-2", "0"],
                      "V_eliminate_i1_i2": "6", "V_retain_i1": "8",
                      "two_nonnegative_rewards_covariance_before": cov_matrices[0].tolist(),
                      "two_nonnegative_rewards_covariance_after": cov_matrices[1].tolist(),
                      "covariance_decrease_matrix": delta_cov.tolist(),
                      "covariance_decrease_determinant": "-1"}
    signed_failure = json.loads(json.dumps(signed_failure, default=str))
    return {"incompatible_clock": incompatible,
            "worst_cause_non_submodular": worst_max,
            "rare_cause_retention_choice": choice,
            "saturated_cover_rare_cause": cover_rare,
            "saturated_cover_two_quotas": cover_both,
            "exact_deadline_certificate": deadline,
            "signed_reward_monotonicity_failure": signed_failure}


def main():
    result = {"status": "PASS", "scope": "Exact rational supplied-generator mathematics only",
              "random_audit": audit_random(), "examples": examples()}
    path = OUT/'results.json'
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({"status": result['status'],
                      "counts": result['random_audit']['counts'],
                      "deadline_interval": [result['examples']['exact_deadline_certificate'][
                          'certificate_joint_'+side+'_float'] for side in ['lower', 'upper']],
                      "saved": str(path)}, indent=2))


if __name__ == '__main__':
    main()
