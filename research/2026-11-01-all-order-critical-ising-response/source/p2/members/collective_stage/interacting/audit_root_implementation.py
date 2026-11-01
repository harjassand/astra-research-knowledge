"""Independent full-state audit of the root's acquired local-table recursion.

Small local identities are checked exactly over Fraction-valued physical states.
Response comparisons use a separate 85-digit Decimal physical Poisson solver.
The n=15 check uses a conventional full-state symmetric CG solve and reports its
residual explicitly; it is a floating numerical comparison, not an exact proof.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'root'))
from conditional_response import Chain, initial, eliminate, solve
from fractions import Fraction as Q
from decimal import Decimal as D, localcontext
from itertools import product
import json
import time
import numpy as np
from scipy.sparse import coo_matrix, diags
from scipy.sparse.linalg import LinearOperator, cg


def enumerate_physics(chain):
    """Enumerate only the stated Gibbs factors, physical rates, and raw source."""
    n = chain.n
    states = list(product(range(2), repeat=n))
    index = {x: k for k, x in enumerate(states)}
    weight, obs, rates, dest = [], [], [], []
    for x in states:
        z = Q(1)
        for i in range(n):
            z *= chain.unary[i][x[i]]
        for i in range(n - 1):
            z *= chain.edge[i][x[i]][x[i + 1]]
        weight.append(z)
        s = [2 * k - 1 for k in x]
        obs.append(chain.constant + sum(chain.a[i] * s[i] for i in range(n))
                   + sum(chain.b[i] * s[i] * s[i + 1] for i in range(n - 1)))
        rates.append([chain.rate[i][x[i - 1] if i else 0][x[i]]
                      [x[i + 1] if i + 1 < n else 0] for i in range(n)])
        dest.append([index[x[:i] + (1 - x[i],) + x[i + 1:]] for i in range(n)])
    z = sum(weight)
    prob = [p / z for p in weight]
    mean = sum(p * f for p, f in zip(prob, obs))
    source = [f - mean for f in obs]
    return states, prob, source, rates, dest


def exact_local_audit(chain):
    """Independently sum every state, without the algorithm's transfer tables."""
    coarse, data = eliminate(chain)
    states, prob, source, rates, dest = enumerate_physics(chain)
    cstates, cprob, csource, crates, _ = enumerate_physics(coarse)
    ci = {x: k for k, x in enumerate(cstates)}
    group = [ci[x[1::2]] for x in states]
    ps = [sum(p for p, g in zip(prob, group) if g == k) for k in range(len(cstates))]
    psource = [sum(p * f for p, f, g in zip(prob, source, group) if g == k) / ps[k]
               for k in range(len(cstates))]
    q = [source[k] - psource[group[k]] for k in range(len(states))]
    # Acquire F^-1 q through an independent two-point conditional sum from pi.
    v = [Q(0) for _ in states]
    for k, x in enumerate(states):
        for i in range(0, chain.n, 2):
            y = dest[k][i]
            p0, p1 = prob[k], prob[y]
            conditional_mean = (p0 * source[k] + p1 * source[y]) / (p0 + p1)
            gamma = rates[k][i] + rates[y][i]
            v[k] += (source[k] - conditional_mean) / gamma
    # Independently multiply physical F on v and KS in its Dirichlet form.
    fv = [sum(rates[k][i] * (v[k] - v[dest[k][i]])
              for i in range(0, chain.n, 2)) for k in range(len(states))]
    b = sum(p * qq * vv for p, qq, vv in zip(prob, q, v))
    c = sum(prob[k] * rates[k][i] * (v[k] - v[dest[k][i]]) ** 2 / 2
            for k in range(len(states)) for i in range(1, chain.n, 2))
    rate_error = Q(0)
    for ck in range(len(cstates)):
        for j, i in enumerate(range(1, chain.n, 2)):
            rate = sum(prob[k] * rates[k][i] for k in range(len(states))
                       if group[k] == ck) / ps[ck]
            rate_error = max(rate_error, abs(rate - crates[ck][j]))
    errors = dict(gibbs=max(abs(a - b) for a, b in zip(ps, cprob)),
                  source=max(abs(a - b) for a, b in zip(psource, csource)),
                  averaged_rates=rate_error,
                  fast_poisson=max(abs(a - b) for a, b in zip(fv, q)),
                  b=abs(b - data['b']), c=abs(c - data['c']))
    return dict(all_exact_zero=all(x == 0 for x in errors.values()),
                errors={k: str(x) for k, x in errors.items()},
                b=float(b), c=float(c), theta=float(data['theta']))


def dec(x):
    if isinstance(x, Q):
        return D(x.numerator) / D(x.denominator)
    return D(str(x))


