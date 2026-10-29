#!/usr/bin/env python3
"""Exact arithmetic checks for the native switching-diffusion obstruction.

The all-path equivalence and response theorem are ordinary proofs in the
companion Markdown file. This executable verifies their finite algebraic
ingredients; it does not sample a native source or prove semigroup analysis.
Only the Python standard library is required.
"""
from fractions import Fraction as F
from functools import reduce
from pathlib import Path
import hashlib
import json


def mm(a, b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def mv(a, b):
    return [sum(x*y for x,y in zip(row,b)) for row in a]


def pmul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            c[i+j]+=x*y
    return c


def serial(x):
    if isinstance(x,F):
        return str(x)
    if isinstance(x,list):
        return [serial(t) for t in x]
    if isinstance(x,dict):
        return {k:serial(v) for k,v in x.items()}
    return x


def main():
    O=[[F(2,3),F(-1,3),F(2,3)],
       [F(-1,3),F(2,3),F(2,3)],
       [F(2,3),F(2,3),F(-1,3)]]
    I=[[F(i==j) for j in range(3)] for i in range(3)]
    one=[F(1)]*3
    a=list(map(F,[1,2,4])); at=mv(O,a)
    eps=F(1,10); c=F(10)
    assert mm(O,O)==I and mv(O,one)==one
    assert at==[F(8,3),F(11,3),F(2,3)]
    assert sum(x for x in a)==sum(x for x in at)
    assert sum(x*x for x in a)==sum(x*x for x in at)
    assert sum(x**3 for x in a)-sum(x**3 for x in at)==F(40,9)

    roots=a+at
    numerator=[F(0)]*6
    for i,x in enumerate(roots):
        term=[F(1)]
        for j,y in enumerate(roots):
            if i!=j:
                term=pmul(term,[F(1),y])
        sign=1 if i<3 else -1
        for k,v in enumerate(term):
            numerator[k]+=sign*x**3*v
    assert numerator==[F(40,9),F(560,27),F(560,27),F(0),F(0),F(0)]

    perturb=eps*max(abs(70-31*x) for x in a)/(1-eps*max(a))
    assert perturb==9 and -c+perturb==-1
    assert 1-eps*max(a)==F(3,5)
    assert 1-eps*max(at)==F(19,30)
    nmin=F(40,27)*(3-14*eps+14*eps*eps)
    dmax=reduce(lambda x,y:x*(1+eps*y),roots,F(1))
    dlo=nmin/dmax
    response_lo=5*eps**3*dlo/(2*(6+21*eps**2))
    assert nmin==F(116,45)
    assert dmax==F(479864,140625)
    assert dlo==F(90625,119966)
    assert response_lo==F(90625,297995544)

    point_checks=[]
    for name,co,si in [('0',F(1),F(0)),('pi/2',F(0),F(1)),
                       ('pi',F(-1),F(0)),('3pi/2',F(0),F(-1))]:
        psi=[1+eps*x*co for x in a]
        psit=mv(O,psi)
        dpsi=[-eps*x*si for x in a]
        d2psi=[-eps*x*co for x in a]
        D=[(d2psi[i]+c*sum(psi))/psi[i] for i in range(3)]
        W=[[(D[i] if i==j else F(0))-c for j in range(3)] for i in range(3)]
        Wt=mm(mm(O,W),O)
        assert mv(W,psi)==d2psi
        assert mv(Wt,psit)==mv(O,d2psi)
        q=[[(-W[i][j]*psi[j]/psi[i]) if i!=j else F(0)
            for j in range(3)] for i in range(3)]
        qt=[[(-Wt[i][j]*psit[j]/psit[i]) if i!=j else F(0)
             for j in range(3)] for i in range(3)]
        for i in range(3):
            for j in range(3):
                if i!=j:
                    assert q[i][j]>0 and qt[i][j]>0
                    assert psi[i]**2*q[i][j]==psi[j]**2*q[j][i]
                    assert psit[i]**2*qt[i][j]==psit[j]**2*qt[j][i]
        assert sum(x*x for x in psi)==sum(x*x for x in psit)
        point_checks.append({'angle':name,'q':q,'q_tilde':qt})

    proof=Path(__file__).with_name('REVERSIBLE_CONTINUOUS_PORT_COUNTEREXAMPLE.md')
    receipt={
        'status':'PASS',
        'scope':'Exact finite algebra; ordinary analytic proof separate; no physical samples.',
        'proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),
        'epsilon':eps,'rotation':O,'a':a,'a_tilde':at,
        'rational_DeltaS_numerator_coefficients':numerator,
        'global_W_tilde_offdiagonal_upper_bound':-c+perturb,
        'global_DeltaS_lower_bound':dlo,
        'third_time_derivative_quadratic_response_gap_lower_bound':response_lo,
        'response_lower_bound_decimal':float(response_lo),
        'pointwise_generator_checks':point_checks,
    }
    dest=Path(__file__).with_name('REVERSIBLE_CONTINUOUS_PORT_EXACT_CHECKS.json')
    dest.write_text(json.dumps(serial(receipt),indent=2)+'\n')
    print(json.dumps({'status':'PASS','response_coefficient_lower_bound':str(response_lo),
                      'decimal':float(response_lo),'receipt':str(dest.resolve())},indent=2))


if __name__=='__main__':
    main()
