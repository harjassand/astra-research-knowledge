#!/usr/bin/env python3
"""Bounded high-energy seed test with streamed physical cutoff Kraus vectors.

The earlier evaluator/report files remain unchanged. This file uses the same
finite physical cutoff-erasure formula, with an independently cross-checked
streaming implementation to limit memory at input cutoff 256 or 384.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import resource
import time

import numpy as np

import e5_realization as original
import e5_regularized_seeds as seed_tools


seed_tools.Q = Fraction(19,20)
MEAN = 19.
BETA = 1/math.sqrt(MEAN)
CUBIC = math.pi/(8*MEAN**3)
WEIGHTS = [Fraction(1,100),Fraction(1,10),Fraction(1,2)]


def streamed_physical(eta,nu,C,cutoff,batch_size=512):
    start=time.monotonic()
    C=np.asarray(C,dtype=complex)
    r,d=C.shape
    N=d-1
    if abs(np.vdot(C,C).real-1)>1e-10:
        raise ValueError('Purification must be normalized')
    G=1+(1-eta)*nu
    tau=eta/G
    b=cutoff+1
    loss=np.zeros((d,d),float)
    for n in range(d):
        value=tau**n
        for ell in range(n+1):
            loss[ell,n]=math.sqrt(value)
            if ell<n:
                value *= (n-ell)/(ell+1)*(1-tau)/tau
    amp=np.zeros((b,b),float)
    for s in range(b):
        value=G**(-s-1)
        for k in range(cutoff-s+1):
            amp[k,s]=math.sqrt(value)
            value *= (s+k+1)/(k+1)*(G-1)/G
    amp_tail=np.array([original.amp_tail(s,cutoff,G) for s in range(d)])
    amp_retained=np.pad(np.sum(amp**2,axis=0),(0,max(0,d-b)))[:d]
    tails=np.zeros(d)
    retained_prob=np.zeros(d)
    for n in range(d):
        ell=np.arange(n+1)
        probabilities=loss[ell,n]**2
        tails[n]=np.dot(probabilities,amp_tail[n-ell])
        retained_prob[n]=np.dot(probabilities,amp_retained[n-ell])
    joint=np.zeros((r*b,r*b),complex)
    vectors=np.zeros((batch_size,r,b),complex)
    used=0
    count=0
    for ell in range(d):
        for k in range(b):
            s=np.arange(min(N-ell,cutoff-k)+1)
            n=ell+s
            out=k+s
            vectors[used][:,out]=C[:,n]*(loss[ell,n]*amp[k,s])[None,:]
            used+=1
            count+=1
            if used==batch_size:
                v=vectors.reshape(used,r*b)
                joint += v.T@v.conj()
                vectors.fill(0)
                used=0
    if used:
        v=vectors[:used].reshape(used,r*b)
        joint += v.T@v.conj()
    flag=(C*tails[None,:])@C.conj().T
    output=np.einsum('abad->bd',joint.reshape(r,b,r,b))
    return {'retained_rb':joint,'erased_r':flag,'retained_b':output,
            'tp_residual':float(np.max(abs(retained_prob+tails-1))),
            'workspace_vector_bytes':vectors.nbytes,
            'streamed_explicit_workspace_bytes':loss.nbytes+amp.nbytes+joint.nbytes+
                 flag.nbytes+output.nbytes+vectors.nbytes+C.nbytes,
            'retained_kraus_count':count,'stream_batch_size':batch_size,
            'elapsed_seconds':time.monotonic()-start}


def prepare(eta,N,M,profile,partner):
    n=np.arange(N+1,dtype=float)
    phase=np.zeros_like(n) if profile=='geometric_positive' else CUBIC*n**3
    seed=.95**(n/2)*np.exp(1j*phase)
    seed/=np.linalg.norm(seed)
    if partner=='number_weight_n_plus_1':
        other=(n+1)*seed
        formula_partner=partner
    else:
        other=np.exp(1j*BETA*n)*seed
        # Tail and energy formula for any phase rotation, independent of beta.
        formula_partner='phase_shift_pi_over_3'
    other/=np.linalg.norm(other)
    C=np.stack([seed,other])/math.sqrt(2)
    mid=streamed_physical(eta,1,C,M)
    return {'eta':eta,'input_cutoff':N,'output_cutoff':M,'profile':profile,
            'partner':formula_partner,'actual_partner':partner,'seed':seed,'other':other,
            'overlap':np.vdot(seed,other),'seed_energy':float(np.dot(n,abs(seed)**2)),
            'partner_energy':float(np.dot(n,abs(other)**2)),
            'midpoint':mid,'prepare_seconds':mid['elapsed_seconds']}


def evaluate(z,p):
    row=seed_tools.evaluate(z,p)
    row.update(partner=z['actual_partner'],phase_shift_beta=BETA,
               cubic_coefficient=CUBIC if z['profile']!='geometric_positive' else 0.,
               engine='streamed_physical_cutoff',
               streamed_explicit_workspace_bytes=z['midpoint']['streamed_explicit_workspace_bytes'],
               retained_kraus_count=z['midpoint']['retained_kraus_count'],
               stream_batch_size=z['midpoint']['stream_batch_size'])
    return row


def controls():
    rng=np.random.default_rng(81203)
    C=rng.normal(size=(2,13))+1j*rng.normal(size=(2,13))
    C/=np.linalg.norm(C)
    a=streamed_physical(.76,1,C,18,17)
    b=original.ThermalCutoff(.76,1,12,18).apply_purification(C)
    result={'retained_matrix_max_error':float(np.max(abs(a['retained_rb']-b['retained_rb']))),
            'erasure_reference_max_error':float(np.max(abs(a['erased_r']-b['erased_r']))),
            'tp_residual':a['tp_residual']}
    assert result['retained_matrix_max_error']<2e-12
    assert result['erasure_reference_max_error']<2e-12
    return result


def scan(destination,N=256,M=160):
    start=time.monotonic()
    results=[]
    checks=controls()
    for eta in [.76,.78,.8]:
        for profile in ['geometric_positive','scaled_cubic']:
            for partner in ['number_weight_n_plus_1','phase_shift_inverse_sqrt_mean']:
                z=prepare(eta,N,M,profile,partner)
                rows=[evaluate(z,p) for p in WEIGHTS]
                results.extend(rows)
                print(json.dumps({'eta':eta,'profile':profile,'partner':partner,'input_cutoff':N,
                                  'output_cutoff':M,'kernel_seconds':z['prepare_seconds'],
                                  'results':[[r['weight_partner'],r['ic_bits_per_use'],
                                              r['p_output_erasure_finite'],
                                              r['input_ic_continuity_charge_bits_diagnostic']]
                                              for r in rows]}),flush=True)
                partial={'controls':checks,'results':results,'elapsed_seconds':time.monotonic()-start,
                         'positive_capacity_claim':False,'faithfulness_inferred':False}
                Path(destination).write_text(json.dumps(partial,indent=2)+'\n')
    return partial


def refine(destination):
    start=time.monotonic()
    results=[]
    for eta in [.76,.78,.8]:
        z=prepare(eta,384,256,'scaled_cubic','number_weight_n_plus_1')
        for p in WEIGHTS:
            row=evaluate(z,p)
            results.append(row)
            print(json.dumps(row),flush=True)
    data={'controls':controls(),'results':results,'elapsed_seconds':time.monotonic()-start,
          'positive_capacity_claim':False,'faithfulness_inferred':False}
    Path(destination).write_text(json.dumps(data,indent=2)+'\n')
    return data


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['controls','scan','refine'])
    parser.add_argument('--input-cutoff',type=int,default=256)
    parser.add_argument('--output-cutoff',type=int,default=160)
    parser.add_argument('--output')
    args=parser.parse_args()
    if args.mode=='controls':
        print(json.dumps(controls()))
    else:
        default=Path(__file__).with_suffix('.json')
        if args.mode=='refine':
            default=default.with_name(default.stem+'_refinement.json')
        destination=args.output or str(default)
        if args.mode=='scan':
            scan(destination,args.input_cutoff,args.output_cutoff)
        else:
            refine(destination)


if __name__=='__main__':
    main()
