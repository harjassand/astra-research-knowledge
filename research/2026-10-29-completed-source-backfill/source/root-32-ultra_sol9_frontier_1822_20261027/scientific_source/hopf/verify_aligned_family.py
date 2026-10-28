#!/usr/bin/env python3
"""Symbolic identities for the exact infinite family, plus literal replay.

Sympy is used to verify polynomial identities for arbitrary parameters;
the main finite target has the separate standard-library-only verifier.
"""
import json,time
from pathlib import Path
import sympy as S

OUT=Path(__file__).resolve().parent

def main():
    start=time.perf_counter()
    m,t,beta,r,s=S.symbols('m t beta r s',real=True)
    bm=(m*m-1)/(m*m+1)
    def literal(M):
        a,b,c,d=list(M);T=a*a+b*b+c*c+d*d
        q=a*d-b*c;x=a*a+c*c-b*b-d*d
        return S.expand(T*T+4*(r-1)*q*q+4*beta*q*x)
    A=S.eye(2);Rp=S.Matrix([[0,m],[-1,0]]);Rm=S.diag(1,-2)
    pp=S.Poly(literal(Rp+t*A).subs({r:4,beta:bm}),t)
    pm=S.Poly(literal(Rm+t*A).subs({r:4,beta:bm}),t)
    assert pp.coeff_monomial(t)==0
    upper=S.factor(pp.coeff_monomial(t*t)/m)
    lower=S.factor((pm.coeff_monomial(t*t)-pm.coeff_monomial(t)**2/(4*pm.coeff_monomial(1)))/(-2))
    assert S.factor(upper-24-16*m/(m*m+1))==0
    assert S.factor(lower-2*(297*bm*bm+603*bm+268)/(24*bm+73))==0
    P=2*m**4-388*m**3-905*m**2-196*m-313
    assert S.factor(lower-upper-4*P/((m*m+1)*(97*m*m+49)))==0
    shifted=S.Poly(S.expand(P.subs(m,t+197)),t)
    assert all(x>0 for x in shifted.all_coeffs())
    # Exact acoustic determinant and its optimization derivative.
    N11=1-beta*beta*s
    N22=2*r-1-3*beta*beta*s
    det=S.expand(N11*N22-4*beta*beta*(1-s))
    expected=3*beta**4*s*s+2*beta*beta*(1-r)*s+2*r-1-4*beta*beta
    assert S.expand(det-expected)==0
    required=(1+3*beta*beta*s+4*beta*beta*(1-s)/(1-beta*beta*s))/2
    assert S.factor(det-2*N11*(r-required))==0
    assert S.factor(S.diff(required,s)-beta*beta*(S.Rational(3,2)-2*(1-beta*beta)/(1-beta*beta*s)**2))==0
    # At r=4, an unconstrained lower bound is enough for strict positivity.
    assert S.factor(det.subs(r,4)-3*beta**4*(s-1/(beta*beta))**2-4*(1-beta*beta))==0
    data={'status':'PASS','scope':'exact symbolic identities; analytic positivity in ALIGNED_FAMILY.md',
          'upper':str(upper),'lower':str(lower),'gap':str(S.factor(lower-upper)),
          'P_shifted_coefficients_descending':[str(x) for x in shifted.all_coeffs()],
          'm200_beta':str(bm.subs(m,200)),
          'm200_gap':str((lower-upper).subs(m,200)),
          'ROC_determinant':str(det),'elapsed_seconds':time.perf_counter()-start}
    (OUT/'ALIGNED_FAMILY_REPLAY.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))

if __name__=='__main__':main()
