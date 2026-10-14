#!/usr/bin/env python3
"""Independent finite truth fixtures for the root thermal-interface note.

Dense diagonalization supplies simulated truth, not free acquisition. Float
checks are diagnostics; analytic inequalities are proved in the accompanying
note. The two-level/sector assertions include exact rational identities.
"""
from pathlib import Path
from fractions import Fraction as Q
import json
import math
import numpy as np

I = np.eye(2)
X = np.array([[0., 1.], [1., 0.]])
Z = np.diag([1., -1.])


def site(op, j, n):
    ans = np.array([[1.]])
    for k in range(n):
        ans = np.kron(ans, op if j == k else I)
    return ans


def distribution(H, A, beta, a=1.):
    E, V = np.linalg.eigh(H)
    weights = np.exp(-beta * (E-E.min()))
    p = weights/weights.sum()
    A_e = V.T.conj() @ A @ V
    prob = p[:, None] * np.abs(A_e)**2/a**2
    d = E[None, :]-E[:, None]
    failure = 1.-prob.sum()
    assert failure >= -1e-12
    return E, p, d, prob, max(0., float(failure))


def assess(H, A, beta, eta, a=1.):
    E, p, d, prob, failure = distribution(H, A, beta, a)
    mag = np.abs(d)
    S = 2*a*a*d/(d*d+eta*eta)
    Y = 2*a*a*mag*np.tanh(beta*mag/2)/(d*d+eta*eta)
    up = np.maximum(d, 0.)
    U = 2*a*a*up*(-np.expm1(-beta*up))/(d*d+eta*eta)
    upper = d > 1e-12
    pairmass = (p[:, None]-p[None, :]) * np.abs(
        np.linalg.eigh(H)[1].T.conj() @ A @ np.linalg.eigh(H)[1])**2
    truth = float(np.sum(np.where(upper, 2*d*pairmass/(d*d+eta*eta), 0.)))
    means = {name: float(np.sum(prob*val)) for name, val in [('signed', S), ('fold', Y), ('up', U)]}
    variance = {name: float(np.sum(prob*val*val)-means[name]**2) for name, val in [('signed', S), ('fold', Y), ('up', U)]}
    B = a*a*min(beta, 1/eta)
    residual = max(abs(v-truth) for v in means.values())
    assert residual < 5e-12
    assert np.max(Y) <= B*(1+1e-12)
    assert variance['fold'] <= variance['signed']+1e-12
    # Diagonal outcomes and failure both output zero.
    assert np.max(np.abs(np.diag(Y))) == 0
    assert truth <= beta*np.trace(np.diag(p) @ (np.linalg.eigh(H)[1].T @ A @ A @ np.linalg.eigh(H)[1])).real+1e-11
    # Quantized energy labels: the complete trace/level fixture remains fixed.
    zeta = eta/32
    rounded = 2*zeta*np.round(E/(2*zeta))
    observed_mag = np.abs(rounded[None, :]-rounded[:, None])
    obs = np.clip(2*a*a*observed_mag*np.tanh(beta*observed_mag/2)/(observed_mag**2+eta**2), 0, B)
    bias = abs(float(np.sum(prob*obs))-truth)
    lip = min(beta/eta, 3/(eta*eta))
    assert np.max(np.abs(rounded-E)) <= zeta*(1+1e-10)
    assert bias <= 2*a*a*lip*zeta+1e-11
    return dict(beta=beta, eta=eta, response=truth, means=means,
                variance=variance, bound=B, failure=failure,
                identity_residual=residual, readout_zeta=zeta,
                readout_bias=bias, readout_bias_bound=2*a*a*lip*zeta), prob, Y


