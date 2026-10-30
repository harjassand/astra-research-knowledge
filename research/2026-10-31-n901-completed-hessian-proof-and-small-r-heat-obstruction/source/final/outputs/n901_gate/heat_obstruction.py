"""Exact actual-field obstruction to ordinary heat for small-r N901.

This evaluates the ORIGINAL polynomial along an actual eight-mode
Hessian heat trajectory. A positive derivative rules out any legitimate
globally closed correction making its ordinary-heat density PSD. It is
not a quasiconvexity counterexample.
"""
from pathlib import Path
from fractions import Fraction as R
from collections import defaultdict
from math import comb
import importlib.util,json,time
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('n901_heat_receiving_algebra',HERE/'receive.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
def add(*polys):
 out=defaultdict(R)
 for P in polys:
  for k,c in P.items():out[k]+=c
 return {k:c for k,c in out.items() if c}
def scale(P,c):return {k:c*v for k,v in P.items() if c*v}
def mul(P,Q):
 out=defaultdict(R)
 for k,c in P.items():
  for l,d in Q.items():out[tuple(x+y for x,y in zip(k,l))]+=c*d
 return {k:c for k,c in out.items() if c}
def heat(P):return {k:-R(k[0]**2+k[1]**2)*c for k,c in P.items()}
def cos(k,c):return {k:c/2,tuple(-x for x in k):c/2}
def source_numerator():
 r,p,q,w=[b.var(4,i) for i in range(4)];one={(0,)*4:R(1)};sig=b.add(one,r);rp2=b.add(scale(one,2),r);u=b.add(b.power(q,2),b.mul(b.power(sig,2),b.power(p,2)));v=b.add(b.power(w,2),b.mul(b.power(sig,2),b.power(q,2)));j=b.mul(sig,b.add(b.mul(p,w),scale(b.power(q,2),-1)));conf=b.add(u,v,scale(j,-2));D=scale(b.mul(r,b.mul(b.power(sig,2),b.power(rp2,2))),8)
 Hnum=b.add(scale(b.mul(r,b.power(conf,2)),9),scale(b.mul(b.mul(r,b.add(r,scale(one,-1))),b.mul(rp2,b.power(u,2))),4),scale(b.mul(rp2,b.power(j,2)),24),scale(b.mul(b.mul(r,rp2),b.mul(u,j)),24))
 return b.add(Hnum,scale(b.mul(D,b.mul(b.power(p,2),q)),-1),scale(b.mul(scale(b.mul(r,b.power(rp2,2)),8),b.power(q,3)),-1),b.mul(D,b.power(p,2))),D
def main():
 start=time.perf_counter();eps=R(1,1000);psi=add(cos((1,0),R(-1)),cos((0,1),eps*R(10,32)),*(cos((a,y),eps*c/2) for a,c in ((2,R(-15,32)),(4,R(6,32)),(6,R(-1,32))) for y in (-1,1)))
 A=[{k:-R(k[0]**2)*v for k,v in psi.items() if k[0]},{k:-R(k[0]*k[1])*v for k,v in psi.items() if k[0]*k[1]},{k:-R(k[1]**2)*v for k,v in psi.items() if k[1]}];At=list(map(heat,A));cache={(0,0,0):{(0,0):R(1)}}
 def mon(pw):
  if pw not in cache:
   i=next(i for i,x in enumerate(pw) if x);ee=list(pw);ee[i]-=1;cache[pw]=mul(A[i],mon(tuple(ee)))
  return cache[pw]
 def dmon(pw):
  out={}
  for i,x in enumerate(pw):
   if x:
    ee=list(pw);ee[i]-=1;out=add(out,scale(mul(mon(tuple(ee)),At[i]),x))
  return out
 Pnum,D=source_numerator();valuepowers=sorted({pw[1:] for pw in Pnum});mom={pw:mon(pw).get((0,0),R(0)) for pw in valuepowers};dmom={pw:dmon(pw).get((0,0),R(0)) for pw in valuepowers};nume={};enume={}
 for pw,c in Pnum.items():nume[pw[0]]=nume.get(pw[0],R(0))+c*dmom[pw[1:]];enume[pw[0]]=enume.get(pw[0],R(0))+c*mom[pw[1:]]
 nume={k:c for k,c in nume.items() if c};enume={k:c for k,c in enume.items() if c};rr=R(1,10**9);degree=max(nume);B=[sum((nume.get(p,R(0))*rr**p*R(comb(k,p),comb(degree,p)) for p in range(k+1)),R(0)) for k in range(degree+1)];assert all(v>0 for v in B)
 den=sum(c*rr**pw[0] for pw,c in D.items());derivative=sum(c*rr**k for k,c in nume.items())/den;energy=sum(c*rr**k for k,c in enume.items())/den;assert derivative>0 and energy>0
 # Independently compare with the direct original polynomial at the
 # endpoint. This also checks the common positive denominator.
 original=b.source(rr);assert sum((c*dmom[pw] for pw,c in original.items()),R(0))==derivative;assert sum((c*mom[pw] for pw,c in original.items()),R(0))==energy
 assert mom.get((2,1,0),0)==0 and mom.get((0,3,0),0)==0
 result={'actual_potential':'-cos(x)+(1/1000)*sin(x)^6*cos(y)','nonzero_real_Fourier_modes':8,'r_interval':'0 < r <= 1/1000000000','common_positive_denominator':'8*r*(r+1)^2*(r+2)^2','heat_derivative_numerator_coefficients':{str(k):str(c) for k,c in sorted(nume.items())},'strictly_positive_Bernstein_coefficients':list(map(str,B)),'endpoint_r':str(rr),'endpoint_energy':str(energy),'endpoint_positive_heat_derivative':str(derivative),'original_cubic_average':'0','ordinary_heat_monotonicity':'REFUTED_ON_STATED_INTERVAL','legitimate_closed_correction_with_PSD_ordinary_heat_density':'IMPOSSIBLE_ON_STATED_INTERVAL','quasiconvexity_failure':False,'other_diffusions_or_nonlocal_flows':'NOT_EXCLUDED','seconds':time.perf_counter()-start};(HERE/'heat_obstruction.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('heat_derivative_numerator_coefficients','strictly_positive_Bernstein_coefficients','endpoint_energy','endpoint_positive_heat_derivative')},indent=2));print('endpoint heat derivative approximately',float(derivative))
if __name__=='__main__':main()
