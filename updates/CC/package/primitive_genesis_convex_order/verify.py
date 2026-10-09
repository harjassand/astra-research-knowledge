#!/usr/bin/env python3
"""Finite diagnostics for the Genesis convex-order continuation.

These checks do not prove the all-horizon theorem, the all-mode spectral gap,
or historical novelty. Run with Python 3 + numpy, scipy, sympy.
"""
from __future__ import annotations
import itertools
import json
import math
from pathlib import Path
import numpy as np
import scipy
from scipy.special import logsumexp
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
import sympy as sp

ROOT = Path(__file__).resolve().parent
RESULTS: list[dict] = []

def check(name: str, condition: bool, **data: object) -> None:
    if not condition:
        raise RuntimeError(f"FAILED: {name}: {data}")
    RESULTS.append({"name": name, "passed": True, **data})

def logmix(z: np.ndarray, nodes: np.ndarray, weights: np.ndarray, r: float) -> np.ndarray:
    return logsumexp(np.log(weights)[None, :] - ((z[:, None]-nodes[None, :])/r)**2/2,
                     axis=1) - math.log(r*math.sqrt(2*math.pi))

def mix_expect(nodes, weights, r, fun, degree=160):
    x, w = np.polynomial.hermite.hermgauss(degree)
    return float(sum(p*np.dot(w, fun(c+math.sqrt(2)*r*x))/math.sqrt(math.pi)
                     for c,p in zip(nodes,weights)))

def mixture_kl(nodes, weights, r, other_nodes=None, other_weights=None, degree=160):
    def f(z):
        numerator = logmix(z, nodes, weights, r)
        if other_nodes is None:
            denominator = -z*z/(2*r*r)-math.log(r*math.sqrt(2*math.pi))
        else:
            denominator = logmix(z,other_nodes,other_weights,r)
        return numerator-denominator
    return mix_expect(nodes,weights,r,f,degree)

# 1. Exact gate identities and finite second-moment design.
c,s = sp.Rational(3,5),sp.Rational(4,5)
Rx=sp.Matrix([[1,0,0],[0,c,-s],[0,s,c]])
Rz=sp.Matrix([[c,-s,0],[s,c,0],[0,0,1]])
for name,R in [('Rx',Rx),('Rz',Rz)]:
    check(f'{name}_orthogonal_exact',R.T*R==sp.eye(3))
    check(f'{name}_determinant_exact',R.det()==1)
Ux=sp.Matrix([[2,-sp.I],[-sp.I,2]])/sp.sqrt(5)
Uz=sp.diag(2-sp.I,2+sp.I)/sp.sqrt(5)
for name,U in [('Ux',Ux),('Uz',Uz)]:
    check(f'{name}_unitary_exact',sp.simplify(U.conjugate().T*U)==sp.eye(2))
    check(f'{name}_determinant_exact',sp.simplify(U.det())==1)
paulis=[sp.Matrix([[0,1],[1,0]]),sp.Matrix([[0,-sp.I],[sp.I,0]]),sp.diag(1,-1)]
for name,U,R in [('x',Ux,Rx),('z',Uz,Rz)]:
    induced=sp.Matrix(3,3,lambda i,j: sp.simplify(sp.trace(paulis[i]*U*paulis[j]*U.conjugate().T)/2))
    check(f'{name}_Bloch_rotation_exact',induced==R)
axes=[sign*sp.eye(3)[:,j] for j in range(3) for sign in [-1,1]]
cov=sum((v*v.T for v in axes),sp.zeros(3))/6
check('six_preparation_second_moment_exact',cov==sp.eye(3)/3)
a=(sp.Rational(1,3)/3-2*sp.Rational(1,72))**2
check('accuracy_to_moment_constant_exact',a==sp.Rational(1,144))
check('explicit_lower_bound_denominator_exact',1536*144**3==4586471424)

