#!/usr/bin/env python3
"""Executable finite checks for COMPILER_PROOF.md.

CPU matrices below VERIFY the scalable block constructions; dense exponentials
are not proposed as the quantum implementation. Sources are computed from
explicit one-particle data. No supplied clock, Kraus or Gaussian-gate oracle.
"""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path
import random

import mpmath as mp
import numpy as np

P=Path(__file__).resolve().parent


def norm(x):
    return float(np.linalg.norm(x,2))


def expm(x):
    """Small dense reference, Taylor scaling/squaring without SciPy."""
    x=np.asarray(x,dtype=complex)
    s=max(0,int(math.ceil(math.log2(max(float(np.linalg.norm(x,np.inf)),1e-300)/.25))))
    y=x/(2.**s);z=np.eye(len(x),dtype=complex);term=z.copy()
    for j in range(1,60):
        term=term@y/j;z+=term
        if np.linalg.norm(term,np.inf)<1e-18:break
    for _ in range(s):z=z@z
    return z


def basis(M,K):
    return sorted((n for n in itertools.product(range(K+1),repeat=M) if sum(n)<=K),key=lambda n:(sum(n),n))


def annihilators(M,K):
    states=basis(M,K);idx={n:i for i,n in enumerate(states)};bs=[]
    for mode in range(M):
        b=np.zeros((len(states),len(states)),complex)
        for j,n in enumerate(states):
            if n[mode]:
                u=list(n);u[mode]-=1;b[idx[tuple(u)],j]=math.sqrt(n[mode])
        bs.append(b)
    return states,bs


def permanent(a):
    n=len(a)
    if n==0:return 1.
    return sum(np.prod([a[j,p[j]] for j in range(n)]) for p in itertools.permutations(range(n)))


def gamma(F,K):
    """Small-M,K validation via the defining permanent formula, not runtime algorithm."""
    states=basis(len(F),K);out=np.zeros((len(states),len(states)),complex)
    for i,m in enumerate(states):
        rows=[j for j,n in enumerate(m) for _ in range(n)]
        for j,n in enumerate(states):
            if sum(m)!=sum(n):continue
            cols=[k for k,v in enumerate(n) for _ in range(v)]
            denom=math.sqrt(math.prod(math.factorial(v) for v in m+n))
            out[i,j]=permanent(F[np.ix_(rows,cols)])/denom
    return out


def positive_sqrt(x):
    e,u=np.linalg.eigh((x+x.conj().T)/2)
    assert e.min()>-1e-10
    return (u*np.sqrt(np.maximum(e,0)))@u.conj().T


class CoupledBath:
    """Genuinely coupled, rank-one loss; one slow rate remains as R grows."""
    def __init__(self,R,K=2):
        assert R>=4
        self.R=float(R);self.K=K;self.M=2
        g=math.sqrt(R)
        self.A=np.array([[0,g],[-g,-R]],complex)
        self.E=np.array([[0],[math.sqrt(2*R)]],complex)
        self.H=1j*(self.A-self.A.conj().T)/2
        self.states,self.bs=annihilators(2,K)
        self.d=len(self.states)
        self.G0b=sum(self.A[i,j]*self.bs[i].conj().T@self.bs[j] for i in range(2) for j in range(2))
        sx=np.array([[0,1],[1,0]],complex);sy=np.array([[0,-1j],[1j,0]],complex);sz=np.diag([1.,-1.])
        self.Hs=.7*sz+.31*sy
        self.c=np.array([.12,.08j]);field=sum(self.c[i]*self.bs[i] for i in range(2));field+=field.conj().T
        self.D=np.kron(self.Hs,np.eye(self.d))+np.kron(sx,field)
        self.W=-1j*self.D
        self.G0=np.kron(np.eye(2),self.G0b)
        self.G=self.G0+self.W
        self.L=np.kron(np.eye(2),math.sqrt(2*R)*self.bs[1])
        self.v=1+norm(self.Hs)+2*float(np.linalg.norm(self.c))*math.sqrt(K+1)
        self.tau=1/self.v
        self.A0=2**math.ceil(math.log2(math.sqrt(16+18*K*self.M)))
        self._eig,self._vec=np.linalg.eig(self.G)
        self._inv=np.linalg.inv(self._vec)

    def F(self,t):
        if self.R==4:return math.exp(-2*t)*(np.eye(2)+(self.A+2*np.eye(2))*t)
        slow=-2/(1+math.sqrt(1-4/self.R));fast=-self.R-slow
        return (math.exp(slow*t)*(self.A-fast*np.eye(2))-math.exp(fast*t)*(self.A-slow*np.eye(2)))/(slow-fast)

    def free(self,t):
        return np.kron(np.eye(2),gamma(self.F(t),self.K))

    def nojump(self,t):
        return (self._vec*np.exp(self._eig*t))@self._inv

    def f2(self,t):
        return float(np.linalg.norm(self.E.conj().T@self.F(t))**2)

    def J(self,t):
        F=self.F(t)
        return max(0.,float(2-np.trace(F.conj().T@F).real))

    def event_cdf(self,t):
        return 2*self.K*self.J(t)+16*self.K*self.v**2*self.M*t*t

    def w(self,t):
        return math.sqrt(2*self.K*self.f2(t)+32*self.K*self.v*self.v*self.M*t)


