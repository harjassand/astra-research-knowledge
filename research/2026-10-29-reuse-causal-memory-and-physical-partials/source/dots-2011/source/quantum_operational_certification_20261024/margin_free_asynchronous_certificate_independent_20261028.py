#!/usr/bin/env python3
"""Exact complementary-dephasing phases and retained-operator coherent extraction."""
from fractions import Fraction as F
from pathlib import Path
import itertools,json
import sympy as s
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
def kron(xs):
 out=s.ones(1,1)
 for x in xs:out=s.kronecker_product(out,x)
 return out
def clean(M):return M.applyfunc(s.expand)
def rot(P,t):return ((1-t*t)*s.eye(P.rows)-2*s.I*t*P)/(1+t*t)
V=rot(kron([X,Y,Z]),s.Rational(1,5));Um=s.zeros(8);errs=[0,4,2,1]
for l,g in itertools.product(range(2),range(4)):Um[(7*l)^errs[g],4*l+g]=1
U=clean(V*Um);BX=clean(U*kron([X,s.eye(4)])*U.H);BZ=clean(U*kron([Z,s.eye(4)])*U.H)
G=s.eye(4)/4
phaseX={'I':G/2,'X':G/2,'Y':s.zeros(4),'Z':s.zeros(4)}
phaseZ={'I':G/2,'X':s.zeros(4),'Y':s.zeros(4),'Z':G/2}
phase_data=[]
for label,gs in [('X',phaseX),('Z',phaseZ)]:
 HX=gs['I']+gs['X']-gs['Y']-gs['Z'];HZ=gs['I']-gs['X']-gs['Y']+gs['Z']
 assert HX==(G if label=='X' else s.zeros(4))
 assert HZ==(G if label=='Z' else s.zeros(4))
 assert all(gs['I']-gg==s.zeros(4) or gs['I']-gg==G/2 for gg in gs.values())
 DX=clean(U*kron([X/2,HX])*U.H);DZ=clean(U*kron([Z/2,HZ])*U.H)
 assert DX==(BX/8 if label=='X' else s.zeros(8))
 assert DZ==(BZ/8 if label=='Z' else s.zeros(8))
 phase_data.append({'phase':label,'X_gap':'1/8' if label=='X' else '0','Z_gap':'1/8' if label=='Z' else '0','both_gaps_positive':False})
# A declared finite mean-level guard fixture: no source counts are manufactured.
b=F(1,16);retained={};stages=[]
for t,phase in [(0,'X'),(1,'X'),(2,'Z')]:
 a=F(1,128*2**t);e=5*a/4;guards={}
 for j in ['X','Z']:
  h=F(1,8) if j==phase else F(0)
  passed=h>e and 2*e<=b*(2*h-e)
  guards[j]=passed
  if passed and j not in retained:retained[j]=t
 assert not all(guards.values())
 stages.append({'stage':t,'phase':phase,'a':str(a),'e':str(e),'guards':guards,'retained':dict(retained)})
assert retained=={'X':1,'Z':2}
# The separately retained exact mean signs implement the actual three-gate SWAP.
CZ=clean(kron([(s.eye(8)+BZ)/2,I])+kron([(s.eye(8)-BZ)/2,X]))
CX=clean(kron([s.eye(8),s.diag(1,0)])+kron([BX,s.diag(0,1)]))
actual=clean(CZ*CX*CZ)
Swap=s.zeros(16)
for l,g,a in itertools.product(range(2),range(4),range(2)):Swap[(4*a+g)*2+l,(4*l+g)*2+a]=1
expected=clean(kron([U,I])*Swap*kron([U.H,I]))
assert actual==expected and actual.H*actual==s.eye(16)
# This operator identity certifies all payload/reference/gauge-memory inputs, not one occupied state.
result={'status':'PASS exact asynchronous certificates and coherent SWAP identity','source_draws':0,'rng_draws':0,'phase_sources':phase_data,'finite_mean_guard_stages':stages,'all_items_retained_at_stage':2,'any_single_stage_both_gaps':False,'exact_16_by_16_SWAP_entries_checked':256,'unknown_fixed_rational_entangling_mixer':True,'mean_level_fixture_not_sampled_acquisition':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
