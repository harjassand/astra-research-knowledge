"""Probe the free orbit-gate law using affine pullbacks of the known QC F."""
from pathlib import Path
from fractions import Fraction as R
from itertools import product
from math import factorial
import json,sys,importlib.util,time
import numpy as np
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import heat_model as h
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
start=time.perf_counter();raw=json.loads((root/'work/orbit_gate_free_law.json').read_text());law=[(R(w),list(map(R,A))) for w,A in zip(raw['atom_weights'],raw['atoms'])];B=np.array([A for w,A in law],float).reshape(-1,2,2);weights=np.array([w for w,A in law],float);F4=np.zeros((4,)*4)
for ids in product(range(4),repeat=4):
 pw=tuple(ids.count(i) for i in range(4));F4[ids]=float(h.F.get(pw,0))*np.prod([factorial(v) for v in pw])/factorial(4)
def score(P,Q):
 A=np.einsum('ij,pjk,kl->pil',P,B,Q).reshape(-1,4);H=12*np.einsum('ijkl,p,pk,pl->ij',F4,weights,A,A);v=4*np.einsum('ijkl,p,pj,pk,pl->i',F4,weights,A,A,A);f=np.einsum('ijkl,p,pi,pj,pk,pl',F4,weights,A,A,A,A);a=2*f-v@np.linalg.solve(H,v);return float(a)
I=[[R(int(i==j)) for j in range(2)] for i in range(2)];candidates=[]
for side,i,j,eps in product((0,1),range(2),range(2),(R(1,16),R(-1,16),R(1,64),R(-1,64),R(1,256),R(-1,256))):
 P=[row[:] for row in I];Q=[row[:] for row in I];(P if side==0 else Q)[i][j]+=eps;val=score(np.array(P,float),np.array(Q,float));candidates.append((val,P,Q))
candidates.sort(key=lambda q:q[0]);val,P,Q=candidates[0];b,ca,r=h.b,h.ca,h.r;A=[b.var(4,i) for i in range(4)];images=[]
for i,j in product(range(2),repeat=2):images.append(b.add(*(b.scale(A[2*k+l],P[i][k]*Q[l][j]) for k,l in product(range(2),repeat=2))))
FP=r.compose(h.F,images,4)
def avg(p):return sum(w*b.evaluate(p,A) for w,A in law)
H=[[avg(b.diff(b.diff(FP,i),j)) for j in range(4)] for i in range(4)];v=[avg(b.diff(FP,i)) for i in range(4)];f=avg(FP);hv=r.m.linear_solve(H,v);aa=2*f-h.r.dot(v,hv);print('small affine-pullback test',float(aa),flush=True)
out={'P':[[str(v) for v in row] for row in P],'Q':[[str(v) for v in row] for row in Q],'exact_translated_QC_excess':str(aa),'negative_exact':aa<0,'scope':'A negative result excludes this FREE law through an affine pullback of the retained globally QC leading F. It is not a gradient witness.'}
if aa<0:
 M=[-x for x in hv];direct=sum(w*b.evaluate(FP,[x+y for x,y in zip(M,A)]) for w,A in law)-b.evaluate(FP,M);assert direct==aa/2<0;out.update({'negative_mean':list(map(str,M)),'direct_negative_free_energy':str(direct),'actual_gradient_realization':'IMPOSSIBLE_BY_KNOWN_QC_AFFINE_PULLBACK'})
else:out['actual_gradient_realization']='UNKNOWN; finite probe is not exhaustive'
(root/'work/free_law_affine_probe.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'negative_exact':aa<0,'actual_gradient_realization':out['actual_gradient_realization'],'seconds':time.perf_counter()-start},indent=2),flush=True)