# 2. The conditional-mean/martingale identity, including gate-dependent output masses.
rng=np.random.default_rng(604534)
gates=np.stack([np.eye(3),np.array(Rx,float),np.array(Rx.T,float),np.array(Rz,float),np.array(Rz.T,float)])
for case in range(12):
    n=7
    p=rng.dirichlet(np.ones(n))
    v=rng.normal(size=(n,3)); v /= np.maximum(1,np.linalg.norm(v,axis=1))[:,None]
    kernels=np.stack([rng.dirichlet(np.ones(n),size=n) for _ in gates])
    joint=p[None,:,None]*kernels/len(gates)
    rotated=np.einsum('gab,ib->gia',gates,v)
    pout=joint.sum(axis=(0,1))
    vout=np.einsum('gij,gik->jk',joint,rotated)/pout[:,None]
    m0=float(np.dot(p,(v*v).sum(axis=1)))
    m1=float(np.dot(pout,(vout*vout).sum(axis=1)))
    loss=float(np.einsum('gij,gij->',joint,((rotated[:,:,None,:]-vout[None,None,:,:])**2).sum(axis=-1)))
    check(f'martingale_variance_identity_{case}',abs((m0-m1)-loss)<2e-13,
          residual=abs((m0-m1)-loss))

# 3. Gaussian KL reverse-triangle inequality on random convex-order pairs.
for case in range(24):
    nodes=np.sort(rng.uniform(-1,1,size=7))
    weights=rng.dirichlet(np.ones(7))
    assign=rng.dirichlet(np.ones(3),size=7)
    coupling=weights[:,None]*assign
    wy=coupling.sum(axis=0)
    y=(coupling*nodes[:,None]).sum(axis=0)/wy
    r=float(rng.uniform(0.35,1.1))
    dx=mixture_kl(nodes,weights,r)
    dy=mixture_kl(y,wy,r)
    dxy=mixture_kl(nodes,weights,r,y,wy)
    gap=dx-dy-dxy
    dx2=mixture_kl(nodes,weights,r,degree=240)
    dy2=mixture_kl(y,wy,r,degree=240)
    dxy2=mixture_kl(nodes,weights,r,y,wy,degree=240)
    check(f'Gaussian_convex_order_triangle_{case}',gap>=-1e-11 and
          max(abs(dx-dx2),abs(dy-dy2),abs(dxy-dxy2))<2e-9,
          jensen_gap=gap,quadrature_discrepancy=max(abs(dx-dx2),abs(dy-dy2),abs(dxy-dxy2)))

# 4. Entropy-production bound: an exact finite-group analogue, tested numerically.
n=9
Q=(np.eye(n)+np.roll(np.eye(n),1,axis=0)+np.roll(np.eye(n),-1,axis=0))/3
spectrum=np.linalg.eigvalsh(Q)
lambda0=float(np.max(np.abs(spectrum[:-1])))
beta=1-lambda0**2
for case in range(20):
    p=rng.dirichlet(np.full(n,0.4))
    qp=Q@p
    entropy=lambda x:float(-np.dot(x,np.log(x)))
    production=entropy(qp)-entropy(p)
    anisotropy=1-float(np.sum(np.sqrt(p))**2/n)
    check(f'finite_group_entropy_production_{case}',production+1e-13>=beta*anisotropy,
          production=production,bound=beta*anisotropy)

# 5. Finite-mode diagnostics only; not a proof of an all-mode spectral gap.
theta=math.atan2(4,3)
harmonics=[]
for ell in range(1,25):
    ms=np.arange(-ell,ell+1,dtype=float)
    Jx=np.zeros((2*ell+1,2*ell+1))
    for j,m in enumerate(ms[:-1]):
        Jx[j,j+1]=Jx[j+1,j]=math.sqrt(ell*(ell+1)-m*(m+1))/2
    eig,U=np.linalg.eigh(Jx)
    cosx=(U*np.cos(theta*eig))@U.T
    block=(np.eye(2*ell+1)+2*cosx+2*np.diag(np.cos(theta*ms)))/5
    ev=np.linalg.eigvalsh(block)
    lam=float(np.max(np.abs(ev)))
    harmonics.append({'ell':ell,'largest_absolute_eigenvalue':lam,'smallest_eigenvalue':float(ev[0]),'largest_eigenvalue':float(ev[-1])})
    check(f'finite_harmonic_block_{ell}',lam<1-1e-9 and ev[0]>=-0.6-1e-12,
          largest_absolute_eigenvalue=lam)
