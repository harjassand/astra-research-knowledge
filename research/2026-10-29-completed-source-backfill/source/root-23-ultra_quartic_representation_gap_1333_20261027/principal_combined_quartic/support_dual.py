"""Acquire and independently rationally verify a full26-feature SOS dual.
This excludes polynomial SOS minor support, NOT polyconvexity or QC.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,time,json
import numpy as np,cvxpy as cp,sympy as s
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'quartic_alternative'))
from poly_support import build

def exact_ldl(A):
    n=len(A);L=[[F(int(i==j)) for j in range(n)] for i in range(n)];D=[]
    for j in range(n):
        d=A[j][j]-sum((L[j][k]**2*D[k] for k in range(j)),F(0))
        assert d>0,(j,str(d));D.append(d)
        for i in range(j+1,n):
            L[i][j]=(A[i][j]-sum((L[i][k]*L[j][k]*D[k] for k in range(j)),F(0)))/d
    assert all(sum((L[i][k]*D[k]*L[j][k] for k in range(min(i,j)+1)),F(0))==A[i][j] for i in range(n) for j in range(n))
    return D

start=time.monotonic();coeff=(1,1,s.Rational(113,10),-s.Rational(83,10),0,0,4,-4,0)
_,_,terms,monoms,P,multipliers,z=build(coeff,multiplier='candidate')
lookup={e:i for i,e in enumerate(monoms)}
target=[F(dict(P.terms()).get(e,0)) for e in monoms]
A=[[F(dict(p.terms()).get(e,0)) for e in monoms] for p in multipliers]
indices=[]
for i in range(26):
    for j in range(26):
        p=s.Poly(z[i]*z[j],P.gens);assert len(p.terms())==1
        exponent,c=p.terms()[0];assert c==1
        indices.append(lookup[exponent])
lam=cp.Variable(len(monoms));margin=cp.Variable()
Y=cp.reshape(lam[indices],(26,26),order='C')
constraints=[np.array(A,float)@lam==0,Y >> margin*np.eye(26),cp.trace(Y)==1,
 np.array(target,float)@lam<=-margin]
problem=cp.Problem(cp.Maximize(margin),constraints)
problem.solve(solver='CLARABEL',max_iter=150,tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-10)
assert problem.status=='optimal' and margin.value>1e-8
np.savez(ROOT/'SUPPORT_DUAL_NUMERIC.npz',lam=lam.value,margin=margin.value)
# Project rounded rational suggestions onto the EXACT multiplier annihilator.
AA=s.Matrix(A);pivots=AA.rref()[1];assert len(pivots)==2
correction=AA[:,list(pivots)].inv()
attempts=[]
for denominator in (10**5,10**6,10**7,10**8,10**9):
    ell=[F(round(float(x)*denominator),denominator) for x in lam.value]
    residual=[sum((a*x for a,x in zip(row,ell)),F(0)) for row in A]
    delta=correction*s.Matrix(residual)
    for j,v in zip(pivots,delta):ell[j]-=F(v)
    assert all(sum((a*x for a,x in zip(row,ell)),F(0))==0 for row in A)
    moment=[[ell[indices[26*i+j]] for j in range(26)] for i in range(26)]
    pairing=sum((x*y for x,y in zip(ell,target)),F(0))
    try:
        assert pairing<0
        piv=exact_ldl(moment)
        break
    except AssertionError as error:attempts.append({'denominator':denominator,'rejected':str(error)[:150]})
else:raise AssertionError('exact reconstruction failed')
out={'status':'EXACT_STRICT_SOS_MINOR_SUPPORT_SEPARATOR',
 'input_nine_coefficients':list(map(str,coeff)),
 'polynomial':'u^2+v^2+3w^2+(113/10)q^2+4q(u-v)',
 'monomial_order':[list(e) for e in monoms],
 'variables':['A0','A1','A2','A3','X0','X1','X2','X3'],
 'lambda':list(map(str,ell)), 'multiplier_basis':['u-v','q'],
 'multiplier_pairings':['0','0'],'energy_pairing':str(pairing),
 'moment26':[[str(x) for x in row] for row in moment],
 'positive_ldl_pivots':list(map(str,piv)),
 'maximum_pivot_integer_bits':max(max(abs(x.numerator).bit_length(),x.denominator.bit_length()) for x in piv),
 'rounding_denominator':denominator,'rejected_reconstructions':attempts,
 'seconds':time.monotonic()-start,
 'scope':'Exact linear functional negative on the candidate Bregman polynomial, zero on both symmetry-reduced multiplier terms, positive on every26-feature SOS Gram. All-degree/symmetry reduction is an analytic premise in quartic_alternative/POLYCONVEX_PROOF.md; this alone is not non-polyconvexity or non-QC.'}
(ROOT/'EXACT_SUPPORT_SEPARATOR.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('lambda','monomial_order','moment26','positive_ldl_pivots')},indent=2))
