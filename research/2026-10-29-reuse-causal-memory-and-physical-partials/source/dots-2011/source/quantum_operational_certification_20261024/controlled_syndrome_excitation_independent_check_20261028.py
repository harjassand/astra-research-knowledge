#!/usr/bin/env python3
"""Exact physical pre-noise injection check with unknown mixers and actual feedback labels."""
import itertools,json
from pathlib import Path
from math import lcm
import sympy as s
import numpy as np
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);Ps=[I,X,Y,Z]
def kron(xs):
 r=s.ones(1,1)
 for x in xs:r=s.kronecker_product(r,x)
 return r
def clean(M):return M.applyfunc(s.expand)
def rot(P,t):return ((1-t*t)*s.eye(P.rows)-2*s.I*t*P)/(1+t*t)
def nums(M,D):
 rr=np.empty(M.shape,dtype=object);ii=np.empty(M.shape,dtype=object)
 for a,b in itertools.product(range(M.rows),range(M.cols)):
  r=s.re(M[a,b])*D;j=s.im(M[a,b])*D;assert r.q==j.q==1;rr[a,b]=int(r);ii[a,b]=int(j)
 return rr,ii
enc=s.zeros(8,2);enc[0,0]=1;enc[7,1]=1
es=[0,4,2,1];Um=s.zeros(8)
for l,g in itertools.product(range(2),range(4)):Um[(7*l)^es[g],4*l+g]=1
errs=[kron([X if (f>>(2-k))&1 else I for k in range(3)]) for f in range(8)]
vs=[rot(kron([X,Y,Z]),s.Rational(1,5)),clean(rot(kron([Z,Z,X]),s.Rational(2,9))*rot(kron([X,I,Y]),s.Rational(1,7)))]
ps=[s.Rational(0),s.Rational(1,13),s.Rational(1,4),s.Rational(2,5),s.Rational(1,2)]
def physical(E,p,V,injections):
 w=[p**f.bit_count()*(1-p)**(3-f.bit_count()) for f in range(8)]
 out=s.zeros(8);code=enc*E*enc.H
 for e in injections:
  for f in range(8):out+=w[f]*(errs[f]*errs[e]*code*errs[e].H*errs[f].H)/len(injections)
 return clean(V*out*V.H)
fixtures=[];entries=0;swap_entries=0
for vi,V in enumerate(vs):
 U=clean(V*Um);assert clean(U.H*U)==s.eye(8)
 BX=clean(U*kron([X,s.eye(4)])*U.H);BZ=clean(U*kron([Z,s.eye(4)])*U.H)
 # Actual coherent extraction, using the same fixed operators for both source roles.
 CZ=clean(kron([(s.eye(8)+BZ)/2,I])+kron([(s.eye(8)-BZ)/2,X]));CX=clean(kron([s.eye(8),s.diag(1,0)])+kron([BX,s.diag(0,1)]))
 Swap=s.zeros(16)
 for l,g,a in itertools.product(range(2),range(4),range(2)):Swap[(4*a+g)*2+l,(4*l+g)*2+a]=1
 assert clean(CZ*CX*CZ)==clean(kron([U,I])*Swap*kron([U.H,I]));swap_entries+=256
 for p in ps:
  t=1-2*p
  q0=(1-p)**2*(1+2*p)/4;q1=(1-p)*(1-p+2*p*p)/4;q2=p*(2-3*p+2*p*p)/4;q3=p*p*(3-2*p)/4
  AI=s.diag(q0,q1,q1,q1);AX=s.diag(q3,q2,q2,q2);HZ=AI-AX
  assert AI+AX==s.eye(4)/4
  assert HZ==s.diag((3*t-t**3)/8,*([(t+t**3)/8]*3)) and all(x>=0 for x in HZ.diagonal())
  gamma=(t+t**3)/16;native=p*(1-p)*(1-2*p)/2
  cal_loss=(3*p-3*p*p+2*p**3)/2;pay_loss=3*p*p-2*p**3
  assert s.trace(AX)==cal_loss
  assert cal_loss-pay_loss==s.Rational(3,2)*p*(1-p)*(1-2*p)
  assert gamma-native==t*(3*t*t-1)/16
  if 0<p<s.Rational(1,2):assert gamma/native==(1+t*t)/(2*(1-t*t))
  GI=s.diag(*[p**e.bit_count()*(1-p)**(3-e.bit_count()) for e in es])
  GX=s.diag(*[p**(3-e.bit_count())*(1-p)**e.bit_count() for e in es])
  for a,b in itertools.product(range(2),repeat=2):
   E=s.zeros(2);E[a,b]=1
   actual_cal=physical(E,p,V,es);model_cal=clean(U*(kron([E,AI])+kron([X*E*X,AX]))*U.H)
   actual_pay=physical(E,p,V,[0]);model_pay=clean(U*(kron([E,GI])+kron([X*E*X,GX]))*U.H)
   assert actual_cal==model_cal and actual_pay==model_pay;entries+=128
   # Both role channels decode under the SAME U, with their different advertised logical losses.
   for out,loss in [(actual_cal,cal_loss),(actual_pay,pay_loss)]:
    mid=clean(U.H*out*U);red=s.zeros(2)
    for l,m in itertools.product(range(2),repeat=2):red[l,m]=sum(mid[4*l+g,4*m+g] for g in range(4))
    assert clean(red)==clean((1-loss)*E+loss*X*E*X)
  assert physical(I/2,p,V,es)==s.eye(8)/8
  fixtures.append({'mixer':vi,'p':str(p),'calibration_gap':str(gamma),'native_gap':str(native),'gap_improved':bool(gamma>native),'calibration_oracle_loss':str(cal_loss),'payload_oracle_loss':str(pay_loss)})
