"""Turn floating frame proposals into exact rational stochastic kernels.
Rounding residuals are corrected through a fixed81-element product basis,
using a strictly positive reserved maximally mixed component.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from math import lcm,gcd
from fractions import Fraction as F
import json,time
import numpy as np
import sympy as S
from exact_instrument import D,clean
from compile_classical import fraction
BASE=Path(__file__).resolve().parents[1]
NQ=D*D
Q=2**48

def integer_matrix(M):
 den=lcm(*[int(x.q) for z in M for x in (S.re(z),S.im(z))])
 real=np.array([[int(S.re(z)*den) for z in row] for row in M.tolist()],dtype=object)
 imag=np.array([[int(S.im(z)*den) for z in row] for row in M.tolist()],dtype=object)
 return real,imag,den

def tensor(A,B):
 ar,ai,ad=A;br,bi,bd=B
 return np.kron(ar,br)-np.kron(ai,bi),np.kron(ar,bi)+np.kron(ai,br),ad*bd

def coords(real,imag):
 ans=[real[i,i] for i in range(NQ)]
 for i in range(NQ):
  for j in range(i+1,NQ):ans.extend((real[i,j],imag[i,j]))
 return np.array(ans,dtype=object)

def output_integer(real,imag,ur,ui):
 mr=ur@real-ui@imag;mi=ur@imag+ui@real
 rr=mr@ur.T+mi@ui.T;ii=mi@ur.T-mr@ui.T
 ra=np.array([[sum(rr[D*a+j,D*b+j] for j in range(D)) for b in range(D)] for a in range(D)],dtype=object)
 ia=np.array([[sum(ii[D*a+j,D*b+j] for j in range(D)) for b in range(D)] for a in range(D)],dtype=object)
 rb=np.array([[sum(rr[D*j+a,D*j+b] for j in range(D)) for b in range(D)] for a in range(D)],dtype=object)
 ib=np.array([[sum(ii[D*j+a,D*j+b] for j in range(D)) for b in range(D)] for a in range(D)],dtype=object)
 eye=np.eye(D,dtype=object)
 out_r=81*sum(rr[i,i] for i in range(NQ))*np.eye(NQ,dtype=object)-45*np.kron(ra.T,eye)-45*np.kron(eye,rb.T)+25*rr.T
 out_i=-45*np.kron(ia.T,eye)-45*np.kron(eye,ib.T)+25*ii.T
 return coords(out_r,out_i)

def encode_ratio(n,d):
 g=gcd(int(n),int(d));n=int(n)//g;d=int(d)//g
 return str(n) if d==1 else str(n)+'/'+str(d)

def replay():
 t=time.monotonic();raw=json.loads((BASE/'results'/'REPAIRED_FRAME_PROPOSAL.json').read_text())
 assert raw['result']['numerical_closure_proposed']
 matrices=[S.Matrix([[S.sympify(v) for v in row] for row in mat]) for mat in raw['local_states']]
 for M in matrices:
  assert M==M.H and S.trace(M)==1 and clean(M*M)==M
 states=[integer_matrix(M) for M in matrices];N=len(states)
 U=S.Matrix([[S.sympify(v) for v in row] for row in raw['gate']]);assert clean(U.H*U)==S.eye(NQ)
 ur,ui,ud=integer_matrix(U)
 products=[tensor(a,b) for a in states for b in states]
 frame_den=lcm(9,*[p[2] for p in products])
 columns=np.array([coords(r,i)*(frame_den//d) for r,i,d in products],dtype=object).T
 nine=[0,1,2,3,5,7,9,11,13]
 basis=[i*N+j for i in nine for j in nine]
 basemat=S.Matrix(columns[:,basis].tolist())/frame_den
 inverse=basemat.inv()
 assert all(v.is_Integer for v in inverse)
 inv=np.array(inverse.tolist(),dtype=object)
 eye_coord=coords(np.eye(NQ,dtype=object),np.zeros((NQ,NQ),dtype=object))*(frame_den//9)
 output_den=484*ud*ud*frame_den
 weight_den=Q*output_den*225
 base=[i*N+j for i in range(15) for j in range(15)]
 kernels=[];min_weight=None;min_reserve=1.;max_residual=0.;minimum_correction_margin=None
 for count,proposal in enumerate(raw['kernels']):
  i,j=proposal['input'];source=i*N+j
  rr,ii,dd=products[source];scale=frame_den//dd
  out=output_integer(rr*scale,ii*scale,ur,ui)
  # All proposed weights and the reserve are rounded down to a binary grid.
  counts=np.zeros(N*N,dtype=object)
  for a,b,p in proposal['terms']:counts[a*N+b]+=int(np.floor(p*Q))
  reserve=int(np.floor(proposal['reserve']*Q));assert reserve>0
  residual=Q*out-(output_den//frame_den)*(columns@counts+reserve*eye_coord)
  correction=inv@residual
  final=counts*(output_den*225)
  for k in base:final[k]+=reserve*output_den
  for k,value in zip(basis,correction):final[k]+=int(value)*225
  assert all(n>=0 for n in final),(source,min(final))
  assert sum(final)==weight_den,(source,'normalization')
  assert all(int(v)==0 for v in ((columns@final)*output_den-weight_den*out*frame_den)),(source,'intertwining')
  kernels.append(dict(input=[i,j],transitions=[[k//N,k%N,encode_ratio(n,weight_den)] for k,n in enumerate(final) if n]))
  min_reserve=min(min_reserve,reserve/Q)
  max_residual=max(max_residual,max(abs(float(F(int(n),Q*output_den))) for n in residual))
  cm=min(int(final[k]) for k in basis)
  minimum_correction_margin=cm if minimum_correction_margin is None else min(cm,minimum_correction_margin)
  if count%50==0:print('exact kernel columns',count+1,'/',N*N,flush=True)
 result=dict(local_states=N,product_kernel_states=N*N,exact_columns=len(kernels),
  exact_normalization=True,exact_nonnegativity=True,exact_matrix_intertwining=True,
  all_local_state_projectors=True,c='9/5',minimum_identity_reserve=min_reserve,
  maximum_rounded_coordinate_residual=max_residual,
  edges=sum(len(k['transitions']) for k in kernels),
  semantics='One fixed rational two-qutrit unitary followed by local Phi_9/5 on both sites; arbitrary width/depth and gate placements on product-frame initial states.',
  elapsed_seconds=time.monotonic()-t)
 artifact=dict(result=result,local_states=raw['local_states'],gate=raw['gate'],kernels=kernels)
 (BASE/'results'/'EXACT_REPAIRED_KERNEL.json').write_text(json.dumps(artifact,separators=(',',':'))+'\n')
 (BASE/'results'/'EXACT_REPAIR_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))

if __name__=='__main__':replay()
