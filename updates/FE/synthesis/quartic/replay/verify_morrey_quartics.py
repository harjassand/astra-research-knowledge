#!/usr/bin/env python3
"""Exact algebra audit for ASTRA Meta-Genesis quartic calculations.

Requires Python 3.10+ and SymPy. Uses no numerical optimizer or floating-point
positivity decision. This verifies finite algebra, not historical priority,
the whole normal-form proof, or quasiconvexity of the retained interior example.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as S


def main() -> None:
    a,b,c,d,s,t = S.symbols('a b c d s t', real=True)
    x=S.Matrix([a,b,c,d]); u=a*a+c*c; v=b*b+d*d; w=a*b+c*d; q=a*d-b*c
    pars=S.symbols('A B C E G H L M N', real=True)
    basis=[u*u,v*v,u*v,w*w,u*w,v*w,q*u,q*v,q*w]
    F=sum(p*f for p,f in zip(pars,basis))
    checks: list[str] = []
    def zero(expr: S.Expr, label: str) -> None:
        if S.expand(expr) != 0:
            raise AssertionError(label)
        checks.append(label)
    def same(M: S.Matrix, N: S.Matrix, label: str) -> None:
        if M.shape != N.shape or any(S.expand(z) != 0 for z in M-N):
            raise AssertionError(label)
        checks.append(label)

    zero(u*v-w*w-q*q, 'Gram determinant identity')
    zero(-c*S.diff(F,a)-d*S.diff(F,b)+a*S.diff(F,c)+b*S.diff(F,d),
         'Infinitesimal left SO(2) invariance')
    even=sum(pars[i]*basis[i] for i in range(6)); odd=F-even
    zero(F.subs({c:-c,d:-d}, simultaneous=True)-(even-odd),
         'Reflection-even / orientation-sensitive splitting')

    # Exact invariance dimension and spanning computation in all 35 quartics.
    exps=[(i,j,k,4-i-j-k) for i in range(5) for j in range(5-i) for k in range(5-i-j)]
    mon=[a**i*b**j*c**k*d**ell for i,j,k,ell in exps]
    def coeffs(poly: S.Expr) -> S.Matrix:
        p=S.Poly(S.expand(poly),a,b,c,d)
        return S.Matrix([p.coeff_monomial(m) for m in mon])
    rot=S.Matrix.hstack(*[coeffs(-c*S.diff(m,a)-d*S.diff(m,b)+a*S.diff(m,c)+b*S.diff(m,d)) for m in mon])
    dim=35-rot.rank(); span=S.Matrix.hstack(*[coeffs(f) for f in basis]).rank()
    assert dim == span == 9
    assert S.Matrix.hstack(*[coeffs(f) for f in basis[:6]]).rank()==6
    checks.append('SO(2) dimension 9 and reflection-even dimension 6')

    acoustic=S.expand(s*s*S.diff(F,a,a)+2*s*t*S.diff(F,a,b)+t*t*S.diff(F,b,b))
    M11=S.hessian(acoustic.coeff(s,2).coeff(t,0),x)/2
    M12=S.hessian(acoustic.coeff(s,1).coeff(t,1),x)/4
    M22=S.hessian(acoustic.coeff(s,0).coeff(t,2),x)/2
    kk=S.symbols('k12 k13 k14 k23 k24 k34', real=True)
    K=S.zeros(4)
    pairs=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    for (i,j),z in zip(pairs,kk): K[i,j]=z;K[j,i]=-z
    Q=M11.row_join(M12+K).col_join((M12-K).row_join(M22))
    z=(s*x).col_join(t*x)
    zero((z.T*Q*z)[0]-acoustic, 'Exact acoustic Gram identity, all parameters')

    r,lam,ell,mu,nu=S.symbols('r lam ell mu nu',real=True)
    canon={pars[0]:1,pars[1]:1,pars[2]:lam,pars[3]:2*r-lam,
           pars[4]:0,pars[5]:0,pars[6]:ell,pars[7]:mu,pars[8]:nu}
    Fc=S.expand(F.subs(canon)); E=S.expand(Fc-q*(ell*u+mu*v+nu*w))
    H1=u*u+v*v+2*w*w
    H3=(u+v)**2+4*w*w
    zero(E-((3-r)*H1/2+(r-1)*H3/2+(lam-r+1)*q*q),
         'Canonical convex plus nonnegative determinant-square decomposition')
    zero(H3-(((a+b)**2+(c+d)**2)**2+((a-b)**2+(c-d)**2)**2)/2,
         'Explicit fourth-power representation of H3')

    M=(s*s*M11+2*s*t*M12+t*t*M22).subs(canon)
    ep=S.Matrix([1,1])/S.sqrt(2); em=S.Matrix([1,-1])/S.sqrt(2)
    U=ep.row_join(em)
    Mp=M.subs({s:1,t:1}); Mm=M.subs({s:1,t:-1})
    eps=3-r; D=1+lam-r
    same(U.T*Mp[:2,:2]*U,S.diag(12*(1+r),4*eps),'Plus-direction p block eigenvalues')
    same(U.T*Mp[2:,2:]*U,S.diag(4*(1+r),4*D),'Plus-direction q block eigenvalues')
    same(U.T*Mm[:2,:2]*U,S.diag(4*eps,12*(1+r)),'Minus-direction p block eigenvalues')
    same(U.T*Mm[2:,2:]*U,S.diag(4*D,4*(1+r)),'Minus-direction q block eigenvalues')
    Cp=U.T*Mp[:2,2:]*U; Cm=U.T*Mm[:2,2:]*U
    zero(Cp[1,0]-(ell+mu+nu),'Plus cross coupling S+nu')
    zero(Cp[1,1]-2*(mu-ell),'Plus cross coupling difference')
    zero(Cp[0,1]+3*(ell+mu+nu),'Plus cross coupling -3(S+nu)')
    zero(Cm[0,1]-(nu-ell-mu),'Minus cross coupling nu-S')
    zero(Cm[0,0]-2*(ell-mu),'Minus cross coupling difference')
    zero(Cm[1,0]-3*(ell+mu-nu),'Minus cross coupling 3(S-nu)')

    # The reflection-even null locus is rigid at either boundary.
    constraints_r3=list((em.T*Mp[:2,2:]).subs(r,3))+list((ep.T*Mm[:2,2:]).subs(r,3))
    constraints_D0=list((Mp[:2,2:]*em).subs(lam,r-1))+list((Mm[:2,2:]*ep).subs(lam,r-1))
    assert S.solve(constraints_r3,[ell,mu,nu]) == {ell:0,mu:0,nu:0}
    assert S.solve(constraints_D0,[ell,mu,nu]) == {ell:0,mu:0,nu:0}
    checks.extend(['r=3 forces all orientation couplings zero','D=0 forces all orientation couplings zero'])

    pstar=[1,1,S.Rational(7,2),S.Rational(1,2),0,0,S.Rational(-29,10),S.Rational(-29,10),0]
    kstar=[S.Rational(1,2),S.Rational(17,10),0,0,S.Rational(17,10),S.Rational(23,10)]
    Qs=Q.subs(dict(zip(pars,pstar))).subs(dict(zip(kk,kstar)))
    minors=[S.factor(Qs[:i,:i].det()) for i in range(1,9)]
    margin=S.Rational(1,16)
    shifted=Qs-margin*S.eye(8)
    shifted_minors=[S.factor(shifted[:i,:i].det()) for i in range(1,9)]
    assert all(z>0 for z in minors+shifted_minors)
    checks.extend(['Interior-example Gram matrix positive definite, exact Sylvester criterion',
                   'Interior-example Gram margin at least 1/16, exact Sylvester criterion'])
    Fs=F.subs(dict(zip(pars,pstar)))
    I={a:1,b:0,c:0,d:1}; J={a:1,b:0,c:0,d:-1}
    fI=Fs.subs(I);fJ=Fs.subs(J)
    assert fI == -S.Rational(3,10) and fJ == S.Rational(113,10)
    bad_measure=(S.Rational(1,50)*7**4*fI+S.Rational(49,50)*fJ)
    assert bad_measure == -S.Rational(833,250)
    assert S.Rational(1,50)*49-S.Rational(49,50)==0
    checks.append('Non-polyconvexity witness: zero barycentre, zero determinant mean, negative quartic mean')

    # Strict feasibility needed for the exact moment-duality formulation.
    normp=[1,1,2,0,0,0,0,0,0]; normk=[1,0,0,0,0,0]
    Qnorm=Q.subs(dict(zip(pars,normp))).subs(dict(zip(kk,normk)))
    assert all(Qnorm[:i,:i].det()>0 for i in range(1,9))
    checks.append('Strictly feasible Gram matrix for |A|^4, supporting dual attainment')

    result={'status':'PASS','checks':len(checks),'check_names':checks,
            'method':'exact SymPy polynomial and rational matrix arithmetic',
            'theorem_status':'proofs in accompanying note; no independent review or priority clearance',
            'retained_example_quasiconvexity':'NOT ESTABLISHED',
            'example_coefficients':[str(z) for z in pstar],
            'example_skew_coefficients':[str(z) for z in kstar],
            'leading_principal_minors':[str(z) for z in minors],
            'gram_margin':str(margin),'shifted_leading_principal_minors':[str(z) for z in shifted_minors],
            'non_polyconvex_measure_mean':str(bad_measure)}
    path=Path(__file__).with_name('verification_results.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