def decimal_response(chain, precision=85):
    states, prob, source, rates, dest = enumerate_physics(chain)
    with localcontext() as ctx:
        ctx.prec = precision
        p = list(map(dec, prob)); f = list(map(dec, source))
        size = len(states)
        # K + 1 pi^T is nonsingular and selects the mean-zero Poisson solution.
        mat = [[p[j] for j in range(size)] + [f[i]] for i in range(size)]
        for k in range(size):
            for i, rate in enumerate(rates[k]):
                rr = dec(rate)
                mat[k][k] += rr
                mat[k][dest[k][i]] -= rr
        for k in range(size):
            pivot = max(range(k, size), key=lambda j: abs(mat[j][k]))
            mat[k], mat[pivot] = mat[pivot], mat[k]
            for j in range(k + 1, size):
                if not mat[j][k]:
                    continue
                fac = mat[j][k] / mat[k][k]
                mat[j][k] = D(0)
                for l in range(k + 1, size + 1):
                    mat[j][l] -= fac * mat[k][l]
        u = [D(0)] * size
        for k in range(size - 1, -1, -1):
            u[k] = (mat[k][-1] - sum(mat[k][j] * u[j] for j in range(k + 1, size))) / mat[k][k]
        return sum(p[k] * f[k] * u[k] for k in range(size))


def numerical_response(chain):
    """A deliberately full-state conventional comparator, for n=15 only."""
    n = chain.n; size = 1 << n
    ids = np.arange(size); bits = (ids[:, None] >> np.arange(n)) & 1
    logp = np.zeros(size)
    for i in range(n):
        unary = np.asarray(chain.unary[i], dtype=float)
        logp += np.log(unary[bits[:, i]])
    for i in range(n - 1):
        edge = np.asarray(chain.edge[i], dtype=float)
        logp += np.log(edge[bits[:, i], bits[:, i + 1]])
    p = np.exp(logp - logp.max()); p /= p.sum(); g = np.sqrt(p)
    spins = 2 * bits - 1
    raw = float(chain.constant) + spins @ np.asarray(chain.a, dtype=float)
    raw += (spins[:, :-1] * spins[:, 1:]) @ np.asarray(chain.b, dtype=float)
    raw -= p @ raw; f = g * raw
    diagonal = np.zeros(size); rows=[]; cols=[]; vals=[]
    for i in range(n):
        tab = np.asarray(chain.rate[i], dtype=float)
        rr = tab[bits[:, i - 1] if i else np.zeros(size, dtype=int), bits[:, i],
                 bits[:, i + 1] if i + 1 < n else np.zeros(size, dtype=int)]
        other = ids ^ (1 << i)
        diagonal += rr
        rows.append(ids); cols.append(other); vals.append(-rr * g / g[other])
    rows.append(ids); cols.append(ids); vals.append(diagonal)
    K = coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(size, size)).tocsr()
    # Remove tiny asymmetric roundoff before conjugate gradients.
    K = (K + K.T) * .5
    operator = LinearOperator((size,size), matvec=lambda x: K @ x + g * (g @ x))
    precond = diags(1 / np.maximum(diagonal + p, 1e-300))
    count = [0]
    def callback(x): count[0] += 1
    u, status = cg(operator, f, M=precond, rtol=2e-11, atol=0., maxiter=18000, callback=callback)
    residual = np.linalg.norm(operator @ u - f) / np.linalg.norm(f)
    return dict(response=float(f @ u), status=int(status), iterations=count[0], relative_residual=float(residual))


def run():
    records=[]
    for n, src, fields in [(3,'mixed',True),(7,'mixed',True),(7,'magnetization',False),(7,'bonds',True)]:
        start=time.perf_counter()
        chain=initial(n,sep=Q(1,10000),exact=True,source=src,fields=fields)
        checks=[]; cur=chain
        while cur.n>1:
            checks.append(dict(n=cur.n,**exact_local_audit(cur)))
            cur,_=eliminate(cur)
        truth=decimal_response(chain)
        bounds=solve(chain)
        with localcontext() as ctx:
            ctx.prec=85
            contained=dec(bounds['lower'])<=truth<=dec(bounds['upper'])
        record=dict(n=n,source=src,fields=fields,sep='1/10000',precision=85,
                    response=str(truth),lower=float(bounds['lower']),upper=float(bounds['upper']),
                    enclosure_pass=contained,local_checks=checks,seconds=time.perf_counter()-start)
        records.append(record)
        print(json.dumps({k:record[k] for k in ['n','source','enclosure_pass','seconds']}),flush=True)
    start=time.perf_counter()
    chain=initial(15,sep=Q(1,20),exact=True,source='mixed',fields=True)
    bounds=solve(chain); numer=numerical_response(chain)
    record=dict(n=15,source='mixed',fields=True,sep='1/20',mode='float64 full-state CG comparison',
                lower=float(bounds['lower']),upper=float(bounds['upper']),**numer,
                enclosure_pass=float(bounds['lower'])<=numer['response']<=float(bounds['upper']),
                seconds=time.perf_counter()-start)
    records.append(record);print(json.dumps(record),flush=True)
    out=dict(all_pass=all(x['enclosure_pass'] and all(y['all_exact_zero'] for y in x.get('local_checks',[])) for x in records),
             root_module='collective_stage/root/conditional_response.py',records=records)
    Path(__file__).with_name('audit_root_implementation_results.json').write_text(json.dumps(out,indent=2)+'\n')


if __name__=='__main__':
    run()
