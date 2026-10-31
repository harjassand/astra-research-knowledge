#!/usr/bin/env python3
"""Independently verify the SAME-acquired-H cubic attenuation negative control."""
from pathlib import Path
from fractions import Fraction as F
import json
from verify_projective import poly,unpack,ev,ff,add,mul,scale,shiftmono,ffpoly
HERE=Path(__file__).resolve().parent
x=json.loads((HERE/'frozen_exercise_results.json').read_text());row=x['cases'][0];rec=row['raw_recognition'];cert=row['certificate'];H=poly(cert['acquisition']['H']);G=poly(cert['acquisition']['G']);LH=poly(cert['acquisition']['LH'])
assert ev(G,(1,0,1))==-F(8,3)
base=json.loads((HERE/'frozen_results.json').read_text())['recognition'];internal=unpack(base)[4];L2={}
for a,c in H.items():
 for u,v,k in internal:
  L2=add(L2,scale(mul(ffpoly(u),add(shiftmono(a,tuple(y-z for z,y in zip(u,v))),{a:-F(1)})),c*k))
Nminus2={(0,0,0):-F(2),(1,0,0):F(1),(0,1,0):F(1),(0,0,1):F(1)}
assert LH==mul(Nminus2,L2)
raw=unpack(rec)[3];eps=F(cert['epsilon']);t=F(cert['t'])
def quotient(state,power):
 def h(z):return 1-eps*ev(H,z)/F((sum(z)+1)**power)
 out=F(0)
 for u,v,k in raw:
  rate=k*ff(state,u)
  if rate:
   y=tuple(a-b+c for a,b,c in zip(state,u,v));out+=rate*(t**(sum(v)-sum(u))*h(y)/h(state)-1)
 return out
for entry in x['essential_attenuation_negative_control']:
 state=entry['state'];bad=quotient(state,cert['degree']);good=quotient(state,cert['denominator_degree'])
 assert bad==F(entry['unattenuated_quotient'])>0 and good==F(entry['corrected_quotient'])<0
print(json.dumps({'same_acquired_H_exact_multiplier_verified':True,'leading_polynomial_at_1_0_1':'-8/3',
 'parent_negative_control_values_independently_recomputed':len(x['essential_attenuation_negative_control']),
 'corrected_and_unattenuated_denominator_powers':[cert['denominator_degree'],cert['degree']],
 'maximum_ray_parameter':10**50},indent=2))
