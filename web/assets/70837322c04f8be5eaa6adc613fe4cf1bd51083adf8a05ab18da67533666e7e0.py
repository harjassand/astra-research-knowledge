#!/usr/bin/env python3
"""Exact rational specification compiler and small diagnostic."""
from fractions import Fraction as F
import pathlib,json,time,math
ROOT=pathlib.Path(__file__).resolve().parent
started=time.monotonic()
def plus(a,b):return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(a,s):return [[x*s for x in ar] for ar in a]
def eye(d):return [[F(int(i==j)) for j in range(d)] for i in range(d)]
def zeros(d):return scale(eye(d),0)
def tr(a):return sum(a[i][i] for i in range(len(a)))
def round_grid(x,q):
 y=x/q;k=y.numerator//y.denominator
 return (k+int(y-k>=F(1,2)))*q
def compile_povm(effects,e):
 m=len(effects);d=len(effects[0]);q=e/F(2*m*d);u=e/F(m);I=eye(d);S=zeros(d);N=[]
 for A in effects:
  B=[[round_grid(x,q) for x in ar] for ar in A]
  assert B==list(map(list,zip(*B)))
  for i in range(d):
   assert sum(abs(B[i][j]-A[i][j]) for j in range(d))<=u
  Ny=plus(B,scale(I,u));N.append(Ny);S=plus(S,Ny)
 den=1+2*e;out=[scale(A,1/den) for A in N]
 rem=plus(I,scale(S,-1/den));out.append(rem)
 assert all(sum(A[i][j] for A in out)==I[i][j] for i in range(d) for j in range(d))
 return out,{'e':str(e),'grid_q':str(q),'operator_shift_u':str(u),'proved_infinity_to_L1_error_upper':str(18*e),'original_outcomes':m,'compiled_outcomes':m+1}
def psd2(a):
 assert a[0][1]==a[1][0]
 assert a[0][0]>=0 and a[1][1]>=0 and a[0][0]*a[1][1]-a[0][1]*a[1][0]>=0

def canon(A,H):
 d=len(A[0]);out=[[0.0]*d for _ in range(d)]
 for a in A:
  p=float(tr(a)/d)
  if p==0:continue
  score=sum(float(a[i][j])*H[j][i] for i in range(d) for j in range(d))/d
  for i in range(d):
   for j in range(d):out[i][j]+=score*float(a[i][j])/p
 return out
# POVM is a mixture of Z and rational rotated-basis dephasings, plus one rare split.
rare=F(1,2**200)
Pz=[[F(1),F(0)],[F(0),F(0)]];Pzc=[[F(0),F(0)],[F(0),F(1)]]
Pr=[[F(9,25),F(12,25)],[F(12,25),F(16,25)]];Prc=plus(eye(2),scale(Pr,-1))
M=[scale(Pz,(1-rare)/2),scale(Pzc,F(1,2)),scale(Pr,F(1,2)),scale(Prc,F(1,2)),scale(Pz,rare/2)]
e=F(1,2**16);out,certificate=compile_povm(M,e)
for A in M+out:psd2(A)
# Gershgorin shift inequalities can be checked exactly in the small fixture.
u=e/len(M)
for A,B in zip(M,out[:-1]):
 N=scale(B,1+2*e);diff=plus(N,scale(A,-1));psd2(diff);psd2(plus(scale(eye(2),2*u),scale(diff,-1)))
probs=[tr(A)/2 for A in out];assert all(p>0 for p in probs)
preps=[scale(A,1/tr(A)) for A in out]
assert all(tr(A)==1 for A in preps)
maximum_observed=0.0
for k in range(101):
 angle=2*math.pi*k/101;z=math.cos(angle);x=math.sin(angle);H=[[z,x],[x,-z]]
 old=canon(M,H);new=canon(out,H);D=[[new[i][j]-old[i][j] for j in range(2)] for i in range(2)]
 # Difference is trace zero; normalized Schatten1 of real Hermitian 2x2 is radius.
 v=math.sqrt(((D[0][0]-D[1][1])/2)**2+D[0][1]**2)
 maximum_observed=max(maximum_observed,v);assert v<=float(18*e)+1e-12
# Output specifications are rational, exact normalized, and JSON serializable.
enc=lambda A:[[str(x) for x in r] for r in A]
max_bit=max(max(abs(x.numerator).bit_length(),x.denominator.bit_length()) for A in out+preps for r in A for x in r)
result={'status':'EXACT_SPECIFICATION_AND_DIAGNOSTIC_ONLY','certificate':certificate,'original_min_tau_probability':str(min(tr(A)/2 for A in M)),'compiled_min_tau_probability':str(min(probs)),'compiled_effects':[enc(A) for A in out],'compiled_preparations':[enc(A) for A in preps],'max_rational_entry_bit_length':max_bit,'exact_PSD_and_normalization_checks':True,'floating_test_scope':'101 real traceless unit contractions; theorem is INITIAL.txt proof','maximum_observed_infinity_to_L1_fixture_error':maximum_observed,'wall_seconds':time.monotonic()-started}
(ROOT/'povm_compiler_check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','certificate','original_min_tau_probability','compiled_min_tau_probability','max_rational_entry_bit_length','exact_PSD_and_normalization_checks','maximum_observed_infinity_to_L1_fixture_error','wall_seconds']},indent=2))
