"""Outward primitives for the planned damped coefficient receiver."""
from pathlib import Path
from fractions import Fraction as Q
from math import factorial
import sys,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent/'morrey_boundary_markov_receiver_20261025'));import outward_binary64 as I

def mid_guard(v,radius=None,relative=None):
 m=(v[0]+v[1])/2;rad=np.nextafter(np.maximum(m-v[0],v[1]-m),np.inf)
 if radius is not None:assert np.max(rad)<=radius,(np.max(rad),radius)
 if relative is not None:assert np.all(v[0]>0) and np.max(np.nextafter(rad/v[0],np.inf))<=relative
 return m,float(np.max(rad))
def H_received(integer_sums,epsilon=Q(1,512)):
 lam=I.mul(I.mul(I.square(I.PI),I.rat(Q(1,8))),I.exact(integer_sums));x=I.mul(lam,I.rat(epsilon));z=I.div(x,I.rat(128));assert np.max(z[1])<=.6
 p=I.rat(Q(1,factorial(20)))
 for j in range(19,-1,-1):p=I.add(I.rat(Q((-1)**j,factorial(j))),I.mul(z,p))
 rem=Q(3,5)**21/factorial(21);p=I.add(p,I.box(-rem,rem))
 for _ in range(7):p=I.square(p)
 return mid_guard(I.div(p,I.mul(I.rat(2),lam)),relative=2**-36)
def extreme_face_N_upper(f,a,steps=42):
 f=np.asarray(f);aa=abs(float(a))
 if aa==0:return np.nextafter(2*np.maximum(-f,0),np.inf),0.
 lo=np.where(f>=0,-2*aa,0.);hi=np.where(f>=0,0.,2*aa);fi=I.exact(f);ai=I.exact(aa);a2=I.square(ai)
 for _ in range(steps):
  mid=(lo+hi)/2;mi=I.exact(mid)
  # p=lambda³-2f lambda²+(f²-2a²)lambda+a²f.
  p=I.add(I.mul(I.add(I.mul(I.sub(mi,I.mul(I.rat(2),fi)),mi),I.sub(I.square(fi),I.mul(I.rat(2),a2))),mi),I.mul(a2,fi))
  neg=p[1]<0;pos=p[0]>0;lo=np.where(neg,mid,lo);hi=np.where(pos,mid,hi)
 width=hi-lo;assert np.max(width)<2**-34, np.max(width)
 out=np.where(f>=0,-lo,hi-2*f)
 return np.nextafter(out,np.inf),float(np.max(width))
if __name__=='__main__':
 import json,time
 P=Path(__file__).resolve().parent;st=time.time();Hs,rad=H_received(np.arange(1,27649));f=np.linspace(-2,2,1001);a=Q(13287662384745547,10**18)/16;out,width=extreme_face_N_upper(f,float(a));M=np.zeros((len(f),3,3));M[:,0,0]=M[:,1,1]=f;M[:,0,1]=M[:,1,0]=float(a);M[:,0,2]=M[:,2,0]=-float(a);ref=np.maximum(-np.linalg.eigvalsh(M),0).sum(1);assert np.max(ref-out)<1e-14
 result={'scope':'Primitive guard regression only, no actual field. Exp and bisection enclosures rely on outward operations; NumPy eigenvalue comparison is diagnostic only.','H_integer_sums_checked':len(Hs),'H_max_absolute_radius':rad,'face_root_max_bracket_width':width,'face_test_count':len(f),'seconds':time.time()-st};(P/'damped_primitive_guard_check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
