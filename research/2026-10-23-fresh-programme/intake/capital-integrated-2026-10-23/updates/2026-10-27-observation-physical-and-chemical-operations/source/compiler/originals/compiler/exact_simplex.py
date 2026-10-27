"""Ordinary exact primal simplex with Bland's anti-cycling rule.

Contract: max c*x subject to A*x<=b and x>=0, rational b>=0.
The known feasible all-zero point avoids a phase-I implementation.
Finite exact arithmetic and Bland's rule give termination for bounded LPs.
This implementation has no polynomial pivot/bit-runtime guarantee.
"""
from fractions import Fraction as F


def solve(A,b,c):
    m,n=len(b),len(c)
    if len(A)!=m or any(len(row)!=n for row in A):raise ValueError('bad LP dimensions')
    if any(v<0 for v in b):raise ValueError('all-zero point must be feasible')
    tab=[[F(v) for v in row]+[F(int(i==j)) for j in range(m)]+[F(b[i])] for i,row in enumerate(A)]
    tab.append([-F(v) for v in c]+[F(0)]*(m+1))
    basis=list(range(n,n+m));pivots=0;max_bits=0
    while True:
        entering=next((j for j,v in enumerate(tab[-1][:-1]) if v<0),None)
        if entering is None:break
        candidates=[(tab[i][-1]/tab[i][entering],basis[i],i) for i in range(m) if tab[i][entering]>0]
        if not candidates:raise ValueError('LP unbounded')
        leaving=min(candidates)[2];pivot=tab[leaving][entering]
        tab[leaving]=[v/pivot for v in tab[leaving]]
        for i in range(m+1):
            if i==leaving:continue
            mult=tab[i][entering]
            if mult:tab[i]=[a-mult*b for a,b in zip(tab[i],tab[leaving])]
        basis[leaving]=entering;pivots+=1
        max_bits=max(max_bits,max(max(v.numerator.bit_length(),v.denominator.bit_length()) for row in tab for v in row))
    x=[F(0)]*n
    for i,j in enumerate(basis):
        if j<n:x[j]=tab[i][-1]
    dual=tab[-1][n:n+m];obj=tab[-1][-1]
    if not (all(v>=0 for v in x+dual) and all(sum(a*v for a,v in zip(row,x))<=rhs for row,rhs in zip(A,b))):
        raise ArithmeticError('invalid exact primal or dual nonnegativity')
    if not all(sum(A[i][j]*dual[i] for i in range(m))>=c[j] for j in range(n)):
        raise ArithmeticError('invalid exact dual')
    if sum(c[j]*x[j] for j in range(n))!=obj or sum(b[i]*dual[i] for i in range(m))!=obj:
        raise ArithmeticError('unequal exact objectives')
    return obj,x,dual,{'pivots':pivots,'maximum_tableau_integer_bits':max_bits}
