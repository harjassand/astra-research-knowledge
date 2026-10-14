#!/usr/bin/env python3
"""Bounded exact facial reconstruction for a new C4 boundary input.

This tests the source's equality-face construction beyond its fixed slice.
No supplied snapshots, binary scientific code or pickle are loaded.
"""
from pathlib import Path
import json
import sympy as s
from general_c4 import build

OUT=Path(__file__).parent
zz=build();A,C,E,L=zz['parameters'];free=zz['free'];j=s.Symbol('j')
r=s.Rational(2);lam=s.Rational(4)
m=L**4-48*L**2+384
c0=3*(-3*L**2+8*lam)*(-L**2+16*r)
c1=-48*(r-1)*(L**2*lam-14*L**2-8*lam*r+24*lam+16*r*r+16*r)
c2=768*(r-1)**2*(L**2-lam*r-3*lam+r*r+4*r+3)
jp=s.expand(-c1*(1+j)**2-2*c2*j)
gb=s.groebner([m,jp],j,L,order='lex',domain=s.QQ)
print('Groebner',gb,flush=True)
def reduce(f):return gb.reduce(s.expand(f))[1]
v=L*L
AA=s.Matrix([[12+4*r*j,8*r*j,-2*j],[8*r,4*r+12*j,-1-3*j],[-2*v,-v*(1+3*j),4+2*lam*j]])
rhs=s.Matrix([-3-j,-2,-2*(2*r-lam)])
D=s.expand(AA.det());nums=(AA.adjugate()*rhs).applyfunc(s.expand)
rho,si,chi=nums
vp=s.Matrix([L*rho,L*j*rho,L*j*si,-j*chi,-D,-j*D])
vm=s.Matrix([-L*j*si,-L*si,-L*rho,-D,-j*chi,-chi])
Sgen=zz['matrix'].subs({A:1,C:lam,E:2*r-lam})
Sb=Sgen.subs({t:0 for t in free});Sm=[Sgen.diff(t) for t in free]
degree=s.degree(m,L)
mon=[L**d*j**e for e in range(2) for d in range(degree)]
def coeffvec(vec):
    ans=[]
    for f in vec:
        pp=s.Poly(reduce(f),j,L,domain=s.QQ)
        ans.extend(pp.coeff_monomial(mm) for mm in mon)
    return s.Matrix(ans)
target=coeffvec((-Sb*vp).col_join(-Sb*vm))
cols=[]
for T in Sm:
    for d in range(degree):cols.append(coeffvec((L**d*T*vp).col_join(L**d*T*vm)))
MM=s.Matrix.hstack(*cols)
sol=s.linsolve((MM,target));sol=next(iter(sol))
unfixed=set().union(*(v.free_symbols for v in sol))
print('face linear shape',MM.shape,'rank',MM.rank(),'free',sorted(map(str,unfixed)),flush=True)
if unfixed:sol=[v.subs({t:0 for t in unfixed}) for v in sol]
tvals=[sum(sol[i*degree+d]*L**d for d in range(degree)) for i in range(6)]
def redL(f):return s.rem(s.Poly(s.expand(f),L,domain=s.QQ),s.Poly(m,L)).as_expr()
SS=Sgen.subs(dict(zip(free,tvals))).applyfunc(redL)
assert (SS*vp).applyfunc(reduce)==s.zeros(6,1)
assert (SS*vm).applyfunc(reduce)==s.zeros(6,1)
print('tau',tvals,flush=True);print('S',SS,flush=True)
lo=s.Rational(318490086807,10**11);hi=s.Rational(318490086808,10**11)
assert s.Poly(m,L).count_roots(lo,hi)==1
def interval(f):
    lower=upper=s.Rational(0)
    for c in s.Poly(f,L,domain=s.QQ).all_coeffs():
        p=[lower*lo,lower*hi,upper*lo,upper*hi]
        lower=min(p)+c;upper=max(p)+c
    return lower,upper
T=SS[2:,2:];B=SS[:2,2:];CC=SS[:2,:2]
mins=[redL(T[:i,:i].det()) for i in range(1,5)]
bounds=[interval(v) for v in mins]
print('Tminor bounds',[[float(v) for v in z] for z in bounds],flush=True)
assert all(l>0 for l,h in bounds)
assert (mins[-1]*CC-B*T.adjugate()*B.T).applyfunc(redL)==s.zeros(2)
print('PASS exact rank-four heat certificate for lambda=4 boundary.',flush=True)
out={'scope':'new independently derived r=2 lambda=4 endpoint, not the full C4 cone',
     'root_polynomial':str(m),'root_interval':[str(lo),str(hi)],'tau_free_names':list(map(str,free)),
     'tau_values':list(map(str,tvals)),'matrix':[[str(v) for v in row] for row in SS.tolist()],
     'T_minor_bounds':[[str(a),str(b)] for a,b in bounds],'schur_zero':True,'status':'EXACT_PASS'}
(OUT/'C4_LAMBDA4_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
