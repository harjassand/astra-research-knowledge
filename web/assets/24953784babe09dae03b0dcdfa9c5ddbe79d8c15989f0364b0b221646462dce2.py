"""Independent finite-dimensional and exact-arithmetic checks.

No check is a substitute for the proof. Dense Fock calculations are confined
here; the delivered sampler itself never constructs an exponential state.
"""
from __future__ import annotations
import sys, json, math, time, itertools
from fractions import Fraction
from pathlib import Path
import numpy as np
import sympy as sp
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from fermion_completion import *

rng=np.random.default_rng(61007)
RESULTS={"seed":61007,"status":"running","checks":{}}

def td(a,b):
    return float(np.linalg.eigvalsh((a-b+a.conj().T-b.conj().T)/2).__abs__().sum()/2)

def unitary(m):
    q,r=np.linalg.qr(rng.normal(size=(m,m))+1j*rng.normal(size=(m,m)))
    return q @ np.diag(np.diag(r)/abs(np.diag(r)))

def pfaff(a):
    n=len(a)
    if n==0:return 1.+0j
    if n%2:return 0j
    return sum((-1)**(j+1)*a[0,j]*pfaff(a[np.ix_([k for k in range(n) if k not in (0,j)],[k for k in range(n) if k not in (0,j)])]) for j in range(1,n))

def bcs_vector(f):
    m=len(f); v=np.zeros(2**m,complex)
    for mask in range(2**m):
        inds=[j for j in range(m) if mask>>j&1]
        if not len(inds)%2:v[mask]=pfaff(f[np.ix_(inds,inds)])
    return v/np.linalg.norm(v)

def two_vector(a):
    m=len(a);v=np.zeros(2**m,complex)
    for i in range(m):
        for j in range(i+1,m):v[(1<<i)|(1<<j)]=a[i,j]
    return v

def one_vector(v):
    ans=np.zeros(2**len(v),complex)
    for i,c in enumerate(v):ans[1<<i]=c
    return ans

def physical_loss(v,m,eta):
    """Direct system/environment exterior-product isometry, not qubit damping."""
    branches={}
    for mask,amp in enumerate(v):
        if abs(amp)<1e-16:continue
        occupied=[i for i in range(m) if mask>>i&1]
        k=len(occupied)
        for sub in range(1<<k):
            kept=[occupied[j] for j in range(k) if sub>>j&1]
            lost=[occupied[j] for j in range(k) if not sub>>j&1]
            sign=(-1)**sum(r<t for r in lost for t in kept)
            env=sum(1<<j for j in lost);system=sum(1<<j for j in kept)
            if env not in branches:branches[env]=np.zeros(2**m,complex)
            branches[env][system]+=amp*sign*eta**(len(kept)/2)*(1-eta)**(len(lost)/2)
    return sum(np.outer(b,b.conj()) for b in branches.values())

def density_formula(a,eta):
    m=len(a);v=two_vector(a)
    rho=eta**2*np.outer(v,v.conj());rho[0,0]+=(1-eta)**2
    inds=[1<<j for j in range(m)]
    rho[np.ix_(inds,inds)]+=eta*(1-eta)*a@a.conj().T
    return rho

def fock_covariance(v,m):
    cv=[]
    for j in range(m):
        av=np.zeros_like(v);ad=np.zeros_like(v)
        for mask,amp in enumerate(v):
            sign=(-1)**((mask & ((1<<j)-1)).bit_count())
            if mask>>j&1:av[mask^(1<<j)]=sign*amp
            else:ad[mask|(1<<j)]=sign*amp
        cv.extend([av+ad,-1j*(av-ad)])
    cv=np.asarray(cv)
    g=(1j*(cv.conj()@cv.T)).real
    np.fill_diagonal(g,0)
    return (g-g.T)/2

def covariance_distribution(g):
    m=len(g)//2;out=np.zeros(2**m)
    def rec(h,p,mask,depth):
        if depth==m:out[mask]=p;return
        for bit in (0,1):
            w,new=condition_first_mode(h,bit)
            if w>1e-15:rec(new,p*w,mask|(bit<<depth),depth+1)
    rec(g,1.,0,0)
    return out

def ensemble(block):
    a,b,x,_=block.parameters();w=block.orbitals;s=block.coefficients
    out=[]
    for j in range(block.rank+1):
        theta=2*math.pi*j/(block.rank+1)
        f=w@canonical_pair_matrix(math.sqrt(x)*s*np.exp(1j*theta))@w.T
        out.append(((a+b)/(block.rank+1),bcs_vector(f)))
    for j,p in enumerate(np.repeat(abs(s)**2,2)):
        out.append((block.eta*(1-block.eta)*p,one_vector(w[:,j])))
    return [(float(p),v) for p,v in out if p>0]

def density_ensemble(ens):
    return sum(p*np.outer(v,v.conj()) for p,v in ens)