# One full exact ordinary feedback law, explicitly retaining and summing all four injection labels.
p=s.Rational(1,13);V=vs[0];U=clean(V*Um);t=1-2*p
HZ=s.diag((3*t-t**3)/8,*([(t+t**3)/8]*3))
outputs={}
for j,sgn,e in itertools.product([1,3],[-1,1],es):outputs[j,sgn,e]=physical((I+sgn*Ps[j])/2,p,V,[e])
D=1
for out in outputs.values():
 for v in out:D=lcm(D,int(s.re(v).q),int(s.im(v).q))
meas=[]
for axes,bits in itertools.product(itertools.product([1,2,3],repeat=3),itertools.product([-1,1],repeat=3)):
 pis=[(I+b*Ps[a])/2 for a,b in zip(axes,bits)]
 mr,mi=nums(kron(pis),8);zr,zi=nums(kron([3*pi-I for pi in pis]),8);meas.append((mr,mi,zr,zi))
accum={j:[np.zeros((8,8),dtype=object),np.zeros((8,8),dtype=object)] for j in [0,1,3]};probtotal=0;events=0
for (j,sgn,e),out in outputs.items():
 rr,ii=nums(out,D)
 for mr,mi,zr,zi in meas:
  prob=int(np.sum(rr*mr.T-ii*mi.T));imag=int(np.sum(rr*mi.T+ii*mr.T));assert imag==0 and prob>=0
  probtotal+=prob;events+=1
  accum[0][0]+=prob*zr;accum[0][1]+=prob*zi
  accum[j][0]+=2*sgn*prob*zr;accum[j][1]+=2*sgn*prob*zi
# Axis/sign 1/4, injection 1/4, readout axes 1/27; both measurement and shadow denominators 8.
assert probtotal==D*8*16*27;den=D*8*16*27*8
for j,target in [(0,s.eye(8)/8),(1,clean(U*kron([X/2,s.eye(4)/4])*U.H)),(3,clean(U*kron([Z/2,HZ])*U.H))]:
 rr,ii=nums(target,den);assert np.array_equal(accum[j][0],rr) and np.array_equal(accum[j][1],ii)
out={'status':'PASS exact physical injection/channel/feedback/common-U checks','source_draws':0,'rng_draws':0,'unknown_rational_entangling_mixers':len(vs),'noise_and_mixer_cases':len(fixtures),'calibration_and_payload_matrix_entries':entries,'same_U_actual_SWAP_entries':swap_entries,'explicit_injection_preparation_readout_Born_events':events,'exact_feedback_common_output_denominator':str(D),'fixtures':fixtures}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='fixtures'},indent=2))
