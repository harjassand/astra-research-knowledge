#!/usr/bin/env python3
"""Exact checks for a failed inverse-path chaotic-response mechanism.

No network, jobs, simulation fitting, or invariant-density oracle is used.
The main checks use rational arithmetic; logarithmic display uses 90 digits.
Run: python verify.py
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import sys
import time
import sympy as sp
import mpmath as mp

HERE = Path(__file__).resolve().parent
start = time.perf_counter()
checks = {}

def mv(A, x):
    return [sum((a*b for a,b in zip(row,x)), F(0)) for row in A]
def add(*xs):
    return [sum(t,F(0)) for t in zip(*xs)]
def scale(c,x):
    return [c*a for a in x]
def rational_matrix(M):
    return [[F(str(x)) for x in row] for row in M]
def as_float(x):
    return float(x)

P = rational_matrix([['.9','.4'],['.1','.6']])
D = rational_matrix([['-1','0'],['1','0']])
r = [sum(row) for row in P]
Q = [[x/rj for x in row] for row,rj in zip(P,r)]
K = [[P[j][i]**2/Q[j][i] for i in range(2)] for j in range(2)]
B = [[P[j][i]*D[j][i]/Q[j][i] for i in range(2)] for j in range(2)]
C = [[D[j][i]**2/Q[j][i] for i in range(2)] for j in range(2)]
h = [F(8,5),F(2,5)]
checks['two_state_stationarity'] = mv(P,h)==h and sum(h)==2
Qstar = [[P[j][i]*h[i]/h[j] for i in range(2)] for j in range(2)]
checks['exact_twist_rows'] = all(sum(row)==1 for row in Qstar)
checks['moment_matrix'] = K==rational_matrix([['1.17','.52'],['.07','.42']])
variance_constants = []
absolute_constants = []
for j in range(2):
    scores=[D[j][i]/P[j][i] for i in range(2)]
    mu=sum(Q[j][i]*scores[i] for i in range(2))
    variance_constants.append(r[j]**2*(sum(Q[j][i]*scores[i]**2 for i in range(2))-mu**2))
    absolute_constants.append(min(Q[j])*r[j]*abs(scores[0]-scores[1]))
checks['conditional_variance_constants'] = variance_constants==[F(4,9),F(6)]
checks['conditional_absolute_constants'] = absolute_constants==[F(4,9),F(1)]

# Independent exact enumeration verifies all moment recursions for n=1,...,8.
enumeration=[]
for n in range(1,9):
    vals=[]
    for j0 in range(2):
        EW=EZ=EW2=EW2S=EZ2=F(0)
        for path in product(range(2), repeat=n):
            cur=j0; prob=F(1); w=F(1); s=F(0)
            for nxt in path:
                prob*=Q[cur][nxt]
                w*=P[cur][nxt]/Q[cur][nxt]
                s+=D[cur][nxt]/P[cur][nxt]
                cur=nxt
            EW+=prob*w; EZ+=prob*w*s; EW2+=prob*w*w
            EW2S+=prob*w*w*s; EZ2+=prob*w*w*s*s
        vals.append([EW,EZ,EW2,EW2S,EZ2])
    f=[F(1)]*2; df=[F(0)]*2; a=[F(1)]*2; b=[F(0)]*2; c=[F(0)]*2
    for k in range(n):
        f,df=mv(P,f),add(mv(P,df),mv(D,f))
        a,b,c=mv(K,a),add(mv(K,b),mv(B,a)),add(mv(K,c),scale(2,mv(B,b)),mv(C,a))
    enumeration.append(all(vals[j]==[f[j],df[j],a[j],b[j],c[j]] for j in range(2)))
checks['exact_enumeration_n1_to_n8'] = all(enumeration)

# Exact first and second moments, not Monte Carlo estimates.
rows=[]
f=[F(1)]*2; df=[F(0)]*2; a=[F(1)]*2; b=[F(0)]*2; c=[F(0)]*2
for n in range(1,501):
    f,df=mv(P,f),add(mv(P,df),mv(D,f))
    a,b,c=mv(K,a),add(mv(K,b),mv(B,a)),add(mv(K,c),scale(2,mv(B,b)),mv(C,a))
    exact_response=F(8,5)-(F(8,5)+F(3,5)*n)*F(1,2)**n
    assert df[1]/2==exact_response
    if n in [1,2,5,10,20,30,50,100,200,500]:
        rows.append({'n':n,'response_mean':float(df[1]/2),
                     'response_variance':float((c[1]-df[1]**2)/4),
                     'exact_truncation_bias':float(F(8,5)-exact_response),
                     'weight_second_moment':float(a[1])})
checks['all_500_exact_response_means'] = True

# Symbolic certificate valid throughout 0 <= delta <= 1/100.
d=sp.symbols('delta',nonnegative=True)
B2=sp.Matrix([[sp.Rational(9,10),sp.Rational(2,5)], [sp.Rational(1,10),sp.Rational(3,5)]])
A=(1-d)*B2+d*sp.ones(2)/2
rr=A*sp.ones(2,1)
KK=sp.diag(*rr)*A
v=sp.Matrix([1,sp.Rational(7,80)])
polys=[sp.expand(x) for x in KK*v-sp.Rational(6,5)*v]
expected=[sp.Rational(939,8000)*d*d-sp.Rational(6313,8000)*d+sp.Rational(31,2000),
          sp.Rational(939,8000)*d*d+sp.Rational(2557,8000)*d+sp.Rational(7,4000)]
checks['symbolic_super_eigenvector_polynomials']=polys==expected
# First polynomial decreases on interval and remains positive at right endpoint;
# the second has nonnegative coefficients and positive constant.
checks['uniform_growth_certificate']=bool(sp.diff(polys[0],d).subs(d,sp.Rational(1,100))<0 and polys[0].subs(d,sp.Rational(1,100))>0 and all(c>=0 for c in sp.Poly(polys[1],d).all_coeffs()))

mp.mp.dps=90
horizon_rows=[]
for delta in [F(1,100),F(1,1000)]:
    # Exact native matrix, solve invariant measure and its response from scratch.
    PP=sp.diag(B2,B2)*(1-sp.Rational(delta.numerator,delta.denominator))+sp.ones(4)*sp.Rational(delta.numerator,delta.denominator)/4
    DD=sp.Matrix([-1,-1,1,1])*sp.ones(1,4)*sp.Rational(delta.numerator,delta.denominator)/4
    I=sp.eye(4)
    E=I-PP
    Aeq=E.copy(); Aeq[3,:]=sp.ones(1,4)
    rhs=sp.zeros(4,1);rhs[3]=1
    pi=Aeq.inv()*rhs
    rhs2=DD*pi;rhs2[3]=0
    dpi=Aeq.inv()*rhs2
    assert PP*pi==pi and sum(pi)==1 and sum(dpi)==0
    assert (I-PP)*dpi==DD*pi
    assert dpi[2]+dpi[3]==sp.Rational(1,2)
    # Actual map validity and endpoint tests: each source cell is partitioned,
    # and each branch maps exactly onto the declared target cell.
    endpoint_ok=True
    for i in range(4):
        left=sp.Rational(i,4)
        for j in range(4):
            width=PP[j,i]/4
            def branch_map(x): return sp.Rational(j,4)+(x-left)/PP[j,i]
            endpoint_ok &= branch_map(left)==sp.Rational(j,4)
            endpoint_ok &= branch_map(left+width)==sp.Rational(j+1,4)
            left+=width
        endpoint_ok &= left==sp.Rational(i+1,4)
    assert endpoint_ok
    # Parameter interval positivity and expansion, affine extrema suffice.
    for theta in [-sp.Rational(1,2),sp.Rational(1,2)]:
        Ptheta=PP+theta*DD
        assert all(0<x<sp.Rational(9,10) for x in Ptheta)
        assert all(sum(Ptheta[:,i])==1 for i in range(4))
    eps=F(1,1000)
    dd=mp.mpf(delta.numerator)/delta.denominator
    n=int(mp.ceil(mp.log(2*mp.mpf(eps.numerator)/eps.denominator)/mp.log(1-dd)))
    # Rational horizon verification, no floating-point decision.
    assert F(1,2)*(1-delta)**n<=eps
    assert F(1,2)*(1-delta)**(n-1)>eps
    # Conservative variance bound for the macro-observable single-path estimator.
    coeff=F(119,16000)*delta
    logvar=mp.log10(mp.mpf(coeff.numerator)/coeff.denominator)+(n-1)*mp.log10(mp.mpf(6)/5)
    logM=logvar-2*mp.log10(mp.mpf(eps.numerator)/eps.denominator)
    horizon_rows.append({'delta':str(delta),'epsilon':str(eps),'minimum_horizon':n,
                        'response_exact':'1/2','pi_exact':[str(x) for x in pi],
                        'dpi_exact':[str(x) for x in dpi],
                        'log10_response_variance_lower':mp.nstr(logvar,30),
                        'log10_independent_paths_for_sd_epsilon_lower':mp.nstr(logM,30),
                        'exact_map_endpoint_tests':bool(endpoint_ok)})
checks['four_state_exact_physical_response_and_map']=True
checks['exact_horizons_and_variance_bounds']=True

# Exact inequalities behind conditional gradient-variance bound.
checks['gradient_variance_constant']=F(7,10)/2-F(1,100)>=F(17,50)
checks['macro_variance_prefactor']=F(1,4)*F(17,50)*F(7,80)==F(119,16000)

out={'scope':'route-specific failure; not a lower bound for all chaotic-response algorithms',
     'all_checks_passed':all(checks.values()),'checks':checks,
     'two_state_exact_moment_table':rows,
     'four_state_certified_stress_tests':horizon_rows,
     'growth_polynomials':[str(p) for p in polys],
     'software':{'python':sys.version.split()[0],'sympy':sp.__version__,'mpmath':mp.__version__,'platform':platform.platform()},
     'elapsed_seconds':time.perf_counter()-start,
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
assert out['all_checks_passed']