def main():
    n = 6
    xs = [site(X, j, n) for j in range(n)]
    zs = [site(Z, j, n) for j in range(n)]
    H = np.zeros((2**n, 2**n))
    for j in range(n):
        H += (.19+.03*j)*zs[j]+(.31-.02*j)*xs[j]
    for j in range(n-1):
        H += (.27+.01*j)*(zs[j] @ zs[j+1])+.07*(xs[j] @ zs[j+1])
    A = xs[2]
    cases = []
    selected = None
    for beta in (.5, 2., 8.):
        for eta in (.02, .2, 2.):
            row, prob, Y = assess(H, A, beta, eta)
            cases.append(row)
            if beta == 2. and eta == .02:
                selected = prob, Y, row
    # A nonunitary Hermitian filter pays for failures explicitly.
    row, _, _ = assess(H, .7*zs[0]+.2*(xs[1] @ xs[3]), 2., .2, .9)
    assert row['failure'] > .2
    cases.append(row)
    row_commuting, _, _ = assess(H, H/np.linalg.norm(H, 2), 2., .2)
    assert abs(row_commuting['response']) < 1e-20

    # Raw independent multinomial trials, no conditional-success normalization.
    prob, Y, selected_row = selected
    raw_p = np.r_[prob.ravel(), max(0., 1.-prob.sum())]
    raw_p /= raw_p.sum()
    values = np.r_[Y.ravel(), 0.]
    B = selected_row['bound']
    eps, delta = .05, .01
    trials = math.ceil(B*B/(2*eps*eps)*math.log(2/delta))
    rng = np.random.default_rng(20261014)
    counts = rng.multinomial(trials, raw_p)
    estimate = float(counts @ values/trials)
    sampling = dict(trials=trials, raw_filter_failures=int(counts[-1]),
                    target=selected_row['response'], estimate=estimate,
                    abs_error=abs(estimate-selected_row['response']),
                    epsilon=eps, sufficient_failure_probability=delta,
                    seed=20261014, note='one synthetic replay, not a coverage proof')

    # The rejected downward-event output can be very large, despite positivity.
    rejected = 10*math.expm1(10)/101
    assert rejected > 2180

    # beta=log(3), exp(-beta)=1/3 gives exact two-level sector identities.
    eta = Q(1)
    t = Q(1, 2)  # tanh(log(3)/2)
    c = Q(1, 2)
    factor = 2*t/(1+eta*eta)
    w_star = Q(3, 4)  # D=1
    response = lambda w: factor*(w+(1-w)*c*c)
    wrong, canonical = response(Q(1, 2)), response(w_star)
    assert wrong == Q(5, 16) and canonical == Q(13, 32)
    assert canonical-wrong == Q(3, 32)
    sector = dict(beta='log(3)', D=1, gap=1, c='1/2',
                  conditional_down_up='1/3 in both blocks',
                  supplied_weight='1/2', canonical_weight=str(w_star),
                  supplied_response=str(wrong), canonical_response=str(canonical),
                  response_difference=str(canonical-wrong))

    # gap collapse at matched eta: exact formula, numerical evaluations only.
    collapse = []
    for e in (.1, .01, .001, .0001):
        value = math.tanh(e/2)/e
        assert abs(value-.5) <= e*e/24+1e-15
        collapse.append(dict(eta=e, H0_regular_response=0., H1_regular_response=value))

    # Independent bounded finite fixture for the unbounded-observable tail lemma.
    dim = 64
    annih = np.zeros((dim, dim))
    for j in range(1, dim):
        annih[j-1, j] = math.sqrt(j)
    q = (annih+annih.T)/math.sqrt(2)
    p_op = (annih-annih.T)/(1j*math.sqrt(2))
    Hq = np.real(p_op @ p_op/2+q @ q/2+q @ q @ q @ q)
    beta = 1.
    E, V = np.linalg.eigh(Hq)
    weights = np.exp(-beta*(E-E.min())); weights /= weights.sum()
    rho = (V*weights) @ V.T
    M2 = float(np.trace(rho @ q @ q))
    M4 = float(np.trace(rho @ q @ q @ q @ q))
    base, _, _ = assess(Hq, q, beta, .5, np.linalg.norm(q, 2))
    qeval, qvec = np.linalg.eigh(q)
    clipped = []
    for cap in (.5, 1., 2.):
        AL = (qvec*np.clip(qeval, -cap, cap)) @ qvec.T
        row, _, _ = assess(Hq, AL, beta, .5, cap)
        error = abs(base['response']-row['response'])
        bound = 2*beta*math.sqrt(M2*M4)/cap
        assert error <= bound+1e-11
        clipped.append(dict(cap=cap, error=error, analytic_bound=bound))

    result = dict(status='PASS', scope='exact rational identities plus finite float truth fixtures; not hardware, interval proof, acquisition or speedup',
                  numpy=np.__version__, spin_dimension=2**n, cases=cases,
                  commuting_response=row_commuting['response'], sampling=sampling,
                  rejected_exponential_weight=rejected, exact_sector=sector,
                  collapsing_gap=collapse,
                  clipping=dict(finite_basis=dim, M2=M2, M4=M4, cases=clipped,
                                limitation='finite basis diagnostic only; does not certify continuum moments'),
                  analytic_checks_not_replaced_by_code=['CP instrument','Lipschitz uniform bound','clipping lemma','entire-function Euclidean obstruction'])
    out = Path(__file__).with_name('THERMAL_TRANSITION_RESULTS.json')
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', cases=len(cases), max_identity_residual=max(x['identity_residual'] for x in cases),
                          trials=trials, synthetic_error=sampling['abs_error'], exact_sector_gap='3/32', rejected_weight=rejected)))


if __name__ == '__main__':
    main()
