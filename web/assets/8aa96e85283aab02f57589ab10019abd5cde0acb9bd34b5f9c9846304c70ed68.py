"""Exact finite same-reference counterexample to classical contraction transfer.

A classical ternary exclusion channel and a 3-dimensional quantum reference.
All density matrices have rational entries. SymPy isolates characteristic roots
with exact rational Sturm intervals; Fraction arithmetic bounds logarithms.
No floating-point arithmetic is used for the certificate's assertions.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import sympy as s
from exact_triangle_certificate import Interval, xlog, decimal_outer


def ff(x): return F(int(x.p),int(x.q))


def entropy_potential(a):
    poly=a.charpoly().as_poly()
    roots=poly.intervals(eps=s.Rational(1,10**32))
    assert sum(mult for _,mult in roots)==a.rows
    ans=Interval.of(0)
    for (lo,hi),mult in roots:
        assert lo>=0
        ans+=mult*xlog(Interval(ff(lo),ff(hi)))
    return ans


def block(u,q,off,rare):
    return (q*u*u.T).row_join(off*u).col_join((off*u.T).row_join(s.Matrix([[rare]])))


def main():
    n=10000;p=s.Rational(1,1+n*n);q=1-p;t=s.Rational(1,10)
    sqrt_pq=s.Rational(n,1+n*n)
    assert sqrt_pq**2==p*q
    us=[s.Matrix([s.Rational(1,2),0]),s.Matrix([0,s.Rational(1,2)]),s.Matrix([-s.Rational(1,2),-s.Rational(1,2)])]
    assert sum(us,s.zeros(2,1))==s.zeros(2,1)
    plus=[block(u,q,t*sqrt_pq,p/3) for u in us]
    minus=[block(u,q,-t*sqrt_pq,p/3) for u in us]
    mean=[block(u,q,s.Rational(0),p/3) for u in us]
    assert sum((s.trace(a) for a in plus))==1
    assert sum(plus,s.zeros(3))==sum(minus,s.zeros(3))==sum(mean,s.zeros(3))
    assert all((a+b)/2==c for a,b,c in zip(plus,minus,mean))
    assert all(s.trace(a)==s.trace(b)==s.trace(c) for a,b,c in zip(plus,minus,mean))
    # Each input block's nontrivial Schur complement is p(1/3-t^2)>0.
    assert p*(s.Rational(1,3)-t*t)>0
    # Sign flip is the same unitary on R, giving identical plus/minus spectra.
    flip=s.diag(1,1,-1)
    assert all(flip*a*flip==b for a,b in zip(plus,minus))
    def exclusion(arr): return [(sum(arr,s.zeros(3))-a)/2 for a in arr]
    outplus,outmean=exclusion(plus),exclusion(mean)
    ix=sum((entropy_potential(a) for a in plus),Interval.of(0))-sum((entropy_potential(a) for a in mean),Interval.of(0))
    iy=sum((entropy_potential(a) for a in outplus),Interval.of(0))-sum((entropy_potential(a) for a in outmean),Interval.of(0))
    assert ix.lo>0
    ratio=iy/ix
    assert ratio.lo>F(9,10) and ratio.hi<1
    result={'status':'PASS','scope':'Finite same-reference rational witness; not formal/general proof verification',
      'parameters':{'n':n,'p':str(p),'t':str(t)},'reference_dimension':3,
      'auxiliary':'uniform classical bit U, exactly independent of R and independently of X',
      'same_reference':'checked as exact rational matrix identity',
      'input_mutual_information':decimal_outer(ix,24),'output_mutual_information':decimal_outer(iy,24),
      'ratio':decimal_outer(ratio,18),'classical_coefficient':'1/2',
      'assertions':['input information > 0','output/input ratio > 9/10','ratio < 1','I(U;R)=0 exactly','I(U;X)=0 exactly'],
      'method':'Rational characteristic-polynomial root isolation; Fraction logarithm bounds with proved remainders'}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
