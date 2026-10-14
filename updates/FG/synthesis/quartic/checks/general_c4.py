#!/usr/bin/env python3
"""Fresh scalar C4 heat interface; no source snapshots or pickle are read.

General F=A(u^2+v^2)+Cuv+Ew^2+Lq(u+v).  The universal identity is exact.
No positivity or universal cone inclusion is asserted by this construction.
"""
from pathlib import Path
import json
import sympy as s

def build():
    a,b,c,d=s.symbols('a b c d',real=True);xx=s.Matrix([a,b,c,d])
    hh=s.symbols('h0:6',real=True)
    B1=s.Matrix([hh[0],hh[1],hh[3],hh[4]])
    B2=s.Matrix([hh[1],hh[2],hh[4],hh[5]])
    x=s.Matrix([a,c]);y=s.Matrix([b,d])
    X=s.Matrix([hh[0],hh[3]]);Y=s.Matrix([hh[1],hh[4]]);Z=s.Matrix([hh[2],hh[5]])
    cross=lambda p,q:p[0]*q[1]-p[1]*q[0]
    zp=s.Matrix([x.dot(X),x.dot(Z),y.dot(Y),cross(x,Y),cross(y,X),cross(y,Z)])
    zm=s.Matrix([-y.dot(Z),-y.dot(X),-x.dot(Y),cross(y,Y),cross(x,Z),cross(x,X)])
    u=x.dot(x);v=y.dot(y);w=x.dot(y);q=cross(x,y)
    A,C,E,L=s.symbols('A C E L',real=True)
    p=(A,C,E,L)
    F=A*(u*u+v*v)+C*u*v+E*w*w+L*q*(u+v)
    theta=s.Matrix([-c,-d,a,b]);zeta=s.Matrix([-b,a,-d,c]);theta_a=s.Matrix([-c,d,a,-b])
    forms=[(u+v)*theta,q*theta,(u+v)*zeta,q*zeta,(u-v)*theta_a]
    g=s.symbols('g0:21');alpha_co=s.symbols('c0:5')
    ij=[(i,j) for i in range(6) for j in range(i,6)]
    G=s.zeros(6)
    for (i,j),gg in zip(ij,g):G[i,j]=G[j,i]=gg
    alpha=sum((co*form for co,form in zip(alpha_co,forms)),s.zeros(4,1))
    Da=alpha.jacobian(xx);HF=s.hessian(F,xx)
    eq=s.expand((B1.T*HF*B1+B2.T*HF*B2+B1.T*(Da.T-Da)*B2-zp.T*G*zp-zm.T*G*zm)[0])
    mat,rhs=s.linear_eq_to_matrix(s.Poly(eq,*(tuple(xx)+hh)).coeffs(),g+alpha_co)
    sol=next(iter(s.linsolve((mat,rhs))))
    S=G.subs(dict(zip(g+alpha_co,sol)))
    alphaf=alpha.subs(dict(zip(g+alpha_co,sol)))
    free=sorted(set().union(*(v.free_symbols for v in sol))-set(p),key=str)
    assert len(free)==6
    assert s.expand(eq.subs(dict(zip(g+alpha_co,sol))))==0
    return dict(matrix=S,alpha=alphaf,free=free,parameters=p,coordinates=xx,jets=hh,zplus=zp,zminus=zm,
                B1=B1,B2=B2,basis=[u*u+v*v,u*v,w*w,q*(u+v)],q=q)

if __name__=='__main__':
    z=build()
    out={'scope':'exact universal scalar C4 heat identity, not positivity or inclusion theorem',
         'parameters':list(map(str,z['parameters'])),'free':list(map(str,z['free'])),
         'matrix':[[str(s.factor(v)) for v in row] for row in z['matrix'].tolist()],
         'primitive':[str(s.expand(v)) for v in z['alpha']]}
    Path(__file__).with_name('GENERAL_C4_INTERFACE.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS universal C4 scalar identity; free variables',out['free'])
    print(z['matrix'])
