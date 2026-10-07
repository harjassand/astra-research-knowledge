#!/usr/bin/env python3
"""Additional exact/numerical diagnostics. Not a general counting algorithm.

Run from any working directory. Outputs stability_results.json beside this file.
Dependencies: numpy, scipy, sympy. All random fixtures use a fixed seed.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, log, sqrt
from pathlib import Path
import json
import numpy as np
from scipy.linalg import eigh
import sympy as sp

results = {"scope": "Exact finite identities and numerical diagnostics; not independent proof certification", "tests": {}}
T=results['tests']
# Sharp coherence extremizer: separate polarization of (s+t)^k.
records=[]
for k in range(1,8):
    profile_mass=[]
    for j in range(k+1):
        coefficient=F(1,comb(k,j))
        profile_mass.append(comb(k,j)**2*coefficient**2)
    assert profile_mass==[F(1)]*(k+1)
    norm=sum(profile_mass)
    mean=sum(F(j,k+1) for j in range(k+1))
    var=sum(F(1,k+1)*(F(j)-mean)**2 for j in range(k+1))
    assert var==F(k*(k+2),12)
    # Generalized covariance eigenvalue in the (+A,-B) direction.
    rayleigh=4*var/F(k)  # denominator sum_i E[X_i] v_i^2 = k
    assert rayleigh==F(k+2,3)
    records.append({'k':k,'norm_squared':str(norm), 'cat_coherence':str(F(2,k+1)),
                    'J_variance':str(var),'normalized_covariance_eigenvalue':str(rayleigh),
                    'necessary_FLC_exponent_upper_bound':str(1/rayleigh)})
T['polarized_cat_extremizers']=records

# Direct rational eigenvector check for complete-bipartite easy-plane XXZ.
# H = 1/2 sum_cross (ZZ-XX-YY). Work only in the k-particle sector.
singlets=[]
for k in range(1,5):
    states=[frozenset(x) for x in combinations(range(2*k),k)]
    pos={x:i for i,x in enumerate(states)}
    vec=[F(1,comb(k,len(S.intersection(range(k))))) for S in states]
    image=[F(0) for _ in states]
    for r,S in enumerate(states):
        diagonal=F(0)
        for a in range(k):
            for b in range(k,2*k):
                diagonal+=F((1-2*(a in S))*(1-2*(b in S)),2)
                if (a in S)!=(b in S):
                    U=S.symmetric_difference({a,b})
                    image[pos[U]]-=vec[r]
        image[r]+=diagonal*vec[r]
    E=-F(k*(k+2),2)
    assert image==[E*x for x in vec]
    singlets.append({'k':k,'sector_size':len(states),'eigenvalue':str(E),'exact':'pass'})
T['complete_bipartite_ground_vector']=singlets

# Explicitly reject the attractive but false *unbalanced* fidelity formula.
k=4
product_fidelity=F(1,2)
assert product_fidelity>F(2,k+1)
T['rejected_unbalanced_cat_bound']={
    'false_claim':'Every stable k-particle state has cat fidelity <= 2/(k+1)',
    'counterexample':'The basis state |A> is stable and has fidelity 1/2 with (|A>+|B>)/sqrt(2)',
    'k':k,'fidelity':str(product_fidelity),'false_bound':str(F(2,k+1)),
    'retained_claim':'Coherence 2*v_A*v_B/||v||^2 <= 2/(k+1); the fidelity bound needs balanced endpoint amplitudes.'}

# Check the exact binary-profile fidelity envelope at many rational points.
for k in range(1,13):
    bound=F(1) if k==1 else F(2,3) if k==2 else F(1,2)
    for i in range(1,41):
        r=F(i,10)
        value=(r**k+1)**2/(2*sum(r**(2*j) for j in range(k+1)))
        assert value<=bound
T['cat_fidelity_envelope']={'rational_checks':12*40,'sharp_bounds':{'k=1':'1','k=2':'2/3','k>=3':'1/2'}}

# Positive-boundary gap-free energy bound for random real stoquastic matrices,
# not only the restricted XXZ family. (Counting remains restricted.)
rng=np.random.default_rng(8062027)
energy_checks=[]
for n in range(1,6):
    N=2**n
    for trial in range(4):
        off=rng.uniform(0,1,(N,N)); off=(off+off.T)/2
        np.fill_diagonal(off,0)
        H=np.diag(rng.normal(size=N))-off
        ev,U=eigh(H)
        overlaps=U.T@np.ones(N)/sqrt(N)
        for tau in (0.07,0.5,2.0):
            w=overlaps**2*np.exp(-2*tau*(ev-ev[0]))
            err=float(np.dot(w,ev-ev[0])/w.sum())
            bound=n*log(2)/(2*tau)
            assert err<=bound+1e-11
            energy_checks.append({'n':n,'tau':tau,'energy_error':err,'bound':bound})
T['positive_boundary_gap_free_energy']={'fixtures':len(energy_checks),'max_bound_fraction':max(r['energy_error']/r['bound'] for r in energy_checks)}

# Explicit caution: NOT every vector in a degenerate ground space is stable.
I=np.eye(2); X=np.array([[0,1],[1,0.]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1.,-1.])
def embed_two(n:int,A:np.ndarray,i:int,j:int)->np.ndarray:
    R=np.zeros((2**n,2**n),complex)
    for inp in range(2**n):
        bits=[(inp>>(n-1-a))&1 for a in range(n)]
        c=2*bits[i]+bits[j]
        for r in range(4):
            bs=bits.copy();bs[i],bs[j]=r//2,r%2
            out=sum(bit<<(n-1-a) for a,bit in enumerate(bs))
            R[out,inp]+=A[r,c]
    return R
n=3
H=sum(embed_two(n,-(np.kron(X,X)+np.kron(Y,Y)+np.kron(Z,Z))/2,i,j) for i,j in ((0,1),(1,2)))
ghz=np.zeros(8);ghz[0]=ghz[-1]=1/sqrt(2)
assert np.linalg.norm(H@ghz+ghz)<1e-12
# 1+z1*z2*z3 vanishes at z1=z2=z3=exp(i*pi/3), all in the upper half-plane.
z=np.exp(1j*np.pi/3)
assert abs(1+z**3)<1e-12
T['degenerate_ground_space_caution']={'n':3,'GHZ_eigenvalue':-1,'global_ground_energy':float(eigh(H,eigvals_only=True)[0]),'unstable_GHZ_polynomial':'1+z1*z2*z3','retained_scope':'P0|+>/||P0|+>||, or an individually specified stable input projection, not every ground vector'}

# The scalar bivariate transverse gate is real stable exactly in c<=1.
u,v,c=sp.symbols('u v c',real=True)
q=c+u+v+c*u*v
assert sp.expand(sp.diff(q,u)*sp.diff(q,v)-q*sp.diff(q,u,v))==1-c**2
T['transverse_gate_rayleigh_difference']='exact: 1-c^2'

# Fixed polynomial examples verify positivity-preserving local symbols
# via the real-stable Rayleigh difference criterion on sampled real points.
def qedge(a,b,c,x):
    x1,x2,x3,x4=x
    return a*(x1*x2+x3*x4)+b*(x1*x3+x2*x4)+c*(x1*x4+x2*x3)
xx=sp.symbols('x0:4')
qs=qedge(sp.Rational(1),sp.Rational(6,5),sp.Rational(1,4),xx)
rayleigh=[sp.lambdify(xx,sp.diff(qs,xx[i])*sp.diff(qs,xx[j])-qs*sp.diff(qs,xx[i],xx[j]),'numpy') for i in range(4) for j in range(i+1,4)]
minimum=1e10
for point in rng.normal(size=(200,4)):
    vals=[float(f(*point)) for f in rayleigh]
    minimum=min(minimum,*vals)
    assert min(vals)>-1e-10
T['real_stability_edge_diagnostic']={'real_points':200,'pairwise_tests':1200,'minimum_rayleigh_difference':minimum,'scope':'diagnostic, analytic proof uses quadratic signature'}

results['status']='all checks passed'
path=Path(__file__).with_name('stability_results.json')
path.write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
