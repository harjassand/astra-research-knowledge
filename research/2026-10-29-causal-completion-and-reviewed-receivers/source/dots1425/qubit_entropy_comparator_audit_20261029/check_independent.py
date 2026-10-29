import numpy as np,itertools,json,hashlib
from fractions import Fraction as F
from pathlib import Path
p=Path(__file__).parent;s=p.parent/'qubit_entropy_comparator_20261029'
assert all(hashlib.sha256((s/f).read_bytes()).hexdigest()==h for f,h in json.loads((s/'AUTHOR_FREEZE.json').read_text()).items())
I=np.eye(2,dtype=complex);P=[I,np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.diag([1,-1]).astype(complex)]
def entropy(r):
 vals=np.linalg.eigvalsh((r+r.conj().T)/2);assert min(vals)>-1e-10
 vals=vals[vals>1e-14];return float(-vals@np.log(vals))
def td(a,b):return float(abs(np.linalg.eigvalsh(a-b)).sum()/2)
def kron(xs):
 r=np.ones((1,1),complex)
 for x in xs:r=np.kron(r,x)
 return r
# Exact probability decomposition over all denominator-12 Pauli channels, all 3 axes.
count=0;eligible=[]
for a in range(13):
 for b in range(13-a):
  for c in range(13-a-b):
   pr=[F(a,12),F(b,12),F(c,12),F(12-a-b-c,12)]
   lam=[pr[0]+pr[1]-pr[2]-pr[3],pr[0]-pr[1]+pr[2]-pr[3],pr[0]-pr[1]-pr[2]+pr[3]]
   for ax in [1,2,3]:
    js=[x for x in [1,2,3] if x!=ax];pairs=[(0,ax),tuple(js)]
    alpha=sum(2*min(pr[x],pr[y]) for x,y in pairs)
    assert alpha==1-max(abs(lam[j-1]) for j in js)
    rest=pr[:];rebuilt=[F(0)]*4
    for x,y in pairs:
     m=min(pr[x],pr[y]);rest[x]-=m;rest[y]-=m;rebuilt[x]+=m;rebuilt[y]+=m
    assert min(rest)>=0 and [x+y for x,y in zip(rest,rebuilt)]==pr
    count+=1
   order=sorted(range(3),key=lambda j:abs(lam[j]),reverse=True)
   if lam[order[0]]**2+lam[order[1]]**2<=1:eligible.append((np.array(pr,float),order[0]+1,float(1-abs(lam[order[1]]))))
# Explicit unital self-compatible boundary extension: average economical cloner and its spin-flipped copy.
V=np.array([[1,0],[0,1/np.sqrt(2)],[0,1/np.sqrt(2)],[0,0]],complex)
W=np.kron(P[1],P[1])@V@P[1]
def ext(r):return (V@r@V.conj().T+W@r@W.conj().T)/2
def marginal(r,which):
 x=r.reshape(2,2,2,2)
 return np.trace(x,axis1=1,axis2=3) if which==0 else np.trace(x,axis1=0,axis2=2)
lam_expected=[1/np.sqrt(2),1/np.sqrt(2),.5]
res=0
for r in P:
 res=max(res,float(np.linalg.norm(marginal(ext(r),0)-marginal(ext(r),1))))
for j in range(3):res=max(res,float(np.linalg.norm(marginal(ext(P[j+1]),0)-lam_expected[j]*P[j+1])))
assert res<1e-14 and np.linalg.norm(marginal(ext(I),0)-I)<1e-14
# Stable entropy-deficit series for weak Bloch-vector local sharpness.
def deficit(r):return sum(r**(2*k)/(2*k*(2*k-1)) for k in range(1,101))
ratios=[deficit(r)/(deficit(r)-deficit(r/np.sqrt(2))) for r in [.1,.01,.001,.0001]]
assert abs(ratios[-1]-2)<1e-8
rng=np.random.default_rng(293448);min_margin=1.;max_ratio=0.;min_submod=1.;max_gauge_error=0.
def randU():
 q,r=np.linalg.qr(rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)));return q
