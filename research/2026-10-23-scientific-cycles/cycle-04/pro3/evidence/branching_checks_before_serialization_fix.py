#!/usr/bin/env python3
"""Exact finite tree certificates plus high-precision quotient diagnostics.

Standard library only. The mathematical theorem is not inferred from these
finite laws. All probability construction/admission checks use Fraction.
Decimal powers are diagnostics with explicit precision and comparison.
"""
from __future__ import annotations
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import resource
import time


CASES = [(4, 2, 16, 11), (64, 2, 20, 14), (64, 3, 48, 16),
         (64, 4, 200, 32), (64, 6, 680, 64)]


def dec(x):
    if isinstance(x, F):
        return Decimal(x.numerator) / Decimal(x.denominator)
    return Decimal(x)


def fracstr(x):
    return str(x.numerator) + '/' + str(x.denominator)


def serial(x):
    if isinstance(x, F):
        return fracstr(x)
    if isinstance(x, Decimal):
        return str(x)
    if isinstance(x, dict):
        return {k: serial(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [serial(v) for v in x]
    return x


def zero_matrix(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def certify_stochastic(P):
    assert all(x >= 0 for row in P for x in row)
    assert all(sum(row) == 1 for row in P)


def certify_balance(P, pi):
    n = len(pi)
    assert all(pi[i] * P[i][j] == pi[j] * P[j][i]
               for i in range(n) for j in range(n))


def rational_tree(D, m, a, k):
    n, alpha, beta, b = 2**a, F(1, 2), F(1, 2), F(63, 100)
    per_child = F(1, 2**(2*k))
    z, s = D * per_child, F(1, 4)
    assert per_child == s**k
    W_leaf = F(n*a*a)
    p = b*z**m*W_leaf
    q = [b*z**i for i in range(m+1)]
    pi = [p*F(1, n**(2*(m-i))) for i in range(m+1)]
    q.append(1-sum(q)); pi.append(1-sum(pi))
    assert min(q) > 0 and min(pi) > 0
    assert sum(q) == sum(pi) == 1
    W = [y/x for x, y in zip(q, pi)]
    assert all(W[i] < W[i+1] for i in range(m))
    assert W[m-1] < 1 < W[-1] < W[m] == W_leaf
    assert n*n/(D*s) >= 1 and D*s/F(n*n) <= 1
    # Exact KL admission: only leaf and star can contribute positively.
    # exp(.995) >= its positive 24th Taylor sum; .995+3*a*p<1.
    x = F(199, 200)
    exp_lower = sum((x**j/F(math.factorial(j)) for j in range(25)), F(0))
    assert q[-1]*exp_lower > 1
    kl_upper = x+3*a*p
    assert kl_upper < 1
    # log(W_leaf)=a log 2+2 log a <3a for integer a>=1.
    size = m+2
    G, L = zero_matrix(size), zero_matrix(size)
    for i in range(size):
        for j in range(size):
            if i != j:
                G[i][j] = q[j]*min(F(1), W[j]/W[i])
        G[i][i] = 1-sum(G[i])
    for i in range(m+1):
        if i < m:
            L[i][i+1] = F(D, D+1)*s
        if i:
            L[i][i-1] = F(1, D+1)*D*s/F(n*n)
        L[i][i] = 1-sum(L[i])
    L[-1][-1] = F(1)
    C = [[(F(i == j)+alpha*G[i][j]+beta*L[i][j])/2
          for j in range(size)] for i in range(size)]
    for P in (G, L, C):
        certify_stochastic(P); certify_balance(P, pi)
    f = beta*F(D, D+1)*s/2
    D0 = alpha*q[-1]/2
    E = f+alpha*(1-b)/2+alpha*b/F(2*(n*n-1))+f/F(n*n)
    exits = [1-C[i][i] for i in range(m)]
    assert all(D0 <= e <= E for e in exits)
    for i in range(m):
        assert C[i][i+1]-alpha*G[i][i+1]/2 == f
    for i in range(1, m+1):
        assert C[i][i-1]-alpha*G[i][i-1]/2 == f/F(n*n)
    em = alpha*(1-p)/(2*W_leaf)+f/F(n*n)
    assert 1-C[m][m] == em
    H = n//(2*m)
    wait_lower = max(F(0), 1-F(m)/(1+D0*H))
    retain_lower = max(F(0), 1-n*em)
    capture_lower = b*(f/E)**m*wait_lower*retain_lower
    tv_lower = capture_lower-p
    exact = dict(D=D, depth=m, n=n, log2_n=a, eta=F(1,k), b=b,
                 per_child_q_ratio=per_child, z=z, screen=s,
                 native_states=1+sum(D**i for i in range(m+1)),
                 quotient_states=size, q_level=q, pi_level=pi, W_level=W,
                 G=G, L=L, C=C, f=f, D0=D0, E=E, exits=exits,
                 leaf_escape=em, H=H, kl_upper_rational=kl_upper,
                 kl_taylor_margin=q[-1]*exp_lower-1,
                 waiting_factor_lower=wait_lower,
                 retention_factor_lower=retain_lower,
                 capture_lower=capture_lower, tv_lower=tv_lower)
    return exact


def matmul(A, B):
    n = len(A)
    return [[sum((A[i][k]*B[k][j] for k in range(n)), Decimal(0))
             for j in range(n)] for i in range(n)]


def rowmul(v, P):
    return [sum((v[i]*P[i][j] for i in range(len(v))), Decimal(0))
            for j in range(len(v))]


def propagate(q, P, n):
    v, A = list(q), P
    matrix_products = row_products = 0
    while n:
        if n & 1:
            v = rowmul(v, A); row_products += 1
        n >>= 1
        if n:
            A = matmul(A, A); matrix_products += 1
    return v, matrix_products, row_products


def diagnostics(exact, reserve):
    a = exact['log2_n']
    working = reserve + math.ceil(a*math.log10(2)) + 30
    with localcontext() as ctx:
        ctx.prec = working
        q = [dec(x) for x in exact['q_level']]
        pi = [dec(x) for x in exact['pi_level']]
        CG = {key: [[dec(x) for x in row] for row in exact[key]] for key in ('C','G')}
        laws, matrices, rows = {}, 0, 0
        for name, key, count in [('hybrid_n','C',exact['n']),
                                  ('pure_imh_n','G',exact['n']),
                                  ('pure_imh_n_over_4','G',exact['n']//4)]:
            law, mp, rp = propagate(q, CG[key], count)
            matrices += mp; rows += rp
            tv = sum((abs(x-y) for x,y in zip(law,pi)), Decimal(0))/2
            mass_error = abs(sum(law)-1)
            assert mass_error < Decimal(10)**(-reserve)
            assert min(law) >= 0
            laws[name] = dict(steps=count, law=law, tv=tv, mass_error=mass_error,
                              leaf_probability=law[-2])
        lower = dec(exact['tv_lower'])
        assert laws['hybrid_n']['tv'] >= lower-Decimal(10)**(-reserve)
        return dict(reserved_digits=reserve, working_digits=working,
                    laws=laws, exact_bound_decimal=lower,
                    matrix_products=matrices, row_products=rows)


def inverse_F(r):
    one = Decimal(1)
    if r >= one:
        return one
    lo, hi = Decimal(0), one
    for _ in range(4*__import__('decimal').getcontext().prec):
        mid = (lo+hi)/2
        if mid == lo or mid == hi:
            break
        value = mid*((one-mid).ln()*(one-mid)/mid).exp()
        if value < r:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2


def constants(precision):
    with localcontext() as ctx:
        ctx.prec = precision
        r0 = (-Decimal(1)).exp()
        cstar, old_chi = inverse_F(r0), inverse_F(2*r0)
        table = []
        for D in (2,4,16,64,256,4096):
            r = Decimal(37)/100*Decimal(D+1)/D
            c = inverse_F(r)
            table.append(dict(D=D,b='63/100',competition=r,exponent=c,
                              reciprocal=1/c,
                              optimizer_v=None if c==1 else -(1-c).ln()/c))
        assert 801**3 < 16*320**3
        return dict(precision=precision,K=1,alpha='1/2',r0=r0,cstar=cstar,
                    coefficient=1/cstar,old_path_chi=old_chi,
                    old_path_coefficient=1/old_chi,finite_D_table=table,
                    exact_lambda_1p5={'left':801**3,'right':16*320**3,
                                       'margin':16*320**3-801**3})


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--reserve',type=int,default=80)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--exact-inputs',type=Path)
    ap.add_argument('--resources',type=Path,required=True)
    args=ap.parse_args()
    t0,c0=time.perf_counter(),time.process_time()
    input_rows, results = [], []
    for params in CASES:
        exact=rational_tree(*params)
        input_rows.append(exact)
        results.append(dict(parameters=params,native_states=exact['native_states'],
                            quotient_states=exact['quotient_states'],
                            target_leaf=exact['pi_level'][-2],
                            kl_upper=exact['kl_upper_rational'],
                            **diagnostics(exact,args.reserve)))
    result=dict(scope='Exact finite admission/certificates; Decimal powers diagnostic only',
                constants=constants(args.reserve),cases=results)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(serial(result),indent=2)+'\n')
    if args.exact_inputs:
        args.exact_inputs.parent.mkdir(parents=True,exist_ok=True)
        args.exact_inputs.write_text(json.dumps(serial(input_rows),indent=2)+'\n')
    costs=dict(body_wall_seconds=time.perf_counter()-t0,
               body_cpu_seconds=time.process_time()-c0,
               peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               reserved_digits=args.reserve,cases=len(CASES),
               largest_native_states=max(x['native_states'] for x in input_rows),
               largest_quotient_states=max(x['quotient_states'] for x in input_rows),
               matrix_products=sum(x['matrix_products'] for x in results),
               row_products=sum(x['row_products'] for x in results),
               active_inference_cost='unknown',monetary_cost='unknown',
               prior_research_cost='not included',
               source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    args.resources.parent.mkdir(parents=True,exist_ok=True)
    args.resources.write_text(json.dumps(costs,indent=2)+'\n')
    print(json.dumps(costs,indent=2))


if __name__=='__main__':
    main()
