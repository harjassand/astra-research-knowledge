#!/usr/bin/env python3
"""Matrix-free reference implementation for the conditional covariance decoder.

No sampling, stationarity, damping, or covariance-error bound is acquired by
this numerical routine. It consumes observed covariance differences. Memory
O(k*n^2), ordinary dense arithmetic O(k*n^3) per Krylov iteration. It is not
an improved asymptotic dense linear-algebra primitive or a physical compiler.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.sparse.linalg import LinearOperator, lsmr
from research_gate import random_binary_code, stationary_covariance


def make_operator(covariances: np.ndarray) -> LinearOperator:
    cs=np.asarray(covariances,dtype=float)
    if cs.ndim!=3 or cs.shape[1]!=cs.shape[2] or len(cs)==0:
        raise ValueError('Covariances must have shape (k,n,n) with positive k,n')
    if not np.isfinite(cs).all() or not np.allclose(cs,cs.transpose(0,2,1),atol=1e-10):
        raise ValueError('Covariances must be finite and symmetric')
    k,n,_=cs.shape; scale=np.sqrt(k)
    def matvec(v):
        e=np.asarray(v).reshape(n,n)
        return (np.matmul(e,cs)+np.matmul(cs,e.T)).reshape(-1)/scale
    def rmatvec(v):
        r=np.asarray(v).reshape(k,n,n)
        return np.sum(np.matmul(r+r.transpose(0,2,1),cs),axis=0).reshape(-1)/scale
    return LinearOperator((k*n*n,n*n),matvec=matvec,rmatvec=rmatvec,dtype=float)


def decode(covariances, forcings, gamma, tolerance=1e-11, max_iterations=500):
    cs=np.asarray(covariances,dtype=float); ds=np.asarray(forcings,dtype=float)
    if cs.shape!=ds.shape or gamma<=0 or not np.isfinite(gamma):
        raise ValueError('Invalid covariance/forcing shapes or damping')
    op=make_operator(cs)
    rhs=(2*gamma*(cs-ds)).reshape(-1)/np.sqrt(len(cs))
    result=lsmr(op,rhs,atol=tolerance,btol=tolerance,maxiter=max_iterations)
    if result[1] not in (0,1,2,4,5):
        raise ArithmeticError(f'LSMR failed to converge reliably: stop code {result[1]}')
    n=cs.shape[1]
    return result[0].reshape(n,n),{
        'stop_code':int(result[1]),'krylov_iterations':int(result[2]),
        'numerical_rms_equation_residual':float(result[3]),
        'numerical_normal_residual':float(result[4]),
        'covariance_storage_bytes':int(cs.nbytes),
        'explicit_design_storage_bytes_avoided':int(len(cs)*n**4*8)}


def main(output):
    rng=np.random.default_rng(2026100929); records=[]; max_adjoint_error=0.
    for n in [3,5,8,12,32]:
        code,delta=random_binary_code(n,rng)
        ds=np.array([np.diag(1+sgn*row) for row in code for sgn in [-1.,1.]])
        a=rng.normal(size=(n,n)); a/=np.linalg.norm(a,2); gamma=9.
        # A supplied exact mathematical simulator, deliberately labeled as such.
        cs=np.array([stationary_covariance(a-gamma*np.eye(n),2*gamma*d) for d in ds])
        op=make_operator(cs)
        v=rng.normal(size=n*n); w=rng.normal(size=len(cs)*n*n)
        left=float(np.dot(op@v,w)); right=float(np.dot(v,op.rmatvec(w)))
        adjoint_error=abs(left-right)/max(1,abs(left),abs(right))
        max_adjoint_error=max(max_adjoint_error,adjoint_error)
        assert adjoint_error<1e-11
        estimated,diagnostics=decode(cs,ds,gamma)
        error=float(np.linalg.norm(estimated-a))
        assert error<1e-8
        records.append({'n':n,'noise_conditions':len(ds),'code_relative_distance':delta,
                        'frobenius_reconstruction_error':error,**diagnostics})
    result={'status':'CONDITIONAL_NUMERICAL_DECODER; NOT_END_TO_END_PHYSICAL_ACQUISITION',
            'maximum_adjoint_identity_error':max_adjoint_error,'records':records}
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('matrix_free_results.json'))
    main(parser.parse_args().output)
