#!/usr/bin/env python3
"""Exact checks for PROFILE_CIRCULATION.md.
Dependencies: SymPy and the two bundled exact helper modules.
No optimizer or stored numerical certificate is used as input.
Run from this directory: python verify_circulation.py
These finite checks are not a formal verification of the analytic theorems.
"""
from __future__ import annotations
from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations_with_replacement
import json
import sympy as S
from profile_algebra import (averaged,poly_terms,polygon_integral,winding_moment,
                            cancelled_loop,square_loop,r,s,p,q,B)
from check_loop_examples import loop_moments,serial
from certify_profile_graph import certify
ROOT=Path(__file__).resolve().parent
checks=[];details={}
def passed(x):
 checks.append(x); print('PASS %02d: %s'%(len(checks),x),flush=True)
def zero(x):assert S.expand(x)==0

x=S.symbols('x0:4',real=True); bb=S.Matrix(B)
U=S.Matrix([S.Symbol('u0'),0,S.Symbol('u1'),0]); V=S.Matrix([0,S.Symbol('v0'),0,S.Symbol('v1')])
mons=[S.prod(x[j] for j in inds) for inds in combinations_with_replacement(range(4),4)]
for f in mons:
 df=S.Matrix([S.diff(f,z) for z in x])
 def val(z):return f.subs(dict(zip(x,z)),simultaneous=True)
 def grad(z):return df.subs(dict(zip(x,z)),simultaneous=True)
 R1=val(bb+V+U)-val(bb+V)-grad(bb+V).dot(U)
 R2=val(bb+V)-val(bb)-grad(bb).dot(V)
 zero(val(bb+V+U)-val(bb)-R1-R2-grad(bb+V).dot(U)-grad(bb).dot(V))
passed('two-column positive-remainder plus circulation identity: all 35 quartic monomials')

A,L,C=S.symbols('A L C',nonzero=True)
zero(A+L+C-A/3-(S.Rational(3,8)/A*(L+4*A/3)**2+C-3*L**2/(8*A)))
xn,yn=S.symbols('xn yn')
zero(xn*xn+yn*yn-(xn+yn)**2/2-(xn-yn)**2/2)
passed('rank-one quartic Bregman margin and the dimension-independent mu/6 margin')

# Pointwise profiles and their y derivatives: curvature is degree at most two.
e=S.Matrix(S.symbols('e0:2'));fprof=S.Matrix(S.symbols('f0:2'))
ep=S.Matrix(S.symbols('ep0:2'));fp=S.Matrix(S.symbols('fp0:2'))
base=bb+S.Matrix([0,r*ep[0]+s*fp[0],0,r*ep[1]+s*fp[1]])
E1=S.Matrix([e[0],0,e[1],0]);E2=S.Matrix([fprof[0],0,fprof[1],0])
for poly in mons:
 df=S.Matrix([S.diff(poly,z) for z in x]).subs(dict(zip(x,base)),simultaneous=True)
 ar=df.dot(E1);ass=df.dot(E2);curv=S.expand(S.diff(ass,r)-S.diff(ar,s))
 assert S.Poly(curv,*B,r,s).total_degree()<=2
passed('all 35 quartics: joint profile curvature is quadratic in background and amplitudes')

# Exact finite-difference loop: not a zero-current path.
path=cancelled_loop(); assert len(path)-1==46
moms={(i,j):winding_moment(path,i,j) for i in range(3) for j in range(3-i)}
assert all(v==0 for v in moms.values())
assert winding_moment(path,3,0)==-48
assert 4*winding_moment(path,3,0)==-192
# Check the translated-loop polynomial principle without relying on numerical cancellation.
t=S.Symbol('t');a0,a1,a2=S.symbols('a0 a1 a2')
g=a0+a1*t+a2*t*t
zero(sum(c*g.subs(t,j) for j,c in enumerate([1,-3,3,-1])))
details['area_moments']={str(k):str(v) for k,v in moms.items()}
details['higher_current']='integral r^4 ds = -192'
passed('eight oriented loops: all six quadratic signed-area moments vanish, higher current does not')