for trial in range(100):
 n=3;dim=16;rank=[1,2,8,16][trial%4]
 A=rng.normal(size=(dim,rank))+1j*rng.normal(size=(dim,rank));rho=A@A.conj().T;rho/=np.trace(rho)
 pars=[eligible[int(rng.integers(len(eligible)))] for _ in range(n)]
 ins=[randU() for _ in range(n)];outs=[randU() for _ in range(n)]
 U=kron(ins+[I]);O=kron(outs+[I]);r=U@rho@U.conj().T
 fs={};base=entropy(r)
 for mask in range(8):
  rr=r.copy()
  for i,(pr,ax,al) in enumerate(pars):
   if mask>>i&1:
    Z=kron([P[ax] if j==i else I for j in range(n)]+[I]);rr=(rr+Z@rr@Z)/2
  fs[mask]=entropy(rr)-base
 for mask in range(8):
  for i,j in itertools.combinations(range(n),2):
   if not(mask>>i&1 or mask>>j&1):
    gap=fs[mask|1<<i]+fs[mask|1<<j]-fs[mask]-fs[mask|1<<i|1<<j];min_submod=min(min_submod,gap);assert gap>-1e-11
 rr=r.copy()
 for i,(pr,ax,al) in enumerate(pars):
  lifts=[kron([z if j==i else I for j in range(n)]+[I]) for z in P]
  rr=sum(w*z@rr@z.conj().T for w,z in zip(pr,lifts))
 gain=entropy(O@rr@O.conj().T)-entropy(rho);alpha=min(t[2] for t in pars);margin=gain-alpha*fs[7]
 assert margin>-1e-11;min_margin=min(min_margin,margin)
 if gain>1e-12:max_ratio=max(max_ratio,fs[7]/gain)
# Stationary-barycenter correlated ensemble: full local Pauli orbit of Bell-like entangled state.
v=np.array([np.sqrt(.7),0,0,np.sqrt(.3)],complex);r=np.outer(v,v.conj());orb=[np.kron(a,b) for a in P for b in P];ensemble=[u@r@u.conj().T for u in orb]
pr=np.array([1+sum(lam_expected),1+lam_expected[0]-lam_expected[1]-lam_expected[2],1-lam_expected[0]+lam_expected[1]-lam_expected[2],1-lam_expected[0]-lam_expected[1]+lam_expected[2]])/4
alpha=1-1/np.sqrt(2)
def ch(r):
 for i in range(2):
  lifts=[np.kron(z,I) if i==0 else np.kron(I,z) for z in P];r=sum(w*z@r@z for w,z in zip(pr,lifts))
 return r
def deph(r):
 for z in [np.kron(P[1],I),np.kron(I,P[1])]:r=(r+z@r@z)/2
 return r
bar=sum(ensemble)/16;assert np.linalg.norm(bar-np.eye(4)/4)<1e-14
loss=sum(entropy(ch(r))-entropy(r) for r in ensemble)/16;dist=sum(td(r,deph(r)) for r in ensemble)/16
assert dist<=np.sqrt(loss/(2*alpha))+1e-12
# Singleton ensemble obstruction to deleting kappa: delta=0 but dephasing changes the state.
r=(I+P[2])/2;dr=(r+P[1]@r@P[1])/2;nonstationary={'holevo_loss_delta':0.,'trace_disturbance':td(r,dr),'kappa':entropy(marginal(ext(r),0))-entropy(r)}
assert nonstationary['trace_disturbance']>.49 and nonstationary['kappa']>0
out={'manifest_verified':True,'exact_rational_pairing_cases':count,'grid_channels_with_required_singular_inequality':len(eligible),'grid_scope':'Singular inequality candidates, not all asserted self-compatible','boundary_extension_residual':res,'weak_axis_local_ratios':ratios,'correlated_reference_gauged_trials':100,'min_submodularity_gap':min_submod,'min_complete_margin':min_margin,'max_complete_observed_ratio':max_ratio,'stationary_correlated_prior':{'delta':loss,'mean_trace_disturbance':dist,'bound':float(np.sqrt(loss/(2*alpha)))},'nonstationary_singleton_counterexample':nonstationary,'scope':'Exact probability arithmetic plus floating entropy/state checks; proof governs, no novelty or hardware claim.'}
(p/'independent_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
