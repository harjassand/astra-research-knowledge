"""Construct rational supporting functionals exposing the two seed rays.

Sum 16 scalar acoustic evaluations, at four roots t and four output
vectors u. The root sum is evaluated exactly in the quotient algebra.
"""
from pathlib import Path
from functools import reduce
from math import gcd,lcm
import importlib.util
import json
import sympy as s

OUT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("face",OUT/"extreme_face.py")
f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
a,b,c,d,t=f.a,f.b,f.c,f.d,f.t

def expose(tau):
    B=1-3*tau*tau;H=1+3*tau*tau
    mod=s.Poly(B*B*(1-t*t)**2-(1-4*tau+3*tau*tau)*H*(1+t*t)**2,t).monic()
    K=s.Matrix([-B*(tau*(1-t*t)+H*t*t)*(1+t*t),
        B*t*(H-tau*(1-t*t))*(1+t*t),
        B*B*t*(1-t*t)-tau*H*t*(1+t*t)**2,
        B*B*t*t*(1-t*t)+tau*H*(1+t*t)**2
        ]).applyfunc(lambda v:s.rem(v,mod.as_expr(),t))
    C=-mod.nth(2)
    ell=[]
    for mon in f.monomials:
        total=0
        for x,y in ((1,0),(0,1),(1,1),(1,-1)):
            Ku=s.Matrix([x*K[0]-y*K[2],x*K[1]-y*K[3],
                         y*K[0]+x*K[2],y*K[1]+x*K[3]])
            hh=s.hessian(mon,f.av).subs(dict(zip(f.av,(x,x*t,y,y*t))),simultaneous=True)
            rem=s.Poly(s.rem(s.expand((Ku.T*hh*Ku)[0]),mod.as_expr(),t),t)
            total+=4*rem.nth(0)+2*C*rem.nth(2)
        ell.append(s.factor(total))
    common=lcm(*(v.q for v in ell));integers=[int(common*v) for v in ell]
    common_gcd=reduce(gcd,integers)
    integers=[v//common_gcd for v in integers]
    assert common_gcd>0
    T=sum(v*v for v in f.av);q=a*d-b*c;X=a*a+c*c-b*b-d*d
    F=T*T+4*(3-12*tau/H)*q*q+4*B/H*q*X
    def evaluate(poly):
        pp=s.Poly(s.expand(poly),*f.av)
        return sum(i*pp.coeff_monomial(m) for i,m in zip(integers,f.monomials))
    assert evaluate(F)==0
    assert evaluate(T*T)>0 and evaluate(q*q)>0
    record={'tau':str(tau),'monomial_powers':f.powers,'integer_exposing_functional':integers,
        'definition':'Positive scalar multiple of sum over t roots of m and u in {(1,0),(0,1),(1,1),(1,-1)} of K_u(t)^T Hessian_G(u tensor (1,t)) K_u(t).',
        'ell_F':str(evaluate(F)),'ell_T_squared':str(evaluate(T*T)),
        'ell_det_squared':str(evaluate(q*q)),
        'scale_from_raw_sum':str(s.Rational(common,common_gcd))}
    path=OUT/f'exposing_{tau.p}_{tau.q}.json'
    path.write_text(json.dumps(record,indent=2)+'\n')
    print(path.name,'ell(F)=',record['ell_F'],'ell(T^2)=',record['ell_T_squared'],flush=True)

if __name__=='__main__':
    expose(s.Rational(1,6));expose(s.Rational(1,30))