def dyadic_cells(t,R,resolution):
    levels=max(0,math.ceil(math.log2(max(1.,R*t))))
    breaks=sorted(set([0.,t]+[t*2.**(-j) for j in range(1,levels+2)]))
    cells=[]
    for a,b in zip(breaks[:-1],breaks[1:]):
        xx=np.linspace(a,b,resolution+1)
        cells.extend(zip(xx[:-1],xx[1:]))
    return cells


def source_checks(bath,resolution):
    t=bath.tau;cells=dyadic_cells(t,bath.R,resolution)
    stacked=[bath.nojump(t)];midpoint=[bath.nojump(t)]
    for a,b in cells:
        x=(a+b)/2;M=bath.L@bath.nojump(x)
        mass=max(0.,bath.event_cdf(b)-bath.event_cdf(a))
        stacked.append(math.sqrt(mass)/bath.w(x)*M)
        midpoint.append(math.sqrt(b-a)*M)
    V=np.vstack(stacked);Vmid=np.vstack(midpoint)
    gram=V.conj().T@V
    assert norm(gram-np.eye(len(gram)))<.01
    # Algebraic OAA check for the actually acquired finite source block V/A0.
    u,s,vh=np.linalg.svd(V,full_matrices=False)
    q=math.ceil(bath.A0);theta=math.pi/(4*q+2)
    amp=np.sin((2*q+1)*np.arcsin(np.clip(s*math.sin(theta),-1,1)))
    Y=(u*amp)@vh;polar=u@vh
    assert max(abs(amp))<=1+1e-14
    return {'cells_for_CPU_check':len(cells),'source_gram_error':norm(gram-np.eye(len(gram))),
            'clock_source_vs_midpoint':norm(V-Vmid),'midpoint_completeness_error':norm(Vmid.conj().T@Vmid-np.eye(len(gram))),
            'OAA_iterations':q,'OAA_output_to_polar_isometry':norm(Y-polar),
            'source_normalization':bath.A0,'actual_envelope_mass':bath.event_cdf(t),
            'proved_envelope_mass_bound':18*bath.K*bath.M}


def cross_source_check(bath,t,resolution):
    J=bath.J(t);out=np.zeros_like(bath.G)
    # Finite row/column source overlap; both distributions live on the SAME cells.
    for a,b in dyadic_cells(t,bath.R,resolution):
        x=(a+b)/2;f=math.sqrt(bath.f2(x));p=max(0,bath.J(b)-bath.J(a))/J;q=(b-a)/t
        free_jump=bath.L@bath.free(x)/(math.sqrt(bath.K)*f)
        select=free_jump@(bath.D/bath.v)@(bath.nojump(t-x)/4)
        out+=math.sqrt(p*q)*select
    acquired=out*(4*bath.v*math.sqrt(bath.K*t*J))
    target=(bath.L@bath.nojump(t)-bath.L@bath.free(t))/(-1j)
    return norm(acquired-target)


def dyson_check(bath,order=8):
    d=len(bath.G);aug=np.zeros(((order+1)*d,(order+1)*d),complex)
    for k in range(order+1):
        aug[k*d:(k+1)*d,k*d:(k+1)*d]=bath.G0
        if k:aug[k*d:(k+1)*d,(k-1)*d:k*d]=bath.W
    ea=expm(aug*bath.tau)
    approx=sum(ea[k*d:(k+1)*d,:d] for k in range(order+1))
    actual=norm(approx-bath.nojump(bath.tau))
    vt=norm(bath.D)*bath.tau
    bound=math.exp(vt)*vt**(order+1)/math.factorial(order+1)
    assert actual<bound+1e-8
    return {'order':order,'actual_error':actual,'factorial_tail_upper':bound}


