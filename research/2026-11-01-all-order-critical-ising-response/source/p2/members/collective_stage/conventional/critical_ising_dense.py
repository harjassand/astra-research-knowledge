"""Independent full-state comparator for nonlinear critical-scale kinetic Ising.

Periodic zero-field Ising, exp(2J)=n, all clocks one.
A_same=1, A_opposite=2. The full Poisson and reference residual solves use
independent spin-space sparse generators, not translation-orbit compilation.
"""
import json
import math
from pathlib import Path
import time

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as sla


def full(n, a_same=1., a_opposite=2.):
    start=time.perf_counter()
    J=.5*math.log(n)
    N=1<<n
    st=np.arange(N,dtype=np.int64)
    spins=1-2*((st[:,None]>>np.arange(n))&1)
    lp=J*np.sum(spins*np.roll(spins,1,axis=1),axis=1)
    p=np.exp(lp-np.max(lp));p/=sum(p)
    rows=[];cols=[];vals=[];vals0=[]
    diag=np.zeros(N);diag0=np.zeros(N)
    for i in range(n):
        L,R=spins[:,(i-1)%n],spins[:,(i+1)%n]
        r0=1/(1+np.exp(2*J*spins[:,i]*(L+R)))
        r=r0*np.where(L==R,a_same,a_opposite)
        rows.extend(st);cols.extend(st^(1<<i));vals.extend(-r);vals0.extend(-r0)
        diag+=r;diag0+=r0
    rows.extend(st);cols.extend(st);vals.extend(diag);vals0.extend(diag0)
    K=sp.csr_matrix((vals,(rows,cols)),shape=(N,N))
    K0=sp.csr_matrix((vals0,(rows,cols)),shape=(N,N))
    M=np.sum(spins,axis=1).astype(float)
    T=np.sum(spins*np.roll(spins,1,axis=1)*np.roll(spins,-1,axis=1),axis=1).astype(float)
    def solve(A,f):
        u=np.zeros(N);u[1:]=sla.spsolve(A[1:,1:],f[1:])
        return u
    var=float(np.dot(p,M*M));energy=float(np.dot(p*M,K@M))
    coeff=var/energy;trial=coeff*M
    residual=M-K@trial
    exactu=solve(K,M);refu=solve(K0,residual)
    chi=float(np.dot(p*M,exactu))
    rnorm=float(np.dot(p*residual,refu))
    lower=var*var/energy
    upper=lower+rnorm/min(a_same,a_opposite)
    gap0=1-math.tanh(2*J)
    chi0=var/gap0
    # Complete conventional two-dimensional Ritz construction for comparison.
    V=np.column_stack([M,T]);H=V.T@(p[:,None]*(K@V));b=V.T@(p*M)
    co=np.linalg.solve(H,b)
    ritz2=float(b@co)
    return {'n':n,'J':J,'states':N,'source':'M=sum_i sigma_i',
            'variance':var,'dirichlet_energy':energy,'ritz_coefficient':coeff,
            'exact_response':chi,'linear_ritz_lower':lower,'reference_residual_upper':upper,
            'relative_certificate_width':(upper-lower)/lower,
            'actual_linear_relative_error':(chi-lower)/chi,
            'reference_residual_norm':rnorm,'glauber_response':chi0,
            'diffusion_universality_prediction':chi0/a_opposite,
            'prediction_relative_error':(chi0/a_opposite-chi)/chi,
            'ritz_MT_lower':ritz2,'ritz_MT_relative_error':(chi-ritz2)/chi,
            'direct_relative_residual':float(np.linalg.norm(K@exactu-M)/np.linalg.norm(M)),
            'seconds':time.perf_counter()-start}


def main():
    out=[]
    for n in [4,6,8,10,12]:
        r=full(n);out.append(r);print(json.dumps(r),flush=True)
    Path(__file__).with_name('critical_ising_dense_results.json').write_text(json.dumps(out,indent=2)+'\n')


if __name__=='__main__':main()
