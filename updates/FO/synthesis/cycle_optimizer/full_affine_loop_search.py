#!/usr/bin/env python3
"""Exact common-affine optimization for a few mixed-parity compatible loops."""
from fractions import Fraction as Q
from pathlib import Path
import json,sys,time
import sympy as S

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'incoming_resonant'))
from profile_algebra import add,scale,mul,cos,sin,meanprod,const,r,s,p,q,B

T=S.symbols('T',real=True)
lam=Q(11,100)

def expressions(n,m):
    a=add(scale(cos(n),p),scale(cos(m),q)); c=add(scale(sin(n),p),scale(sin(m),q))
    b=add(scale(sin(n),-n*r),scale(sin(m),-m*s)); d=add(scale(cos(n),n*r),scale(cos(m),m*s))
    X=[a,b,c,d]
    X=[add(x,const(bb)) for x,bb in zip(X,B)]
    a,b,c,d=X
    u=add(mul(a,a),mul(c,c));v=add(mul(b,b),mul(d,d));w=add(mul(a,b),mul(c,d));det=add(mul(a,d),scale(mul(b,c),-1))
    Favg=S.expand(meanprod(u,u)+meanprod(v,v)+4*meanprod(w,w)
                  +S.Rational(339,100)*meanprod(det,det)
                  -S.Rational(29,10)*meanprod(det,add(u,v)))
    B0,B1,B2,B3=B
    ub=B0**2+B2**2;vb=B1**2+B3**2;wb=B0*B1+B2*B3;qb=B0*B3-B1*B2
    Fbase=S.expand(ub**2+vb**2+4*wb**2+S.Rational(339,100)*qb**2-S.Rational(29,10)*qb*(ub+vb))
    N4=S.expand(meanprod(add(u,v),add(u,v)))
    N4=S.expand(N4.subs({bb:0 for bb in B},simultaneous=True))
    return Favg,Fbase,N4

def loop(n,m,vertices,widths):
    Favg,Fbase,N4=expressions(n,m)
    gap=0; n4=0
    total=Q(0)
    for (r0,s0),(r1,s1),h0 in zip(vertices,vertices[1:]+vertices[:1],widths):
        h=S.Rational(h0); t=T
        sub={r:S.Rational(r0)+t*(S.Rational(r1)-S.Rational(r0)),
             s:S.Rational(s0)+t*(S.Rational(s1)-S.Rational(s0)),
             p:(S.Rational(r1)-S.Rational(r0))/h,
             q:(S.Rational(s1)-S.Rational(s0))/h}
        gap+=h*S.integrate(S.expand((Favg-Fbase).subs(sub,simultaneous=True)),(t,0,1))
        n4+=h*S.integrate(S.expand(N4.subs(sub,simultaneous=True)),(t,0,1))
        total+=h0
    gap=S.Poly(S.expand(gap),*B)
    assert gap.total_degree()<=2
    g=gap.as_expr()
    zero={x:0 for x in B}
    H=S.hessian(g,B).subs(zero,simultaneous=True)
    bvec=S.Matrix([S.diff(g,x).subs(zero,simultaneous=True) for x in B])
    c0=g.subs(zero,simultaneous=True)
    if H.det()==0:
        return {'status':'SINGULAR_AFFINE_HESSIAN','H':str(H),'b':list(map(str,bvec)),'c':str(c0)}
    assert all(H[:i,:i].det()>0 for i in range(1,5))
    Bopt=-H.inv()*bvec
    optgap=S.factor(c0+(bvec.dot(Bopt))/2)
    return {'status':'EXACT_AFFINE_OPTIMUM','carrier_pair':[n,m],
            'vertices':[[str(x),str(y)] for x,y in vertices],
            'widths':[str(x) for x in widths],'total_width':str(total),
            'third_moment_vector_b':[str(x) for x in bvec],
            'common_Hessian':[[str(H[i,j]) for j in range(4)] for i in range(4)],
            'H_ldl_diagonal':[str(x) for x in H.LDLdecomposition(hermitian=False)[1].diagonal()],
            'constant_c':str(c0),'common_B_opt':[str(x) for x in Bopt],
            'fully_optimized_unnormalized_gap':str(optgap),
            'fully_optimized_normalized_gap':str(S.factor(optgap/S.Rational(total.numerator,total.denominator))),
            'fourth_gradient_integral':str(S.factor(n4)),
            'cubic_nonzero':bvec!=S.zeros(4,1)}

if __name__=='__main__':
    start=time.time(); square=Q(0)
    paths=[
      ('unit-square',[(Q(0),Q(0)),(Q(1),Q(0)),(Q(1),Q(1)),(Q(0),Q(1))],[Q(1)]*4),
      ('centered-square',[(Q(-1,2),Q(-1,2)),(Q(1,2),Q(-1,2)),(Q(1,2),Q(1,2)),(Q(-1,2),Q(1,2))],[Q(1)]*4),
      ('translated-square',[(Q(1),Q(1)),(Q(2),Q(1)),(Q(2),Q(2)),(Q(1),Q(2))],[Q(1)]*4),
      ('rectangle-varied-width',[(Q(0),Q(0)),(Q(1),Q(0)),(Q(1),Q(1,2)),(Q(0),Q(1,2))],[Q(1,2),Q(1),Q(2),Q(1,4)]),
    ]
    runs=[]
    for name,path,widths in paths:
        for n,m in [(1,2),(2,1)]:
            result=loop(n,m,path,widths);result['path_name']=name;runs.append(result)
    out={'integrand':'Fstar-(11/100)q^2','purpose':'bounded mixed-parity test; exact common affine optimization','runtime_seconds':time.time()-start,'runs':runs}
    (ROOT/'full_affine_loop_search.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