def mp_cdf(R,t):
    R=mp.mpf(R);t=mp.mpf(t);g=mp.sqrt(R);A=mp.matrix([[0,g],[-g,-R]])
    if R==4:F=mp.exp(-2*t)*(mp.eye(2)+(A+2*mp.eye(2))*t)
    else:
        slow=-2/(1+mp.sqrt(1-4/R));fast=-R-slow
        F=(mp.exp(slow*t)*(A-fast*mp.eye(2))-mp.exp(fast*t)*(A-slow*mp.eye(2)))/(slow-fast)
    return 2-sum(abs(x)**2 for x in F)


def prefix_source_check(R,tau,B,samples=5):
    """Evaluate the actual prefix rotations, without a table of 2^B masses."""
    rng=random.Random(937);tau=mp.mpf(tau);total=mp_cdf(R,tau);maximum=mp.mpf(0)
    for _ in range(samples):
        a=mp.mpf(0);b=tau;ja=mp.mpf(0);jb=total;product=mp.mpf(1);j=0
        for depth in range(B):
            mid=(a+b)/2;jm=mp_cdf(R,mid)
            p=(jm-ja)/(jb-ja) if jb>ja else mp.mpf(0)
            p=max(mp.mpf(0),min(mp.mpf(1),p))
            bit=int(mp.mpf(rng.random())>=p)
            j=2*j+bit
            if bit:product*=1-p;a=mid;ja=jm
            else:product*=p;b=mid;jb=jm
        exact=(jb-ja)/total
        maximum=max(maximum,abs(product-exact))
    assert maximum<mp.mpf('1e-65')
    return {'time_bits':B,'coherent_prefix_levels':B,'CDF_evaluations_per_path':B+1,
            'leaf_count_not_enumerated':str(2**B),'probability_product_residual':str(maximum)}


def julia_check(bath):
    F=bath.F(.31*bath.tau)
    U=np.block([[F,positive_sqrt(np.eye(2)-F@F.conj().T)],
                [positive_sqrt(np.eye(2)-F.conj().T@F),-F.conj().T]])
    gu=gamma(U,2);states=basis(4,2)
    pick=[i for i,n in enumerate(states) if n[2:]==(0,0)]
    vac=gu[np.ix_(pick,pick)]
    target=gamma(F,2)
    err=norm(vac-target)
    assert err<1e-12 and norm(gu.conj().T@gu-np.eye(len(gu)))<1e-10
    return {'one_particle_unitary_error':norm(U.conj().T@U-np.eye(4)),
            'two_particle_unitary_error':norm(gu.conj().T@gu-np.eye(len(gu))),
            'vacuum_block_error':err}


def run():
    mp.mp.dps=85
    rows=[]
    for R in [4.,40.,4000.,400000.]:
        b=CoupledBath(R,K=2)
        times=[0.,.001/R,.1/R,1/R,b.tau/3,b.tau]
        intertwining=0.;mass_bound=0.
        for t in times:
            F=b.F(t);gf=gamma(F,b.K);vf=(b.E.conj().T@F)[0]
            ann=sum(vf[j]*b.bs[j] for j in range(2))
            exact=b.L@np.kron(np.eye(2),gf)
            constructed=np.kron(np.eye(2),gf@ann)
            intertwining=max(intertwining,norm(exact-constructed))
            assert norm(exact)<=math.sqrt(b.K*b.f2(t))+1e-9
            mass_bound=max(mass_bound,b.J(t))
        assert intertwining<1e-9 and mass_bound<=2+1e-12
        source=source_checks(b,64)
        cross=cross_source_check(b,b.tau,64)
        assert cross<2e-4
        row={'R':R,'K':b.K,'v':b.v,'tau':b.tau,'intertwining_error':intertwining,
             'actual_loss_J_at_tau':b.J(b.tau),'first_event':source,
             'cross_source_Duhamel_error':cross,'Dyson':dyson_check(b),
             'prefix_source':prefix_source_check(str(R),str(b.tau),24+math.ceil(math.log2(R))),
             'Julia_dilation':julia_check(b),
             'generic_normalized_dissipation_over_window':b.tau*norm(b.L)**2}
        rows.append(row)
        print(json.dumps(row),flush=True)
    refinement=[]
    b=CoupledBath(4000.,K=2)
    for q in [16,32,64,128]:
        refinement.append({'resolution':q,**source_checks(b,q),
                           'cross_source_Duhamel_error':cross_source_check(b,b.tau,q)})
    assert refinement[-1]['source_gram_error']<refinement[0]['source_gram_error']
    result={'scope':'Finite amplitude/source/isometry checks for a noncommuting qubit with a coupled rank-one-loss two-mode memory. Dense matrices verify formulas; no fault-tolerant circuit or practical advantage is claimed.',
            'stiffness_sweep':rows,'refinement':refinement}
    (P/'results/loss_clock_checks.json').write_text(json.dumps(result,indent=2))


if __name__=='__main__':run()
