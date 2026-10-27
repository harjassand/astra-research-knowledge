#!/usr/bin/env python3
"""Finite Dwork specialization for bounded univariate Laurent phases.
No field-element enumeration occurs in production. Depends on the already
validated exact unramified-ring arithmetic and splitting coefficients.
"""
from chain_ring_kloosterman import *
from field_kloosterman import Unramified,theta_coefficients
import numpy as np


def laurent_multiply(p,q,h):
    out={}
    for i,a in p.items():
        for j,b in q.items(): out[i+j]=out.get(i+j,0)^gf_mul(a,b,h)
    return {i:a for i,a in out.items() if a}


def trace_fold(poly,h):
    out={}
    q=1<<(h.bit_length()-1)
    for e,c in poly.items():
        if e:
            while e%2==0: e//=2; c=gf_pow(c,q//2,h)
        out[e]=out.get(e,0)^c
    return {e:c for e,c in out.items() if c}


def laurent_local_matrix(ring,coefficients,theta,minimum,maximum):
    series={0:ring.one}; modmask=ring.mask
    for exponent,residue in sorted(coefficients.items()):
        if not residue: continue
        A=ring.teich(residue); powers=[ring.one]
        for _ in range(1,len(theta)): powers.append(ring.mul(powers[-1],A))
        factor=[(exponent*u,tuple((int(x)*theta[u])&modmask for x in powers[u]))
                for u in range(len(theta)) if theta[u]]
        out={}
        for a,x in series.items():
            for b,y in factor:
                if not minimum<=a+b<=maximum: continue
                v=ring.mul(x,y); old=out.get(a+b,(0,)*ring.d)
                out[a+b]=tuple((i+j)&modmask for i,j in zip(old,v))
        series={e:c for e,c in out.items() if any(c)}
    coeff=np.zeros((ring.d,maximum-minimum+1),dtype=ring.dtype)
    for e,c in series.items(): coeff[:,e-minimum]=c
    states=np.arange(minimum,maximum+1)
    ix=2*states[:,None]-states[None,:]-minimum
    valid=(ix>=0)&(ix<coeff.shape[1])
    return coeff[:,np.clip(ix,0,coeff.shape[1]-1)]*valid[None,:,:]


def laurent_dwork(poly,h,*,details=False):
    if not irreducible_binary(h): raise ValueError('irreducible field presentation required')
    d=h.bit_length()-1; q=1<<d
    if any(not isinstance(e,int) or not isinstance(c,int) or not 0<=c<q for e,c in poly.items()):
        raise ValueError('invalid Laurent coefficients')
    poly=trace_fold(poly,h); constant=poly.pop(0,0); sign=1-2*gf_trace(constant,h)
    if not poly:
        answer=sign*(q-1); data=dict(matrix_dimension=1,field_points_enumerated=0,constant=True)
        return (answer,data) if details else answer
    N=d+2; theta=theta_coefficients(N); ring=Unramified(h,N)
    minimum=min(0,4*min(poly)*N+1)
    maximum=max(0,4*max(poly)*N-1)
    matrix=None; co=dict(poly)
    for _ in range(d):
        current=laurent_local_matrix(ring,co,theta,minimum,maximum)
        matrix=current if matrix is None else ring.matrix_mul(current,matrix)
        co={e:gf_mul(c,c,h) for e,c in co.items()}
    residues=[((q-1)*int(np.trace(matrix[j])))&ring.mask for j in range(d)]
    assert not any(residues[1:]),(poly,h,residues)
    answer=residues[0]
    if answer>=1<<(N-1): answer-=1<<N
    assert abs(answer)<=q-1,(poly,h,answer)
    answer*=sign
    data=dict(residue_degree=d,precision_bits=N,states=[minimum,maximum],
              matrix_dimension=maximum-minimum+1,field_points_enumerated=0,
              exponents=sorted(poly))
    return (answer,data) if details else answer


def shifted_hesse_sum(h,a,rho=0,sigma=0,tau=0,constant=0,*,details=False):
    """Sum psi(X²Y+XY²+Z³+aXYZ+rho X+sigma Y+tau Z+constant).
    All field degrees and arbitrary linear coefficients are supported,
    whether or not the homogeneous cubic is smooth. At a=0 the phase is
    already binary quadratic and is eliminated directly.
    """
    d=h.bit_length()-1; q=1<<d
    if not irreducible_binary(h) or any(not 0<=x<q for x in (a,rho,sigma,tau,constant)):
        raise ValueError('valid field presentation and field elements required')
    if not a:
        def value(bits):
            x,y,z=[(bits>>(i*d))&(q-1) for i in range(3)]
            phase=gf_mul(gf_mul(x,x,h),y,h)^gf_mul(x,gf_mul(y,y,h),h)^gf_mul(gf_mul(z,z,h),z,h)
            phase^=gf_mul(rho,x,h)^gf_mul(sigma,y,h)^gf_mul(tau,z,h)^constant
            return gf_trace(phase,h)
        answer=quadratic_sum(value,3*d)
        data=dict(method='binary quadratic elimination',quadratic_dimension=3*d,field_points_enumerated=0)
        return (answer,data) if details else answer
    inv=gf_pow(a,q-2,h)
    z={2:inv,-1:inv}
    if rho: z[-2]=gf_mul(inv,rho,h)
    z3=laurent_multiply(laurent_multiply(z,z,h),z,h)
    phase=dict(z3); phase[2]=phase.get(2,0)^sigma
    for e,c in z.items(): phase[e]=phase.get(e,0)^gf_mul(tau,c,h)
    phase=trace_fold(phase,h)
    assert set(phase)<={0,3,1,-1,-3,-5}
    torus,meta=laurent_dwork(phase,h,details=True)
    gaussian=0
    if not rho:
        def value(x):
            return gf_trace(gf_mul(gf_mul(x,x,h),x,h)^gf_mul(tau,x,h),h)
        gaussian=quadratic_sum(value,d)
    answer=q*(1-2*gf_trace(constant,h))*(torus+gaussian)
    data=dict(laurent_phase=phase,torus_sum=torus,zero_Y_gaussian=gaussian,**meta)
    return (answer,data) if details else answer
