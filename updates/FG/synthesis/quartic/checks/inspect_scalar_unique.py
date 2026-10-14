#!/usr/bin/env python3
"""Acquire a nonzero real-rank minor for the scalar forced-face obstruction."""
import json
from pathlib import Path
import numpy as np
import sympy as s
from general_c4 import build

z=build();A,C,E,L=z['parameters'];j=s.Symbol('j');v=L*L
m=L**4-48*L**2+384
gb=s.groebner([m,j*j+(s.Rational(3,8)*v-8)*j+1],j,L,order='lex',domain=s.QQ)
red=lambda f:gb.reduce(s.expand(f))[1]
AA=s.Matrix([[12+8*j,16*j,-2*j],[16,8+12*j,-1-3*j],[-2*v,-v*(1+3*j),4+8*j]])
n=AA.adjugate()*s.Matrix([-3-j,-2,0]);ra,rb,rc=n.applyfunc(red);D=red(AA.det())
vp=s.Matrix([L*ra,L*j*ra,L*j*rb,-j*rc,-D,-j*D]).applyfunc(red)
vm=s.Matrix([-L*j*rb,-L*rb,-L*ra,-D,-j*rc,-rc]).applyfunc(red)
Sg=z['matrix'].subs({A:1,C:4,E:0})
MM=s.Matrix.hstack(*[(Sg.diff(t)*vp).col_join(Sg.diff(t)*vm) for t in z['free']]).applyfunc(red)
kn=float(s.sqrt(24-8*s.sqrt(3)));jn=float((3*s.sqrt(3)-1-s.sqrt(24-6*s.sqrt(3)))/2)
Mnum=np.array(MM.subs({L:kn,j:jn}),float)
rows=[]
for i in range(12):
    if np.linalg.matrix_rank(Mnum[rows+[i],:],tol=1e-8)>len(rows):rows.append(i)
assert len(rows)==6
det=red(MM[rows,:].det(method='domain-ge'))
print('rows',rows,'det reduced',s.factor(det),flush=True)
Kexact=s.sqrt(24-8*s.sqrt(3));Jexact=(3*s.sqrt(3)-1-s.sqrt(24-6*s.sqrt(3)))/2
scale=10**40
lcenter=int(s.N(Kexact*scale,70));jcenter=int(s.N(Jexact*scale,70))
llo=s.Rational(lcenter-1,scale);lhi=s.Rational(lcenter+2,scale)
jlo=s.Rational(jcenter-1,scale);jhi=s.Rational(jcenter+2,scale)
assert s.Poly(m,L).count_roots(llo,lhi)==1
def box(poly):
    lower=upper=s.Rational(0)
    for cc in s.Poly(poly,L).all_coeffs():
        cl=cu=s.Rational(0)
        for c in s.Poly(cc,j).all_coeffs():
            p=[cl*jlo,cl*jhi,cu*jlo,cu*jhi];cl=min(p)+c;cu=max(p)+c
        p=[lower*llo,lower*lhi,upper*llo,upper*lhi]
        lower=min(p)+cl;upper=max(p)+cu
    return lower,upper
jp=j*j+(s.Rational(3,8)*v-8)*j+1
assert box(jp.subs(j,jlo))[0]>0
assert box(jp.subs(j,jhi))[1]<0
bd=box(det);print('root j',jn,'det bound',list(map(float,bd)),flush=True)
assert bd[0]>0 or bd[1]<0
out={'rows':rows,'L_interval':[str(llo),str(lhi)],'j_interval':[str(jlo),str(jhi)],
     'determinant':str(det),'determinant_interval':list(map(str,bd))}
Path(__file__).with_name('SCALAR_UNIQUENESS.json').write_text(json.dumps(out,indent=2)+'\n')
