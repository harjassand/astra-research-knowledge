import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(202610291235);I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
def kron(xs):
 v=np.ones((1,1),complex)
 for a in xs:v=np.kron(v,a)
 return v
def S(r):
 v=np.linalg.eigvalsh((r+r.conj().T)/2);v=v[v>1e-15];return -float(v@np.log(v))
def pinch(r,u):return (r+u@r@u.conj().T)/2
def part(r,u,a):return ((1+a)*r+(1-a)*u@r@u.conj().T)/2
maxcontract=0.;maxratio=0.;maxdef=0.;count=0
for n in [1,2,3]:
 dR=3;d=2**n*dR;xx=[kron([X if k==i else I for k in range(n)]+[np.eye(dR)]) for i in range(n)];yy=[kron([Y if k==i else I for k in range(n)]+[np.eye(dR)]) for i in range(n)]
 for trial in range(200):
  rank=int(rng.integers(1,d+1));A=rng.normal(size=(d,rank))+1j*rng.normal(size=(d,rank));rho=A@A.conj().T;rho/=np.trace(rho)
  a=float(rng.uniform(.01,1));de=pinch(rho,xx[0]);pa=part(rho,xx[0],a);g=S(de)-S(rho);ga=S(de)-S(pa)
  if g>1e-12:maxcontract=max(maxcontract,ga/(a*a*g))
  assert ga<=a*a*g+1e-11
  de=rho.copy();out=rho.copy()
  for u,v in zip(xx,yy):de=pinch(de,u);out=part(part(out,u,1/np.sqrt(2)),v,1/np.sqrt(2))
  loss=S(out)-S(rho);dloss=S(de)-S(rho);maxdef=max(maxdef,dloss-2*loss)
  if loss>1e-12:maxratio=max(maxratio,dloss/loss)
  assert dloss<=2*loss+1e-11;count+=1
weak=[]
for r in [.1,.01,.001]:
 rho=(I+r*Y)/2;out=part(part(rho,X,1/np.sqrt(2)),Y,1/np.sqrt(2));de=pinch(rho,X);weak.append(dict(r=r,ratio=(S(de)-S(rho))/(S(out)-S(rho))))
out=dict(trials=count,reference_dimension=3,max_binary_pinch_contraction_ratio=maxcontract,max_phase_complete_ratio=maxratio,max_factor2_defect=maxdef,weak_state_sharpness=weak,scope='Floating independent tests of proved identities; arbitrary-reference theorem is analytic, not inferred from tests.')
Path(__file__).with_name('PHASE_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