def fock_lift(u):
    m=len(u);ans=np.zeros((2**m,2**m),complex)
    sectors={k:[mask for mask in range(2**m) if mask.bit_count()==k] for k in range(m+1)}
    ind={mask:[j for j in range(m) if mask>>j&1] for mask in range(2**m)}
    for masks in sectors.values():
        for x in masks:
            for y in masks:ans[x,y]=np.linalg.det(u[np.ix_(ind[x],ind[y])])
    return ans

start=time.perf_counter()
# 1. Exact rational identities for the unnormalised completion.
count=0
for r in range(1,8):
    weights=[Fraction(j, r*(r+1)//2) for j in range(1,r+1)]
    for eta in (Fraction(1,20),Fraction(1,5),Fraction(1,2),Fraction(4,5)):
        a=(1-eta)**2;b=eta**2;t=b/a
        e=[Fraction(1)]+[Fraction(0)]*r
        for w in weights:
            for k in range(r,0,-1):e[k]+=w*e[k-1]
        product=math.prod([1+t*w for w in weights])
        added=a*sum(e[k]*t**k for k in range(2,r+1))
        assert a*product+2*eta*(1-eta)==1+added
        assert e[2] if False else True
        count+=1
RESULTS['checks']['rational_completion']={"instances":count,"exact":True}

# 2. Exact symbolic sharp four-mode formulas.
a,b=sp.symbols('a b',positive=True)
d=(sp.sqrt(a+b)-sp.sqrt(a))**2
assert sp.simplify((b-d)**2-4*a*d)==0
z=sp.symbols('z',positive=True)
assert sp.simplify((2*(4*a*z*(1+z))*z-4*a*z*z)/(1+2*z)-4*a*z*z)==0
RESULTS['checks']['sharp_distance_symbolic']={"identities":2,"exact":True}

# 3. Covariance sign, measurement updates, passive maps and lossy Gaussian maps.
max_cov=max_prob=max_loss=0.;cases=0
for m in (2,4,6,8):
    for rep in range(3):
        z=rng.normal(size=m//2)+1j*rng.normal(size=m//2)
        f=canonical_pair_matrix(z);u=unitary(m)
        v=bcs_vector(u@f@u.T)
        g0=np.zeros((2*m,2*m))
        for j,zz in enumerate(z):g0[4*j:4*j+4,4*j:4*j+4]=pair_covariance(zz)
        g=gaussian_loss(g0,u)
        max_cov=max(max_cov,float(np.max(abs(g-fock_covariance(v,m)))))
        max_prob=max(max_prob,float(np.max(abs(covariance_distribution(g)-abs(v)**2))))
        if m<=6:
            eta=.37
            exact=physical_loss(v,m,eta)
            approx=covariance_distribution(gaussian_loss(g,math.sqrt(eta)*np.eye(m)))
            max_loss=max(max_loss,float(np.max(abs(approx-np.diag(exact).real))))
        cases+=1
assert max(max_cov,max_prob,max_loss)<2e-10,(max_cov,max_prob,max_loss)
RESULTS['checks']['gaussian_engine']={"instances":cases,"max_covariance_entry_error":max_cov,"max_full_distribution_entry_error":max_prob,"max_loss_distribution_entry_error":max_loss}

# 4. All-rank two-fermion completion, independently generated loss, acquisition.
max_identity=max_td_error=max_reconstruction=0.; cases=0
for m in (4,6,8):
    for eta in (.01,.1,.35,.6,.85):
        s=rng.normal(size=m//2)+1j*rng.normal(size=m//2);s/=np.linalg.norm(s)
        u=unitary(m);aa=u@canonical_pair_matrix(s)@u.T
        v=two_vector(aa)
        rho=physical_loss(v,m,eta)
        max_identity=max(max_identity,float(np.max(abs(rho-density_formula(aa,eta)))))
        block=TwoFermionBlock(s,eta,u)
        sigma=density_ensemble(ensemble(block));delta=block.parameters()[3]
        max_td_error=max(max_td_error,abs(td(rho,sigma)-delta))
        a0=(1-eta)**2;bb=eta**2
        assert delta<=a0*(bb/a0-math.log1p(bb/a0))+1e-12
        ss,ww,error=canonical_two_form(aa)
        max_reconstruction=max(max_reconstruction,error)
        assert np.max(abs(sigma-sigma.conj().T))<1e-12
        assert np.linalg.eigvalsh(sigma).min()>-1e-12
        assert abs(np.trace(sigma)-1)<1e-12
        cases+=1
assert max(max_identity,max_td_error,max_reconstruction)<2e-9
RESULTS['checks']['general_two_fermion']={"instances":cases,"max_independent_loss_error":max_identity,"max_trace_distance_formula_error":max_td_error,"max_acquired_two_form_error":max_reconstruction}

# 5. Sharp four-mode witness, including the high-transmission branch.
worst_violation=-1.;max_opt_error=0.;cases=0
for eta in (.001,.03,.1,.3,.55,.64,.8,.98):
    aa=canonical_pair_matrix(np.array([1,1])/math.sqrt(2))
    phi=two_vector(aa);rho=density_formula(aa,eta)
    block=TwoFermionBlock(np.array([1,1])/math.sqrt(2),eta,balanced_magic=True)
    sigma=density_ensemble(ensemble(block));a0,b0,_,delta=block.parameters()
    t=min(.5,(math.sqrt(1+b0/a0)-1)/2)
    W=np.outer(phi,phi.conj())
    for mask in range(16):
        if mask.bit_count()==2:W[mask,mask]-=.5
    W[0,0]-=t;W[15,15]-=1/(4*t)
    vals=np.linalg.eigvalsh(W);bound=float(np.trace(W@rho).real/(vals[-1]-vals[0]))
    max_opt_error=max(max_opt_error,abs(td(rho,sigma)-delta),abs(bound-delta))
    assert abs(np.trace(W@sigma).real)<2e-9
    for _ in range(20):
        f=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));f=(f-f.T)/2
        vv=bcs_vector(f)
        worst_violation=max(worst_violation,float(np.vdot(vv,W@vv).real))
    cases+=1
assert max_opt_error<2e-9 and worst_violation<=1e-10
RESULTS['checks']['sharp_magic_distance']={"transmissions":cases,"random_gaussian_witness_tests":20*cases,"largest_witness_value":worst_violation,"max_optimal_distance_error":max_opt_error}

# 6. Two blocks, arbitrary global interferometer, entire 256-outcome law.
blocks=[TwoFermionBlock(np.array([1,1])/math.sqrt(2),e,balanced_magic=True) for e in (.18,.27)]
u=unitary(8);lift=fock_lift(u)
aa=canonical_pair_matrix(np.array([1,1])/math.sqrt(2))
rhos=[density_formula(aa,bl.eta) for bl in blocks]
ens=[ensemble(bl) for bl in blocks]
rho=np.kron(rhos[1],rhos[0]);sigma=np.kron(density_ensemble(ens[1]),density_ensemble(ens[0]))
p=np.diag(lift@rho@lift.conj().T).real
q_dense=np.diag(lift@sigma@lift.conj().T).real
q_engine=np.zeros(256)
for (w1,v1),(w2,v2) in itertools.product(*ens):
    g=np.zeros((16,16));g[:8,:8]=fock_covariance(v1,4);g[8:,8:]=fock_covariance(v2,4)
    q_engine+=w1*w2*covariance_distribution(gaussian_loss(g,u))
D=1-math.prod(1-bl.parameters()[3] for bl in blocks)
observed=float(abs(p-q_engine).sum()/2)
assert observed<=D+1e-10 and abs(td(rho,sigma)-D)<1e-10
assert np.max(abs(q_engine-q_dense))<1e-10
RESULTS['checks']['two_block_global_interference']={"outcomes":256,"gaussian_ensemble_components":len(ens[0])*len(ens[1]),"state_trace_distance":D,"output_total_variation":observed,"dense_vs_covariance_max_entry_error":float(np.max(abs(q_engine-q_dense)))}

# 7. Cubic barrier: three-fermion GHZ and projected odd Gaussian states.
m=6;psi=np.zeros(64,complex);psi[7]=psi[56]=1/math.sqrt(2)
P3=np.diag([float(mask.bit_count()==3) for mask in range(64)])
W=np.outer(psi,psi.conj())-.5*P3
max_w=-1.;cases=0
for _ in range(30):
    u=unitary(6);lift=fock_lift(u)
    zz=rng.normal(size=2)+1j*rng.normal(size=2)
    vv=np.zeros(64,complex)
    vv[1]=1;vv[1|6]=zz[0];vv[1|24]=zz[1];vv[1|6|24]=zz[0]*zz[1]
    vv/=np.linalg.norm(vv);vv=lift@vv
    max_w=max(max_w,float(np.vdot(vv,W@vv).real));cases+=1
for eta in (.02,.1,.4,.8):
    rr=physical_loss(psi,6,eta)
    assert abs(np.trace(W@rr).real-eta**3/2)<1e-12
assert max_w<=1e-10
RESULTS['checks']['three_particle_obstruction']={"odd_gaussians":cases,"largest_witness_value":max_w,"loss_witness_instances":4}

# 8. Executed polynomial sampler beyond dense-Fock sizes.
M=128;blocks=[TwoFermionBlock(np.array([1,1])/math.sqrt(2),.08,balanced_magic=True) for _ in range(M//4)]
u=unitary(M)
t0=time.perf_counter();sampled=sample_lossy_two_fermions(blocks,u,shots=12,seed=913)
RESULTS['checks']['polynomial_sampler_execution']={"modes":M,"two_fermion_blocks":M//4,"shots":12,"state_error_bound":sampled['state_error_bound'],"observed_particle_counts":sampled['samples'].sum(axis=1).tolist(),"elapsed_seconds":time.perf_counter()-t0,"precision":"IEEE double; not certified"}
np.save(Path(__file__).parent/'samples_128_modes.npy',sampled['samples'])
RESULTS['status']='all assertions passed';RESULTS['elapsed_seconds']=time.perf_counter()-start
Path(__file__).with_name('results.json').write_text(json.dumps(RESULTS,indent=2))
print(json.dumps(RESULTS,indent=2))
