"""Independent effect contraction and nonidentical mixed-port checks; finite floating diagnostic."""
import numpy as np,itertools,json
from pathlib import Path
rng=np.random.default_rng(11291133)
def adj(a):return a.conj().T
def td(a,b):return np.linalg.svd(a-b,compute_uv=False).sum()/2
def partial(rho,d,n,keep):
 a=rho.reshape([d]*(2*n));left=n
 for j in reversed(range(n)):
  if j not in keep:a=np.trace(a,axis1=j,axis2=j+left);left-=1
 return a.reshape(d**len(keep),d**len(keep))
def pgm(d,N):
 digits=list(itertools.product(range(d),repeat=N+1));D=len(digits);P=[]
 for port in range(1,N+1):
  A=np.zeros((D,D))
  for r,rr in enumerate(digits):
   for c,cc in enumerate(digits):
    if rr[0]==rr[port] and cc[0]==cc[port] and all(rr[j]==cc[j] for j in range(1,N+1) if j!=port):A[r,c]=1/d
  P.append(A)
 total=sum(P);lam,V=np.linalg.eigh(total);live=lam>1e-10;root=(V[:,live]/np.sqrt(lam[live]))@V[:,live].T;Q=V[:,live]@V[:,live].T
 Ms=[root@a@root+(np.eye(D)-Q)/N for a in P]
 Js=[partial(M,d,N+1,[0,i+1]).T/d**(N+1) for i,M in enumerate(Ms)]
 assert np.linalg.norm(sum(Ms)-np.eye(D))<1e-11
 J=sum(Js);phi=np.eye(d).ravel()/np.sqrt(d);F=float(phi@J@phi);bound=N/(N+d*d-1)
 assert F>=bound-1e-11 and abs(np.trace(J)-1)<1e-11
 assert max(np.linalg.norm(j-J/N) for j in Js)<1e-11
 for i,A in enumerate(P):
  r=d**(N-1);v=np.trace(A@root)/r;avg=np.trace(A@total)/r
  assert v+1e-11>=avg**-.5
 return Ms,Js,J,F
rows=[]
for d,N in [(2,i) for i in range(1,6)]+[(3,1),(3,2)]:
 Ms,Js,J,F=pgm(d,N);phi=np.eye(d).ravel()/np.sqrt(d);Phi=np.outer(phi,phi);lam=(d*d*F-1)/(d*d-1)
 assert np.linalg.norm(J-lam*Phi-(1-lam)*np.eye(d*d)/d**2)<1e-11
 assert abs(td(J,Phi)-(1-F))<1e-11
 rows.append(dict(d=d,ports=N,F=F,proved_bound=N/(N+d*d-1)))
# Full density simulation with two DIFFERENT CPTP port resources, no square-root branch implementation.
d=2;N=2;Ms,Js,J,F=pgm(d,N);phi=np.eye(d).ravel()/np.sqrt(d);Phi=np.outer(phi,phi)
channels=[]
for g in [.13,.47]:
 z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));U,_=np.linalg.qr(z)
 channels.append([U@np.diag([1,np.sqrt(1-g)]),U@np.array([[0,np.sqrt(g)],[0,0]])])
def onout(C,ks):return sum(np.kron(np.eye(d),k)@C@adj(np.kron(np.eye(d),k)) for k in ks)
resources=[onout(Phi,k) for k in channels];rho=np.kron(np.kron(Phi,resources[0]),resources[1]);order=[0,1,2,4,3,5];rho=rho.reshape([d]*12).transpose(order+[x+6 for x in order]).reshape(64,64)
actual=np.zeros((4,4),complex)
for i,M in enumerate(Ms):
 left=np.kron(np.kron(np.eye(d),M),np.eye(d**N))@rho;actual+=partial(left,d,2*N+2,[0,N+2+i])
expected=sum(onout(j,k) for j,k in zip(Js,channels));res=float(np.linalg.norm(actual-expected));assert res<1e-11
average=sum(onout(J,k) for k in channels)/N;assert np.linalg.norm(actual-average)<1e-11
out=dict(ideal_cases=rows,nonidentical_mixed_product_full_density_residual=res,equal_routed_port_subchannels_verified=True,scope='Independent finite floating PGM/effect contraction and mixed nonidentical resources; not native scalable compiler, SDP or physical resource acquisition.')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
