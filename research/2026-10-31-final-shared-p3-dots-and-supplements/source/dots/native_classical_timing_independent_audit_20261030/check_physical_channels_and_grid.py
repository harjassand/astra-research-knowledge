"""Finite channel and deterministic timing checks, not a hardware threshold."""
import numpy as np,json,itertools
rng=np.random.default_rng(1484)
n=2
# c,stage,tag(notfree/free), X=(Det,Rand), S=(saved Det)
shape=(3,n+1,2,4,2);dim=np.prod(shape)
idx=lambda x:np.ravel_multi_index(x,shape)
labels=list(itertools.product(*(range(d) for d in shape)))
I=np.eye(dim,dtype=complex)
# Actual complete tick channel acts as identity on tag, X, S.
kt=[]
for c,j in itertools.product(range(3),range(n+1)):
 k=np.zeros_like(I)
 for tag,x,s in itertools.product(range(2),range(4),range(2)):
  jj=j+1 if c==2 and j<n else j
  k[idx((c,jj,tag,x,s)),idx((c,j,tag,x,s))]=1
 kt.append(k)
pt=np.zeros_like(I);pf=np.zeros_like(I);ready=np.zeros_like(I)
for z in labels:
 c,j,tag,x,s=z
 pt[idx(z),idx(z)]=tag==0
 pf[idx(z),idx(z)]=tag==1
 ready[idx(z),idx(z)]=(c==2 and j==n)
# Disabled leaves do not resolve X or S.
kc=[pt,pf@(I-ready)]
enabled=[]
for oldx,s,r in itertools.product(range(4),range(2),range(2)):
 k=np.zeros_like(I)
 k[idx((0,0,1,2*(1-s)+r,s)),idx((2,n,1,oldx,s))]=1/np.sqrt(2)
 kc.append(k);enabled.append(k)
# Source effects diagonal here, calculate exactly without large dense products.
effect=lambda ks:sum(k.conj().T@k for k in ks)
tick_err=float(np.linalg.norm(effect(kt)-I))
commit_err=float(np.linalg.norm(effect(kc)-I))
free_err=float(np.linalg.norm(effect(kc[1:])-pf))
assert max(tick_err,commit_err,free_err)<1e-12
# A disabled opportunity leaves a coherent S payload untouched.
v=np.zeros(dim,complex)
for s in range(2):v[idx((1,1,1,0,s))]=1/np.sqrt(2)
rho=np.outer(v,v.conj())
out=sum(k@rho@k.conj().T for k in kc)
disabled_payload_error=float(np.linalg.norm(out-rho))
assert disabled_payload_error<1e-12
# The enabled outcome definitely exits ready and has a fair Rand bit.
v=np.zeros(dim,complex);v[idx((2,n,1,0,0))]=1
rho=np.outer(v,v.conj());out=sum(k@rho@k.conj().T for k in kc)
assert abs(np.trace(ready@out))<1e-12
rand=[sum(out[idx(z),idx(z)].real for z in labels if z[3]%2==r) for r in range(2)]
assert np.allclose(rand,[.5,.5])
# Tilted identity includes the entire physical TP background.
lam=.7;kap=.4
norms=[]
for theta in [-.4,.2]:
 # H contribution on I vanishes for any H; the complete commit background also vanishes.
 adj=lam*(np.exp(theta)*effect(kt)-I)+kap*(effect(kc)-I)
 norms.append(float(np.linalg.norm(adj-lam*(np.exp(theta)-1)*I)))
assert max(norms)<1e-12
# Deterministic regular-grid adversarial timing test (n_big=400, delta=1).
nbig=400;ticks=[]
for tile in range(200):
 m=int(rng.integers(19,22))
 # Alternating extreme clustering near tile endpoints; distinct timestamps.
 vals=np.linspace(.0001,.0002,m) if tile%2 else np.linspace(.9998,.9999,m)
 ticks.extend(tile+vals)
ticks=np.array(ticks)
starts=np.r_[rng.uniform(0,175,2000), np.arange(175),ticks[ticks<175]+1e-8]
durs=[]
for t in starts:
 first=np.searchsorted(ticks,t,side='right');done=ticks[first+nbig-1];durs.append(done-t)
assert min(durs)>=16 and max(durs)<=24
# Exact Chernoff conservative constant.
e=.05;mu_per_n=.05
upper=mu_per_n*((1+e)*np.log(1+e)-e)
lower=mu_per_n*(e+(1-e)*np.log(1-e))
assert min(upper,lower)>=1/24000
print(json.dumps({'scope':'Exact small-channel and finite timing checks only.',
 'complete_tick_effect_error':tick_err,'complete_commit_effect_error':commit_err,
 'FREE_family_effect_error':free_err,'disabled_coherent_payload_error':disabled_payload_error,
 'enabled_Rand_distribution':rand,'tilted_identity_residuals':norms,
 'tested_active_run_starts':len(starts),'duration_in_delta_units':[min(durs),max(durs)],
 'universal_short_count_fraction':17*21/400,'universal_long_count_fraction':23*19/400,
 'Chernoff_exponents_per_n':[upper,lower],'conservative_exponent_per_n':1/24000},indent=2))