# Reconstruct G's exact acoustic certificate.
a,b,c,d=x;u=a*a+c*c;v=b*b+d*d;det=a*d-b*c
G=3*(u+v-2*det)**2+S.Rational(35,24)*u*u+det*det-S.Rational(5,2)*det*u
M11=S.hessian(S.diff(G,a,2),x)/2;M12=S.hessian(S.diff(G,a,b),x)/2;M22=S.hessian(S.diff(G,b,2),x)/2
K=S.zeros(4);pairs=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
for (i,j),vv in zip(pairs,[11,S.Rational(91,6),0,0,11,S.Rational(41,3)]):K[i,j]=vv;K[j,i]=-vv
Qm=M11.row_join(M12+K).col_join((M12-K).row_join(M22))
mi=[Qm[:j,:j].det() for j in range(1,7)]
assert mi==[S.Rational(107,2),642,S.Rational(1605,8),S.Rational(8445,16),S.Rational(2815,8),S.Rational(26865,4)]
T=Qm[:6,:6];UQ=Qm[:6,6:];assert Qm[6:,6:]-UQ.T*T.inv()*UQ==S.zeros(2)
details['G_Gram_minors']=[str(z) for z in mi]
passed('G: independent rational rank-six global acoustic certificate, not sampled rank-one tests')

# Full affine optimization for a genuinely circulating, quartic-current-cancelled field.
z=loop_moments(1,2,path)
assert z['b']!=S.zeros(4,1)
assert z['c']==S.Rational(797092,345)
assert z['n4']==S.Rational(191204,345)
assert z['gap']==S.Rational(73027952684,31894215)
assert z['gap']>=z['n4']/2
assert z['Bopt']==S.Matrix([-S.Rational(19549,92447),0,0,-S.Rational(96763,184894)])
details['eight_loop_field']=serial(z)
passed('exact compatible 46-strip, two-carrier field: nonzero cubic, full rational affine optimum')

sq=square_loop(Q(1),Q(1));z=loop_moments(1,3,sq);zr=loop_moments(1,3,sq[::-1])
assert z['C']==zr['C']==S.diag(S.Rational(1,2),S.Rational(145,12),S.Rational(1,2),S.Rational(145,12))
assert z['H']==zr['H'];assert z['b']==zr['b']==S.zeros(4,1)
assert z['gap']==S.Rational(119299,40);assert zr['gap']==S.Rational(106339,40)
assert z['gap']-zr['gap']==324
assert z['n4']==zr['n4']==S.Rational(25861,30)
details['oriented_pair']={'forward':serial(z),'reverse':serial(zr)}
passed('two compatible carrier interactions: identical covariance/H/b, signed fourth-order difference 324')

# Exact duration perspective identity; convexity is supplied analytically by rank-one convexity.
h=S.Symbol('h',positive=True);w=S.Symbol('w');cs=S.symbols('c0:5');ff=sum(cs[j]*w**j for j in range(5))
zero(S.diff(h*ff.subs(w,1/h),h,2)-S.diff(ff,w,2).subs(w,1/h)/h**3)
passed('edge-duration perspective identity: timing optimization is convex for the original rank-one-convex energy')

out=certify(save=True)
assert out['vertex_count']==81 and out['directed_edge_width_count']==32805
assert out['negative_raw_energy_edges']==104
assert out['negative_adjusted_edges']==2046
assert out['minimum_slack_integer']=='0'
assert out['most_negative_raw_edge']['energy']=='-1431/1280'
details['graph']={k:v for k,v in out.items() if k not in ('vertices','potential_numerators')}
passed('all 32,805 rational directed strip costs: telescoping calibration for every closed walk')

(ROOT/'circulation_verification.json').write_text(json.dumps({'status':'PASS','groups':checks,'details':details},indent=2))
print('WROTE circulation_verification.json;',len(checks),'groups passed.',flush=True)
