#!/usr/bin/env python3
"""Exact full-common-affine search on elementary mixed-parity profile loops."""
from fractions import Fraction as Q
from pathlib import Path
import json,sys,time
import sympy as S
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'incoming_resonant'))
from profile_algebra import add,scale,mul,cos,sin,meanprod,const,r,s,p,q,B

T=S.symbols('T',real=True)
L=Q(11,100)

def gap_poly(n,m, verts, widths):
    a=add(scale(cos(n),p),scale(cos(m),q)); c=add(scale(sin(n),p),scale(sin(m),q))
    b=add(scale(sin(n),-n*r),scale(sin(m),-m*s)); d=add(scale(cos(n),n*r),scale(cos(m),m*s))
    X=[add(x,const(bb)) for x,bb in zip([a,b,c,d],B)]
    a,b,c,d=X
    u=add(mul(a,a),mul(c,c));v=add(mul(b,b),mul(d,d));w=add(mul(a,b),mul(c,d));det=add(mul(a,d),scale(mul(b,c),-1))
    Favg=S.expand(meanprod(u,u)+meanprod(v,v)+4*meanprod(w,w)+S.Rational(339,100)*meanprod(det,det)-S.Rational(29,10)*meanprod(det,add(u,v)))
    B0,B1,B2,B3=B
    ub=B0**2+B2**2;vb=B1**2+B3**2;wb=B0*B1+B2*B3;qb=B0*B3-B1*B2
    Fbase=ub**2+vb**2+4*wb**2+S.Rational(339,100)*qb**2-S.Rational(29,10)*qb*(ub+vb)
    gap=0
    for (r0,s0),(r1,s1),h0 in zip(verts,verts[1:]+verts[:1],widths):
        h=S.Rational(h0.numerator,h0.denominator)
        sub={r:S.Rational(r0.numerator,r0.denominator)+T*S.Rational((r1-r0).numerator,(r1-r0).denominator),
             s:S.Rational(s0.numerator,s0.denominator)+T*S.Rational((s1-s0).numerator,(s1-s0).denominator),
             p:S.Rational((r1-r0).numerator,(r1-r0).denominator)/h,
             q:S.Rational((s1-s0).numerator,(s1-s0).denominator)/h}
        expr=S.expand((Favg-Fbase).subs(sub,simultaneous=True))
        gap+=h*S.integrate(expr,(T,0,1))
    g=S.Poly(S.expand(gap),*B)
    if g.total_degree()>2: raise ValueError('affine degree exceeded two')
    ex=g.as_expr();zero={x:0 for x in B}
    H=S.hessian(ex,B).subs(zero,simultaneous=True);bv=S.Matrix([S.diff(ex,x).subs(zero,simultaneous=True) for x in B]);c0=ex.subs(zero,simultaneous=True)
    if not all(H[:i,:i].det()>0 for i in range(1,5)):
        return {'status':'NONPOSITIVE_HESSIAN','H':str(H),'b':[str(x) for x in bv],'c':str(c0)}
    opt=-H.inv()*bv
    value=S.factor(c0+bv.dot(opt)/2)
    return {'status':'EXACT_FULL_AFFINE_OPTIMUM','optimized_gap':str(value),'B_opt':[str(x) for x in opt],
            'c_at_B0':str(c0),'third_moment_vector':[str(x) for x in bv],
            'H_ldl':[str(x) for x in H.LDLdecomposition(hermitian=False)[1].diagonal()]}

def main():
    t0=time.time(); axis=[Q(i,4) for i in range(-4,5)]
    widths=[Q(1,4),Q(1,2),Q(1),Q(2)]
    patterns=[[w]*4 for w in widths]+[[Q(1,4),Q(1,2),Q(1),Q(2)],[Q(2),Q(1),Q(1,2),Q(1,4)]]
    runs=[]
    for i in range(len(axis)-1):
      for j in range(len(axis)-1):
        x,y=axis[i],axis[j]
        verts=[(x,y),(axis[i+1],y),(axis[i+1],axis[j+1]),(x,axis[j+1])]
        for ws in patterns:
          ans=gap_poly(1,2,verts,ws)
          runs.append({'square_lower_left':[str(x),str(y)],'widths':[str(z) for z in ws],**ans})
    neg=[x for x in runs if x.get('optimized_gap') is not None and Q(x['optimized_gap'])<0]
    smallest=min((Q(x['optimized_gap']) for x in runs if x.get('optimized_gap') is not None),default=None)
    out={'integrand':'Fstar-(11/100)q^2','carrier_pair':[1,2],
         'scope':'all 64 axis-aligned elementary squares in [-1,1]^2 on (1/4)Z^2; each loop uses common B optimized over all four edges; widths are four common widths plus two cyclic varied-width patterns',
         'width_patterns':[[str(z) for z in row] for row in patterns], 'loop_count':len(runs),
         'exact_negative_fully_optimized_loops':len(neg),'smallest_optimized_gap':str(smallest),
         'runtime_seconds':time.time()-t0,'runs':runs}
    (ROOT/'full_affine_square_lattice_search.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='runs'},indent=2))
if __name__=='__main__': main()
