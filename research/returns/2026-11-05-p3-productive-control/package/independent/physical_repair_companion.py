"""Reproducible checks for the finite-source repair companion theorem.

Only finite CTMC algebra is tested; these are not physical validation data.
"""
import json
import math
from itertools import product

import numpy as np
from scipy.linalg import expm


def logsumexp(values):
    values = list(values)
    z = max(values)
    return z + math.log(sum(math.exp(v-z) for v in values))


def repair(N, m, crews, lam=1.0, mu=4.0, nu=1.0):
    b = np.array([lam*(N-k) for k in range(m)])
    d = np.array([mu*min(k, crews) for k in range(m)])
    logw = [0.0]
    for k in range(1, N+1):
        logw.append(logw[-1] + math.log(lam*(N-k+1))
                    - math.log(mu*min(k, crews)))
    pref = []
    pref_r = []
    log_prefix = -math.inf
    log_prefix_r = -math.inf
    for k in range(m):
        log_prefix = float(np.logaddexp(log_prefix, logw[k]))
        log_prefix_r = float(np.logaddexp(log_prefix_r, logw[k]+math.log(nu*(N-k))))
        pref.append(log_prefix)
        pref_r.append(log_prefix_r)
    logh_terms = [pref[k]-math.log(b[k])-logw[k] for k in range(m)]
    logg_terms = [pref_r[k]-math.log(b[k])-logw[k] for k in range(m)]
    logH = logsumexp(logh_terms)
    logG = logsumexp(logg_terms)
    mode = max(range(m), key=lambda k: logw[k])
    logR = logw[mode]-logw[m-1]
    lower = logR-math.log(b[m-1])
    upper = lower+math.log(m*(m+1)/2)
    assert lower-1e-10 <= logH <= upper+1e-10
    return b, d, logw, logh_terms, logg_terms, {
        "N": N, "m": m, "crews": crews, "log_mean_time": logH,
        "log_mean_work": logG, "log_R": logR,
        "log_lower": lower, "log_upper": upper,
    }


def generator(b, d):
    m = len(b)
    Q = np.zeros((m, m))
    for k in range(m):
        Q[k,k] = -b[k]-d[k]
        if k+1<m:
            Q[k,k+1] = b[k]
        if k:
            Q[k,k-1] = d[k]
    return Q


def potential(b, s, lam=1.0, mu=4.0):
    q = lam/(lam+mu)
    xstar = q if s>=q else 1-mu*s/lam
    if b<=xstar:
        return 0.0
    def KL(x):
        return x*math.log(x/q)+(1-x)*math.log((1-x)/(1-q))
    if b<=s:
        return KL(b)
    if xstar>=s:
        rho = 1-b
        c_lam = mu*s/lam
        return c_lam-rho-rho*math.log(c_lam/rho)
    # Integral from s to b of log(mu*s/(lam*(1-x))).
    y0, y1 = 1-b, 1-s
    A = mu*s/lam
    def F(y):
        return y*(math.log(A/y)+1)
    return KL(s)+F(y1)-F(y0)


def main():
    N,m,c = 7,5,2
    b,d,logw,ht,gt,row = repair(N,m,c)
    Q = generator(b,d)
    H = np.linalg.solve(-Q,np.ones(m))
    G = np.linalg.solve(-Q,np.array([N-k for k in range(m)],float))
    H_formula = np.array([math.exp(logsumexp(ht[i:])) for i in range(m)])
    G_formula = np.array([math.exp(logsumexp(gt[i:])) for i in range(m)])
    assert np.allclose(H,H_formula,rtol=1e-12)
    assert np.allclose(G,G_formula,rtol=1e-12)
    policies=0
    for staffing in product(*[range(min(k,c)+1) for k in range(m)]):
        Qp=generator(b,4*np.array(staffing,float))
        Hp=np.linalg.solve(-Qp,np.ones(m))
        Gp=np.linalg.solve(-Qp,np.array([N-k for k in range(m)],float))
        assert np.all(Hp<=H+1e-9)
        assert np.all(Gp<=G+1e-9)
        policies+=1
    # Check the stationary-coupling survival bound at moderate finite N.
    N,m,c=20,12,5
    b,d,lw,ht,gt,row=repair(N,m,c)
    Q=generator(b,d)
    pi=np.exp(np.array(lw)-logsumexp(lw))
    tail=float(pi[m:].sum())
    flux=float(pi[m-1]*b[m-1])
    worst=0.0
    for t in np.geomspace(1e-3,1e4,80):
        fail=1-float(expm(Q*t)[0].sum())
        bound=tail+flux*t
        assert fail<=bound+2e-8
        worst=max(worst,fail-bound)
    rows=[]
    for s in [.13,.15,.175,.20,.25,.40]:
        V=potential(.4,s)
        for N in [100,200,400,800,1600]:
            m=round(.4*N)
            c=round(s*N)
            *_,row=repair(N,m,c)
            row["crew_fraction"]=c/N
            row["limiting_exponent"]=V
            row["log_mean_per_N"]=row["log_mean_time"]/N
            rows.append(row)
    out={"checks":{"exact_formula_matches_linear_system":True,
                   "stationary_policies_exhaustively_checked":policies,
                   "stationary_coupling_survival_bound_checked":True},
         "scaling":rows}
    print(json.dumps(out,indent=2))


if __name__=="__main__":
    main()