(ROOT/'harmonic_diagnostics.json').write_text(json.dumps({'scope':'Degrees 1 through 24 only. Does not certify the full spectral gap.','blocks':harmonics},indent=2)+'\n')

# 6. Exact rational finite-horizon construction on a coarse octahedron.
V=sp.Matrix.hstack(*[3*v for v in axes]).T # each row is a vertex
alpha=sp.Rational(1,3)
T=3
delta=sp.Rational(1,3)**(T+1)

def octa_bary(z):
    weights=[sp.Rational(0)]*6
    for j in range(3):
        val=z[j]
        if val>=0:weights[2*j+1]=val/3
        else:weights[2*j]=-val/3
    residual=1-sum(weights)
    weights[0]+=residual/2;weights[1]+=residual/2
    return sp.Matrix([weights])

exact_gates=[sp.eye(3),Rx,Rx.T,Rz,Rz.T]
Ps=[]
for k,R in enumerate(exact_gates):
    P=sp.Matrix.vstack(*[octa_bary(alpha*R*V[i,:].T) for i in range(6)])
    check(f'exact_octahedral_kernel_{k}',all(x>=0 for x in P) and P*sp.ones(6,1)==sp.ones(6,1) and P*V==alpha*V*R.T)
    Ps.append(P)
word_checks=0
for length in range(T+1):
    response=sp.Matrix([(1+delta*alpha**(-length)*V[j,2])/2 for j in range(6)])
    check(f'exact_readout_range_{length}',all(0<=z<=1 for z in response))
    for word in itertools.product(range(5),repeat=length):
        for x in axes:
            p=octa_bary(x); target=x
            for k in word:
                p=p*Ps[k];target=exact_gates[k]*target
            actual=(p*response)[0]
            expected=(1+delta*target[2])/2
            if actual!=expected: raise RuntimeError('Exact finite-word identity failed')
            word_checks+=1
check('exact_words_all_preparations',True,comparisons=word_checks,max_length=T,
      delta=str(delta),note='Coarse fixed grid and a small delta verify the compensation identity, not the asymptotic state count.')

# 7. A finer numerical polytope with delta=1/3; verifies exact-formula reconstruction.
nhalf=32
j=np.arange(nhalf)
z=1-2*(j+0.5)/nhalf
phi=j*math.pi*(3-math.sqrt(5))
pts=np.column_stack((np.sqrt(1-z*z)*np.cos(phi),np.sqrt(1-z*z)*np.sin(phi),z))
pts=np.vstack((pts,-pts))
hull=ConvexHull(pts)
a_poly=float(np.min(-hull.equations[:,-1]))
W=pts/a_poly
n=len(W)
Aeq=np.vstack((np.ones(n),W.T))
def bary(z):
    sol=linprog(np.zeros(n),A_eq=Aeq,b_eq=np.r_[1,z],bounds=(0,None),method='highs')
    if not sol.success:raise RuntimeError(sol.message)
    return sol.x
num_P=[np.vstack([bary(R@v) for v in pts]) for R in gates]
for k,(P,R) in enumerate(zip(num_P,gates)):
    check(f'fine_polytope_kernel_{k}',np.min(P)>=-1e-11 and np.max(abs(P.sum(axis=1)-1))<1e-10 and np.max(abs(P@W-a_poly*W@R.T))<1e-10)
max_t=int(math.floor(math.log(1/3)/math.log(a_poly)))-1
check('fine_polytope_readout_headroom',max_t>=3 and (1/3)*a_poly**(-max_t-1)<=1+1e-12,
      states=n,alpha=a_poly,max_exact_horizon=max_t)
