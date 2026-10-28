#!/usr/bin/env python3
"""Exact margin-free alternating-source and ordinary Born-law witness; no draws."""
from pathlib import Path
from math import lcm
import itertools,json
import sympy as s
import numpy as np
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
P=[I,X,Y,Z]
def kron(xs):
 out=s.ones(1,1)
 for x in xs:out=s.kronecker_product(out,x)
 return out
def clean(M):return M.applyfunc(s.expand)
def rot(pa,t):return ((1-t*t)*s.eye(pa.rows)-2*s.I*t*pa)/(1+t*t)
def matnum(M,D):
 re=np.empty(M.shape,dtype=object);im=np.empty(M.shape,dtype=object)
 for a,b in itertools.product(range(M.rows),range(M.cols)):
  rr=s.re(M[a,b])*D;ii=s.im(M[a,b])*D
  assert rr.q==1 and ii.q==1
  re[a,b]=int(rr);im[a,b]=int(ii)
 return re,im
Gmix=rot(kron([X,Y]),s.Rational(1,4));P0=s.simplify(Gmix*s.diag(1,1,0,0)*Gmix.H);P1=s.eye(4)-P0
assert P0*P0==P0 and P1*P1==P1 and P0*P1==s.zeros(4) and s.trace(P0)==2
V=rot(kron([X,Y,Z]),s.Rational(1,5))*rot(kron([Z,I,X]),s.Rational(1,7))
Um=s.zeros(8);es=[0,4,2,1]
for l,g in itertools.product(range(2),range(4)):Um[(7*l)^es[g],4*l+g]=1
U=clean(V*Um);assert s.simplify(U.H*U-s.eye(8))==s.zeros(8)
BX=clean(U*s.kronecker_product(X,s.eye(4))*U.H);BZ=clean(U*s.kronecker_product(Z,s.eye(4))*U.H)
outs={};Ds={};kernel_tests=0
for t,Pt in enumerate([P0,P1]):
 GI=(s.eye(4)+Pt)/8;GZ=(s.eye(4)-Pt)/8;HX=GI-GZ;HZ=GI+GZ
 assert HZ==s.eye(4)/4 and HX==Pt/4 and s.trace(GI)==s.Rational(3,4) and s.trace(GZ)==s.Rational(1,4)
 assert GI-GZ==HX
 # Exact negative expectation on the omitted rank-two subspace for any positive kappa.
 omitted=s.eye(4)-Pt
 for kap in [s.Rational(1,1000),s.Rational(1,7),s.Rational(1)]:
  assert s.trace(omitted*(HX-kap*HZ))/2==-kap/4
  kernel_tests+=1
 Ds[t,1]=clean(U*s.kronecker_product(X/2,HX)*U.H)
 Ds[t,3]=clean(U*s.kronecker_product(Z/2,HZ)*U.H)
 assert s.simplify(Ds[t,1]*Ds[t,1]-U*s.kronecker_product(I/4,Pt/16)*U.H)==s.zeros(8)
 for j,sgn in itertools.product([1,3],[-1,1]):
  inp=(I+sgn*P[j])/2
  out=clean(U*(s.kronecker_product(inp,GI)+s.kronecker_product(Z*inp*Z,GZ))*U.H)
  assert s.trace(out)==1
  outs[t,j,sgn]=out
assert (Ds[0,1]+Ds[1,1])/2==BX/16
assert (Ds[0,3]+Ds[1,3])/2==BZ/8
assert s.simplify((BX/16)**2-s.eye(8)/256)==s.zeros(8) and s.simplify((BZ/8)**2-s.eye(8)/64)==s.zeros(8)
parity_cases=0
for N,start in itertools.product([2,4,6,10,32],[0,1]):
 avg=sum((([P0,P1][(start+k)%2] for k in range(N))),s.zeros(4))/N
 assert avg==s.eye(4)/2;parity_cases+=1
# Build one common exact denominator for every output matrix.
D=1
for out in outs.values():
 for v in out:
  D=lcm(D,int(s.re(v).q),int(s.im(v).q))
num={key:matnum(out,D) for key,out in outs.items()}
meas=[]
for axes,bits in itertools.product(itertools.product([1,2,3],repeat=3),itertools.product([-1,1],repeat=3)):
 pis=[(I+b*P[a])/2 for a,b in zip(axes,bits)]
 M=kron(pis);SH=kron([3*pi-I for pi in pis])
 mr,mi=matnum(M,8);zr,zi=matnum(SH,8);meas.append((mr,mi,zr,zi))
expectations={};events=0;den=D*8*4*27*8
for t in range(2):
 accum={j:[np.zeros((8,8),dtype=object),np.zeros((8,8),dtype=object)] for j in [0,1,3]};probtotal=0
 for j,sgn in itertools.product([1,3],[-1,1]):
  rr,ii=num[t,j,sgn]
  for mr,mi,zr,zi in meas:
   # trace(out*projector), both represented by exact Gaussian-integer numerators.
   prob=int(np.sum(rr*mr.T-ii*mi.T));imag=int(np.sum(rr*mi.T+ii*mr.T))
   assert imag==0 and prob>=0
   probtotal+=prob;events+=1
   accum[0][0]+=prob*zr;accum[0][1]+=prob*zi
   accum[j][0]+=2*sgn*prob*zr;accum[j][1]+=2*sgn*prob*zi
 assert probtotal==D*8*4*27
 for j in [0,1,3]:
  target=s.eye(8)/8 if j==0 else Ds[t,j]
  tr,ti=matnum(target,den)
  assert np.array_equal(accum[j][0],tr) and np.array_equal(accum[j][1],ti)
  expectations[t,j]=accum[j]
# The actually averaged signed laws have full gaps despite both pointwise X kernels.
for j,gap in [(1,s.Rational(1,16)),(3,s.Rational(1,8))]:
 avg=(Ds[0,j]+Ds[1,j])/2
 assert s.simplify(avg*avg-gap*gap*s.eye(8))==s.zeros(8)
result={'status':'PASS exact margin-free alternating-source witness','source_draws':0,'rng_draws':0,'ordinary_exact_Born_events':events,'call_types':2,'positive_pointwise_kappa_exists':False,'explicit_negative_margin_kernel_cases':kernel_tests,'even_bank_parity_cases':parity_cases,'coarse_X_mass':'1/2','unsigned_patch_floor':'1/8','averaged_signed_X_gap':'1/16','averaged_signed_Z_gap':'1/8','current_full_CPTP_oracle_loss':'1/4','nontrivial_rational_gauge_projector':True,'nontrivial_rational_entangling_output_mixer':True,'exact_common_output_denominator':str(D)}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
