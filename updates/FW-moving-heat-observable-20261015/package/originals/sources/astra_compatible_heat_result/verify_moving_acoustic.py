#!/usr/bin/env python3
"""Verify the moving-acoustic heat certificate with exact rational arithmetic.

Usage:
  python verify_moving_acoustic.py [MOVING_ACOUSTIC_CERTIFICATE.json]

Requires Python 3.10+ and SymPy. No numerical optimizer, network, repository
checkout, pickle, or discovery script is used. A JSON verification receipt is
written beside the input. Algebraic checks do not replace analytic proof review.
"""
from __future__ import annotations
import hashlib
import json
import sys
from itertools import combinations, combinations_with_replacement
from pathlib import Path
import sympy as s


def require(condition: bool, description: str) -> None:
    if not condition:
        raise AssertionError(description)


def verify(path: Path) -> dict:
    data = json.loads(path.read_text(encoding='utf-8'))
    R = s.Rational
    r, t = s.symbols('r t', real=True)
    x = s.Matrix(s.symbols('a b c d', real=True))
    a,b,c,d = x
    z = s.Matrix(s.symbols('z0:6', real=True))
    B1 = s.Matrix([z[0],z[1],z[3],z[4]])
    B2 = s.Matrix([z[1],z[2],z[4],z[5]])
    Z = s.kronecker_product(x,z)
    pairs = list(combinations(range(4),2))
    monomials = list(combinations_with_replacement(range(4),2))
    require(data['omega_pair_order'] == [list(v) for v in pairs], 'two-form ordering')
    require(data['omega_monomial_order'] == [list(v) for v in monomials], 'monomial ordering')
    def load_matrix(name: str) -> s.Matrix:
        arr = data[name]
        blocks = [s.Matrix([[R(v) for v in row] for row in block]) for block in arr]
        shape = blocks[0].shape
        require(all(M.shape == shape for M in blocks), f'{name} dimensions')
        return sum((r**i*M for i,M in enumerate(blocks)),s.zeros(*shape))
    CN,SN,WN = [load_matrix(n) for n in ['C_numerator','S_numerator','omega_numerator']]
    require(CN.shape==(24,18) and SN.shape==(18,18) and WN.shape==(6,10), 'dimensions')
    require(SN==SN.T, 'symmetric Gram numerator')
    D1,D2 = map(R,data['diffusion'])
    require(D1>0 and D2>0,'positive diffusion')
    def heat(F):
        hh=s.hessian(F,x)
        return s.expand(D1*(B1.T*hh*B1)[0]+D2*(B2.T*hh*B2)[0])
    omega=s.zeros(4)
    mon=s.Matrix([x[i]*x[j] for i,j in monomials])
    for (i,j),p in zip(pairs,WN*mon):
        omega[i,j]=p; omega[j,i]=-p
    correction=(B1.T*omega*B2)[0]
    u=a*a+c*c; j=a*d-b*c
    H=((a-d)**2+(b+c)**2)**2
    F=3*H+r*(r-1)*u*u/6+j*j+r*u*j
    # C=CN/(r+1), S=-SN/(r+1), omega=-omega_num/(r+1).
    ell=CN.T*Z
    residual=s.expand((ell.T*SN*ell)[0]+(r+1)**3*heat(F)-(r+1)**2*correction)
    require(residual==0,'universal parameter-dependent polynomial identity')
    for i,k,l in combinations(range(4),3):
        require(s.expand(s.diff(omega[k,l],x[i])-s.diff(omega[i,l],x[k])+s.diff(omega[i,k],x[l]))==0,'closedness')
    alpha=omega.T*x/4
    for i,k in pairs:
        require(s.expand(s.diff(alpha[k],x[i])-s.diff(alpha[i],x[k])-omega[i,k])==0,'polynomial primitive')
    print('PASS: universal rational identity, closedness, and primitive',flush=True)
    eye=s.eye(18)
    v1=eye[:,0]-eye[:,12]+eye[:,16]
    v2=-eye[:,13]+eye[:,17]
    K=12*D1*v1*v1.T+12*D2*v2*v2.T
    require(s.expand((ell.T*K*ell)[0]-(r+1)**2*heat((a-d)**4))==0,'scalar subtraction identity')
    epsilon=R(data['scalar_subtraction_epsilon'])
    require(epsilon==R(1,2000),'specified epsilon')
    T=(SN+epsilon*(r+1)*K).applyfunc(s.expand)
    require(all(s.Poly(q,r).degree()<=3 for q in T if q!=0),'cubic positive matrix numerator')
    lo,hi=map(R,data['interval'])
    require(lo==R(-21,8) and hi==R(-5,2),'specified interval')
    require(lo<hi<-1,'denominator sign')
    Tt=T.subs(r,lo+(hi-lo)*t).applyfunc(s.expand)
    pc=[Tt.applyfunc(lambda q:s.Poly(q,t).nth(k)) for k in range(4)]
    Bs=[sum((pc[k]*s.binomial(i,k)/s.binomial(3,k) for k in range(i+1)),s.zeros(18)) for i in range(4)]
    recon=sum((s.binomial(3,i)*t**i*(1-t)**(3-i)*Bs[i] for i in range(4)),s.zeros(18))
    require((recon-Tt).applyfunc(s.expand)==s.zeros(18),'exact Bernstein identity')
    pivots=[]
    for i,M in enumerate(Bs):
        L,DD=M.LDLdecomposition(hermitian=False)
        require(L*DD*L.T==M,f'Bernstein matrix {i} LDL identity')
        pp=list(DD.diagonal())
        require(all(p>0 for p in pp),f'Bernstein matrix {i} positive')
        pivots.append([str(p) for p in pp])
    print('PASS: four rational Bernstein matrices, all 72 LDL pivots positive',flush=True)
    h,k=s.symbols('h k',real=True)
    avg=(h**4+k**4+((h+k)**4+(h-k)**4)/4)/4
    require(s.expand(avg-R(3,8)*(h*h+k*k)**2)==0,'four-rotation identity')
    kappa=R(data['rotationally_averaged_kappa'])
    require(kappa==R(3,8)*epsilon==R(3,16000),'averaged margin')
    require(kappa*R(4,1875)==R(1,2500000),'elliptic Jensen constant')
    G=3*H+R(35,24)*u*u+j*j-R(5,2)*u*j
    require(s.expand(F.subs(r,-R(5,2))-G)==0,'G basepoint')
    al,be,ga,de=s.symbols('alpha beta gamma delta',real=True)
    FF=al*H+be*u*u+ga*j*j+de*u*j
    point={a:1,b:-(r+1)*t,c:(r+1)*t,d:1}
    direction=s.Matrix([t,1,0,0])
    acoustic=(direction.T*s.hessian(FF.subs(de,ga*r),x).subs(point)*direction)[0]
    target=(12*be-2*ga*r*r+2*ga*r)*t*t+2*(r+1)**2*(2*be+ga*r)*t**4
    require(s.expand(acoustic-target)==0,'rank-one threshold necessity')
    require(s.expand(FF.subs({a:1,b:t,c:0,d:1})-FF.subs({a:1,b:0,c:0,d:1})-al*t**4)==0,'persistent acoustic degeneracy')
    GG=(direction.T*s.hessian(G,x).subs(point)*direction)[0]
    require(s.expand(s.Poly(GG,t).nth(2)-2*(r+R(5,2))**2)==0,'source-cone exclusion coefficient')
    FI=s.factor(F.subs({a:1,b:0,c:0,d:1}))
    FJ=s.factor(F.subs({a:1,b:0,c:0,d:-1}))
    require(s.expand(FI-(r+2)*(r+3)/6)==0,'negative conformal value')
    # Derivative signs give simple exact uniform endpoint bounds on the interval.
    require(s.diff(FI,r).subs(r,lo)<=0 and s.diff(FI,r).subs(r,hi)<=0,'FI monotonicity')
    require(s.diff(FJ,r).subs(r,lo)<0 and s.diff(FJ,r).subs(r,hi)<0,'FJ monotonicity')
    require(FI.subs(r,lo)==-R(5,128) and FJ.subs(r,lo)==R(6811,128),'uniform witness bounds')
    require(1600*(-R(5,128))+R(6811,128)==-R(1189,128),'negative lifted Jensen law')
    print('PASS: rotations, margin constant, acoustic boundary, and non-polyconvex witness',flush=True)
    receipt={
       'status':'EXACT_PASS',
       'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
       'sympy_version':s.__version__,
       'interval':[str(lo),str(hi)],
       'universal_identity':True,'closedness':True,'primitive':True,
       'subtraction_identity':True,'bernstein_identity':True,
       'bernstein_positive_pivots':pivots,
       'positive_pivot_count':72,'kappa':str(kappa),'integrated_margin':'1/2500000',
       'acoustic_threshold_identity':True,'source_positive_addition_exclusion':True,
       'uniform_four_atom_nonpolyconvexity_witness':True,
       'scope':'Exact finite algebra and analytic constants only; see RESEARCH_REPORT.md for the analytic theorem and external review limitations.'
    }
    return receipt

if __name__=='__main__':
    try:
        source=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('MOVING_ACOUSTIC_CERTIFICATE.json')
        receipt=verify(source)
        output=source.with_name('MOVING_ACOUSTIC_VERIFICATION.json')
        output.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
        print(f'EXACT_PASS; receipt: {output}')
    except Exception as exc:
        print(f'VERIFICATION FAILED: {exc}',file=sys.stderr)
        raise