errors=[]
for case in range(80):
    t=int(rng.integers(0,max_t+1));word=rng.integers(0,5,size=t)
    x=rng.normal(size=3);x/=np.linalg.norm(x)
    u=rng.normal(size=3);u/=np.linalg.norm(u)
    p=bary(x);actual_x=x.copy()
    for k in word:p=p@num_P[k];actual_x=gates[k]@actual_x
    h=(1+(1/3)*a_poly**(-t)*(W@u))/2
    observed=float(p@h);target=(1+(1/3)*float(u@actual_x))/2
    errors.append(abs(observed-target))
check('fine_polytope_random_word_responses',max(errors)<1e-10,
      comparisons=len(errors),maximum_probability_error=max(errors),scope='Floating-point diagnostics; the symbolic formula is exact in the proof.')

# 8. Counterexamples: raw Gaussian KL is not an order-complete invariant.
mu_nodes=np.array([-1.,2.]);mu_weights=np.array([2/3,1/3])
nu_nodes=-mu_nodes
for r in [0.4,0.8,1.4]:
    d1=mixture_kl(mu_nodes,mu_weights,r)
    d2=mixture_kl(nu_nodes,mu_weights,r)
    check(f'reflection_incompleteness_{r}',abs(d1-d2)<1e-12)
call=lambda nodes,w,t:float(np.dot(w,np.maximum(nodes-t,0)))
check('reflection_pair_incomparable_calls',call(mu_nodes,mu_weights,1)>call(nu_nodes,mu_weights,1) and call(mu_nodes,mu_weights,-1)<call(nu_nodes,mu_weights,-1))
# Mutual information may increase after a mean-preserving contraction.
small_nodes=np.array([-0.02,0.02]); small_w=np.array([0.5,0.5])
spread_nodes=np.array([-1.,0.,1.]);spread_w=np.array([0.01,0.98,0.01]);r=0.001
Ismall=float(np.dot(small_w,small_nodes**2)/(2*r*r)-mixture_kl(small_nodes,small_w,r))
Ispread=float(np.dot(spread_w,spread_nodes**2)/(2*r*r)-mixture_kl(spread_nodes,spread_w,r))
check('mutual_information_not_convex_order_monotone',Ismall>Ispread+0.5,
      information_contracted=Ismall,information_spread=Ispread,
      note='The proof uses the finite-alphabet r->0 limit, not this quadrature.')

# 9. Gaussian log-score probes recover finite maxima of affine functions.
slopes=np.array([-1.3,-0.2,0.5,1.1])
intercepts=np.array([-0.2,0.3,-0.4,0.1])
probe_input=np.array([-1.0,0.2,0.7]);probe_p=np.array([0.2,0.4,0.4])
poly=lambda z:np.max(z[:,None]*slopes[None,:]+intercepts[None,:],axis=1)
poly_expect=float(np.dot(probe_p,poly(probe_input)))
for k in [5,20,80,200]:
    r=1/k
    logweights=k*intercepts+slopes**2/2
    logZ=float(logsumexp(logweights))
    weights=np.exp(logweights-logZ)
    centers=slopes/k
    z=np.linspace(-2,2,31)
    direct=logmix(z,centers,weights,r)+z*z/(2*r*r)+math.log(r*math.sqrt(2*math.pi))
    symbolic=logsumexp(k*(z[:,None]*slopes[None,:]+intercepts[None,:]),axis=1)-logZ
    check(f'Gaussian_probe_likelihood_identity_{k}',np.max(abs(direct-symbolic))<1e-9,
          maximum_residual=float(np.max(abs(direct-symbolic))))
    smoothed=mix_expect(probe_input,probe_p,r,lambda z:logsumexp(k*(z[:,None]*slopes[None,:]+intercepts[None,:]),axis=1)/k)
    error=abs(smoothed-poly_expect)
    bound=(math.log(len(slopes))+float(np.max(abs(slopes)))*math.sqrt(2/math.pi))/k
    check(f'Gaussian_probe_convex_approximation_{k}',error<=bound+1e-10,
          measured_error=error,proved_upper_bound=bound)

receipt={'status':'All finite checks passed. Not a proof-assistant or external verification.',
         'check_groups':len(RESULTS),'exact_word_comparisons':word_checks,
         'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__,
         'results':RESULTS}
(ROOT/'verification_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='results'},indent=2))
