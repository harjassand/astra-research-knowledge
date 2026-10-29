import numpy as np,json,math
from pathlib import Path
I=np.eye(2);swap=np.eye(4)[[0,2,1,3]];P=(np.eye(4)+swap)/2
ks=[np.sqrt(2/3)*P@np.kron(I,np.eye(2)[:,j:j+1]) for j in range(2)]
assert np.linalg.norm(sum(k.T@k for k in ks)-I)<1e-12
rho=np.array([[.65,.12-.08j],[.12+.08j,.35]])
r=np.linalg.norm([.24,.16,.3]);b=r/6
K=[I];rows=[]
def marginal(x,n):
 # retain first output spin, trace all other spins
 d=2**(n-1);return np.trace(x.reshape(2,d,2,d),axis1=1,axis2=3)
for ell in range(1,4):
 oldn=2**(ell-1);local=[np.ones((1,1))]
 for _ in range(oldn):local=[np.kron(a,k) for a in local for k in ks]
 K=[a@k for a in local for k in K];n=2**ell
 out=sum(k@rho@k.conj().T for k in K);red=marginal(out,n);f=(2/3)**ell;target=f*rho+(1-f)*I/2
 err=np.sum(np.abs(np.linalg.eigvalsh(red-rho)))/2
 assert np.linalg.norm(red-target)<1e-12 and err<=ell*b+1e-12
 rows.append(dict(depth=ell,receivers=n,kraus_count=len(K),map_residual=float(np.linalg.norm(red-target)),broadcast_error=float(err),telescoping_bound=float(ell*b),marginal_choi_is_EB=bool(f<=1/3)))
# Independent finite oscillator projection/reset checks on random coherent mixed states.
rng=np.random.default_rng(20261029);cutrows=[]
for _ in range(50):
 n=32;A=rng.normal(size=(n,3))+1j*rng.normal(size=(n,3));rr=A@A.conj().T;rr/=np.trace(rr);E=float(np.dot(np.arange(n),rr.diagonal().real));R=10
 trunc=np.zeros_like(rr);trunc[:R+1,:R+1]=rr[:R+1,:R+1];p=float(rr[R+1:,R+1:].trace().real);trunc[0,0]+=p
 distance=float(np.sum(abs(np.linalg.eigvalsh(rr-trunc)))/2);assert distance<=np.sqrt(p)+p/2+1e-12 and p<=E/R
 cutrows.append(dict(tail=p,distance=distance,gentle_bound=float(np.sqrt(p)+p/2)))
# Resource law on one oscillator, N(R)=floor(R)+1. Existence bounds, not actual huge trees.
table=[]
for E in [1.,10.]:
 for bb in [.01,.001,.0001]:
  R=16*E/bb**2;d=math.floor(R)+1;ell=math.ceil(math.log2(d*d/bb));bound=ell*bb+2*(math.sqrt(E/R)+E/R)+d*d/2**ell
  table.append(dict(energy=E,b=bb,cutoff=R,dimension=d,depth=ell,receivers=2**ell,bound=min(1.,bound)))
out=dict(cloner_tree=rows,max_cutoff_gentle_ratio=max(z['distance']/z['gentle_bound'] for z in cutrows),cutoff_trials=50,oscillator_resource_table=table,scope='Finite CP-map and cutoff floating checks; large resource rows evaluate proved bounds, not simulated trees or hardware.')
Path(__file__).with_name('CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
