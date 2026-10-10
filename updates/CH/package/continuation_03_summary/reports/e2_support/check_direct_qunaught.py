#!/usr/bin/env python3
"""Uncertified direct-thermal Chernoff diagnostics for structured GKP pairs.

This is a finite-envelope comb family, not Fock-coefficient optimization.
Fock/input/output truncations and discarded inverse-power tails are reported.
The numbers cannot certify a capacity witness.
"""
import json
import math
from pathlib import Path
import numpy as np


def gaussian_fock(q,p,width,dimension):
    d=width*width
    coeff=np.zeros(dimension,dtype=complex)
    coeff[0]=math.sqrt(2*width/(1+d))*np.exp(
        -q*q/(2*(1+d))-d*p*p/(2*(1+d))+1j*q*p/(1+d))
    linear=math.sqrt(2)*(q+1j*d*p)/(1+d)
    quadratic=(d-1)/(d+1)
    for n in range(dimension-1):
        coeff[n+1]=linear*coeff[n]/math.sqrt(n+1)
        if n:
            coeff[n+1]+=quadratic*math.sqrt(n/(n+1))*coeff[n-1]
    return coeff


def qunaught_pair(aspect,width,dimension=100):
    period=math.sqrt(2*math.pi)*aspect
    momentum_shift=math.pi/period
    images=math.ceil(8/(width*period))+1
    vectors=[]
    raw_norms=[]
    for p in [0,momentum_shift]:
        vector=np.zeros(2*dimension,dtype=complex)
        for j in range(-images,images+1):
            q=j*period
            vector+=math.exp(-width*width*q*q/2)*gaussian_fock(q,p,width,2*dimension)
        raw_norms.append(float(np.vdot(vector,vector).real))
        vectors.append(vector)
    full_vectors=[v/math.sqrt(np.vdot(v,v).real) for v in vectors]
    input_tail=max(float(np.vdot(v[dimension:],v[dimension:]).real) for v in full_vectors)
    v0,v1=[v[:dimension].copy() for v in full_vectors]
    v0/=math.sqrt(np.vdot(v0,v0).real)
    overlap=np.vdot(v0,v1)
    v1-=overlap*v0
    v1/=math.sqrt(np.vdot(v1,v1).real)
    energies=[float(np.sum(np.arange(dimension)*np.abs(v)**2)) for v in [v0,v1]]
    return v0,v1,dict(input_tail_at_double_cutoff=input_tail,
                      pair_overlap_before_orthogonalization=abs(overlap),
                      mean_photons=energies,comb_images=2*images+1)


def thermal_outputs(v0,v1,eta,nu=1,output_dimension=160):
    n=len(v0)
    inputs=np.stack([np.outer(v0,v0.conj()),np.outer(v1,v1.conj()),
                     np.outer(v0,v1.conj())])
    gain=1+(1-eta)*nu
    transmissivity=eta/gain
    lost=np.zeros_like(inputs)
    for ell in range(n):
        size=n-ell
        coefficient=np.zeros(size)
        coefficient[0]=(1-transmissivity)**(ell/2)
        for a in range(size-1):
            coefficient[a+1]=coefficient[a]*math.sqrt((a+ell+1)/(a+1)*transmissivity)
        lost[:,:size,:size]+=coefficient[:,None]*coefficient[None,:]*inputs[:,ell:,ell:]
    amplified=np.zeros((3,output_dimension,output_dimension),dtype=complex)
    for ell in range(output_dimension):
        size=min(n,output_dimension-ell)
        coefficient=np.zeros(size)
        coefficient[0]=gain**(-.5)*((gain-1)/gain)**(ell/2)
        for a in range(size-1):
            coefficient[a+1]=coefficient[a]*math.sqrt((a+ell+1)/(a+1)/gain)
        amplified[:,ell:ell+size,ell:ell+size]+=coefficient[:,None]*coefficient[None,:]*lost[:,:size,:size]
    return amplified


def convex_minimum(base,slope):
    def evaluate(s):
        weights=np.exp(base+s*slope)
        return float(np.sum(weights)),float(np.sum(weights*slope))
    if evaluate(0)[1]>=0:
        s=0.
    elif evaluate(1)[1]<=0:
        s=1.
    else:
        lo,hi=0.,1.
        for _ in range(48):
            mid=(lo+hi)/2
            if evaluate(mid)[1]<0:
                lo=mid
            else:
                hi=mid
        s=(lo+hi)/2
    return dict(value=evaluate(s)[0],minimizer=s)


def metrics(outputs,cutoff):
    b0,b1,cross=outputs
    l0,u0=np.linalg.eigh((b0+b0.conj().T)/2)
    l1,u1=np.linalg.eigh((b1+b1.conj().T)/2)
    keep0=l0>cutoff
    keep1=l1>cutoff
    eigen0,eigen1=l0[keep0],l1[keep1]
    u0,u1=u0[:,keep0],u1[:,keep1]
    log0,log1=np.log(eigen0)[:,None],np.log(eigen1)[None,:]
    overlap_squared=np.abs(u0.conj().T @ u1)**2
    cross_squared=np.abs(u0.conj().T @ cross @ u1)**2
    bob_base=np.log(np.maximum(overlap_squared,1e-300))+log1
    eve_base=np.log(np.maximum(cross_squared,1e-300))-log0
    slope=log0-log1
    bob=convex_minimum(bob_base,slope)
    eve=convex_minimum(eve_base,slope)
    return dict(eigenvalue_cutoff=cutoff,bob_chernoff=bob,eve_chernoff_lower_truncation=eve,
                eve_minus_bob=eve['value']-bob['value'],
                discarded_eigenvalue_mass=[float(np.sum(l0[~keep0])),float(np.sum(l1[~keep1]))],
                retained_ranks=[int(np.sum(keep0)),int(np.sum(keep1))])


def main():
    records=[]
    for aspect,width in [(1,.25),(1,.4),(1.68,.25),(1.68,.4)]:
        v0,v1,preparation=qunaught_pair(aspect,width)
        for eta in [.76,.8,.85]:
            outputs=thermal_outputs(v0,v1,eta)
            record=dict(aspect=aspect,envelope_and_peak_width=width,eta=eta,nu=1,
                        input_dimension=100,output_dimension=160,
                        output_trace_defects=[1-float(np.trace(outputs[i]).real) for i in [0,1]],
                        preparation=preparation,
                        metrics=[metrics(outputs,c) for c in [1e-10,1e-12,1e-14]],
                        status='uncertified_finite_envelope_and_Fock_diagnostic')
            records.append(record)
            print(json.dumps(record),flush=True)
    path=Path(__file__).with_name('direct_qunaught_diagnostics.json')
    path.write_text(json.dumps(records,indent=2)+'\n')
    print('saved',path)


if __name__=='__main__':
    main()
