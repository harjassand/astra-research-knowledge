"""Finite exact pure-B expectations versus the independently derived formula.

The finite chain is killed at B=0 or B=cap+1. This is a diagnostic only.
The all-state and critical-boundary proofs are in report.md.
"""

from decimal import Decimal, localcontext
from fractions import Fraction as Q


def killed_expected_deaths(beta, cap):
    A = [[Q(int(i == j)) for j in range(cap)] for i in range(cap)]
    rhs = [Q(0) for _ in range(cap)]
    for b in range(1, cap + 1):
        birth = beta*b
        death = Q(b*(b-1))
        p = birth/(birth+death)
        r = death/(birth+death)
        if b < cap:
            A[b-1][b] -= p
        if b >= 3:
            A[b-1][b-3] -= r
        rhs[b-1] = r
    for j in range(cap):
        pivot = next(i for i in range(j,cap) if A[i][j])
        A[j],A[pivot] = A[pivot],A[j]
        rhs[j],rhs[pivot] = rhs[pivot],rhs[j]
        x=A[j][j]
        A[j]=[v/x for v in A[j]]
        rhs[j]/=x
        for i in range(j+1,cap):
            f=A[i][j]
            if f:
                A[i]=[a-f*b for a,b in zip(A[i],A[j])]
                rhs[i]-=f*rhs[j]
    g=[Q(0)]*cap
    for i in range(cap-1,-1,-1):
        g[i]=rhs[i]-sum(A[i][j]*g[j] for j in range(i+1,cap))
    assert g[0]==g[1]
    for b in range(1,cap+1):
        gp=g[b] if b<cap else Q(0)
        gm=g[b-3] if b>=3 else Q(0)
        residual=beta*b*(gp-g[b-1])+b*(b-1)*(gm-g[b-1])+b*(b-1)
        assert residual==0
    return g[0]


def h_series(beta):
    with localcontext() as ctx:
        ctx.prec=60
        x=Decimal(beta.numerator)/Decimal(beta.denominator)
        term=Decimal(1)
        total=term/x
        for n in range(1,500):
            term*=(-2*x)/n
            add=term/(x+n)
            total+=add
            if n>20 and abs(add)<Decimal('1e-55'):
                break
        return (1+x*(2*x).exp()*total)/2


for beta in [Q(1,4),Q(1),Q(2)]:
    g=killed_expected_deaths(beta,30)
    hd=h_series(beta)
    gd=Decimal(g.numerator)/Decimal(g.denominator)
    assert abs(gd-hd)<Decimal('1e-9'), (beta,gd,hd)
    print('beta=',beta,'finite-cap expected deaths=',str(gd),'h formula=',str(hd),'absolute difference=',str(abs(gd-hd)))

with localcontext() as ctx:
    ctx.prec=50
    expected=(Decimal(2).exp()+1)/4
    assert abs(h_series(Q(1))-expected)<Decimal('1e-45')
print('PASS: exact capped Poisson identities and numerical expectation/formula comparisons.')
print('The cap comparisons are finite diagnostics; they do not prove the critical theorem.')
