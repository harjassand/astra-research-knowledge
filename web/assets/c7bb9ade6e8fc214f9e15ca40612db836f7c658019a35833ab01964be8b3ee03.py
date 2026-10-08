"""Exact, finite checks of the algebraic-log determinant ledger.

These fixtures do not prove moving-center interpolation or asymptotic
irrationality bounds. They test actual nonzero full-row minors, denominator
clearing, all algebraic conjugates through the norm, and rational parameter
inequalities. Written independently here; no source scripts executed.
"""
from __future__ import annotations
import json
import math
from fractions import Fraction
from pathlib import Path
import sympy as S
from sympy.polys.matrices import DomainMatrix

BASE=Path(__file__).resolve().parent
t,z=S.symbols('t z')

def matrix_fixture(name, root, b, q, p, H=5, w0=1, w1=2, v0=2,
                   theta=S.Rational(1,2), K=2, F0=6):
    F=S.QQ.algebraic_field(root)
    a=root
    v1=w1/theta
    T=math.ceil(S.Rational(F0*w1,v0))
    G=sum(S.Rational((-1)**(k+1),k)*t**k for k in range(1,T))
    L=S.ilcm(*range(1,T)) if T>2 else S.Integer(1)
    D=L**(H//w1)
    cols=[(h,g) for g in range(H//w1+1)
          for h in range((H-w1*g)//w0+1)]
    rows=[(j,s,be) for j in range(K)
          for be in range(math.ceil(H/v1))
          for s in range(math.ceil((H-v1*be)/v0))
          if v0*s+v1*be<H]
    raw=[];cleared=[]
    for j,s,be in rows:
        rr=[];cc=[]
        for h,g in cols:
            if be>g:
                val=S.Integer(0)
            else:
                coeff=S.expand((1+t)**h*(j*S.Rational(p,q)+G)**(g-be)).coeff(t,s)
                val=S.expand(a**(j*h)*S.binomial(g,be)*coeff)
            rr.append(val)
            cv=S.simplify(D*b**((K-1)*h)*S.Rational(q)**(g-be)*val)
            cc.append(cv)
            # Membership in Z[b*a], checked by reduction in its power basis.
            beta=b*a
            Fb=S.QQ.algebraic_field(beta)
            coordinate_coefficients=Fb.from_sympy(cv).to_list()
            assert all(c.denominator==1 for c in coordinate_coefficients), (name,j,s,be,h,g,cv)
        raw.append(rr);cleared.append(cc)
    RM=S.Matrix(raw); CM=S.Matrix(cleared)
    domain=DomainMatrix.from_Matrix(RM).convert_to(F)
    _,pivots=domain.rref()
    assert len(pivots)==len(rows),(name,len(rows),len(pivots))
    indices=list(pivots)
    minor=domain.extract(list(range(len(rows))),indices)
    de=F.to_sympy(minor.det())
    cminor=DomainMatrix.from_Matrix(CM[:,indices]).convert_to(F)
    cde=S.simplify(F.to_sympy(cminor.det()))
    SS=D**len(rows)
    for index in indices:
        h,g=cols[index];SS*=b**((K-1)*h)*S.Rational(q)**g
    for _,_,be in rows:SS*=S.Rational(q)**(-be)
    assert F.from_sympy(cde-SS*de)==F.zero
    # Norm via the exact resultant of the algebraic minimal polynomial.
    mpoly=S.Poly(S.minpoly(a,z),z).monic()
    cpoly=S.Poly.from_list([S.Rational(c) for c in F.from_sympy(cde).to_list()],z)
    upoly=S.Poly.from_list([S.Rational(c) for c in F.from_sympy(de).to_list()],z)
    # The algebraic field generator is exactly a for these expressions.
    nn=S.resultant(mpoly.as_expr(),cpoly.as_expr(),z)
    nu=S.resultant(mpoly.as_expr(),upoly.as_expr(),z)
    assert nn!=0 and nn.is_Integer
    assert S.simplify(nn-SS**mpoly.degree()*nu)==0
    return dict(name=name,alpha=str(a),minimal_polynomial=str(mpoly.as_expr()),
                b=b,q=q,p=p,H=H,weights=[w0,w1,v0,str(v1)],K=K,
                rows=len(rows),columns=len(cols),rank=len(pivots),
                selected_columns=[cols[i] for i in indices],truncation=T,
                lcm=int(L),entry_denominator_D=int(D),scaling=str(SS),
                unscaled_determinant=str(S.simplify(de)),
                scaled_determinant=str(cde),scaled_norm=str(nn),
                unscaled_norm=str(nu),all_scaled_entries_in_Z_balpha=True,
                exact_norm_and_scaling_identities=True)

def rational_parameters(d,nu):
    nu=Fraction(nu)
    beta=(Fraction(1,2)+1-Fraction(d,1)/nu)/2
    delta=min(Fraction(1,4),(2*beta-1)/(2*beta*beta))
    theta=1-delta; A=1-beta*delta
    C=(A/theta+1/A)/2
    B=(A+min(1/C,C*theta))/2
    gap0=nu*(A-theta)-d*(1-theta)
    eta=gap0/(4*nu*A)
    gap=nu*(A*(1-eta)-theta)-d*(1-theta)
    assert 0<theta<A<B<1 and C>1
    assert B<1/C and B<C*theta<1 and gap>0 and A*A<theta
    return {k:str(v) for k,v in dict(d=d,nu=nu,beta=beta,delta=delta,
                theta=theta,A=A,B=B,C=C,eta=eta,gap=gap,
                K_over_w0_base=C*B,v0_growth_base=C*theta/B,
                collision_growth_base=B/A).items()}

def bad_norm_shortcut():
    u=1+S.sqrt(2)
    records=[]
    for n in range(1,9):
        v=S.expand((S.sqrt(2)-1)**n)
        norm=S.simplify(v*v.xreplace({S.sqrt(2):-S.sqrt(2)}))
        assert abs(norm)==1
        records.append(dict(n=n,value=str(v),norm=str(norm),absolute_value=float(v.evalf())))
    return records

def rational_power_jet_valuations():
    records=[]
    for p,q in [(2,7),(4,9),(3,10),(7,12)]:
        for s in range(1,10):
            coeff=S.prod(S.Rational(p,q)-j for j in range(s))/S.factorial(s)
            for ell,exp in S.factorint(q).items():
                def val(n):
                    n=abs(int(n));r=0
                    while n and n%ell==0:n//=ell;r+=1
                    return r
                actual=val(S.numer(coeff))-val(S.denom(coeff))
                expected=-s*exp-val(S.factorial(s))
                assert actual==expected
                records.append(dict(p=p,q=q,s=s,prime=int(ell),valuation=int(actual)))
    return records

if __name__=='__main__':
    out={
        'scope':'Finite exact algebraic ledger checks; not asymptotic theorem verification',
        'fixtures':[
            matrix_fixture('nonintegral_shared_denominator_prime',(1+S.sqrt(2))/3,3,9,2),
            matrix_fixture('nonintegral_negative_conjugate',S.sqrt(2)/2,2,7,4),
            matrix_fixture('unit_with_small_negative_conjugate',1+S.sqrt(2),1,7,6),
            matrix_fixture('nonintegral_two_real_conjugates',(1+S.sqrt(5))/2,2,9,4),
            matrix_fixture('cubic_with_nonreal_conjugates',S.real_root(2,3),1,11,2),
        ],
        'rational_parameter_checks':[rational_parameters(d,Fraction(2*d)+eps)
             for d in [1,2,3,10] for eps in [Fraction(1),Fraction(1,10),Fraction(1,100)]],
        'false_integral_modulus_shortcut':bad_norm_shortcut(),
        'rational_power_jet_valuations':rational_power_jet_valuations(),
    }
    dst=BASE/'algebraic_log_exact_checks.json'
    dst.write_text(json.dumps(out,indent=2,default=int))
    print(json.dumps({'path':str(dst),'fixture_ranks':[(r['name'],r['rank']) for r in out['fixtures']],
           'parameter_schedules_checked':len(out['rational_parameter_checks']),
           'power_jet_valuations_checked':len(out['rational_power_jet_valuations'])},indent=2))
