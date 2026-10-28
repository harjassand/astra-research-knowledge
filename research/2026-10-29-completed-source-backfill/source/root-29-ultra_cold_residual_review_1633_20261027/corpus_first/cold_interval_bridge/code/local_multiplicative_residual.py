"""Concrete all-Schatten certificate interface for disjoint entangled collars.

Numerical source measurements; this file does not claim a small residual or
certified cold purity. The accompanying theorem gives the exact implication.
"""
import sys
sys.dont_write_bytecode = True
import json,time
import numpy as np
from scipy.linalg import svdvals
from seam_residual import LocalSeam, BASE


def measure(source, s):
    local = source.local(s); dim = len(source.states)
    E = np.zeros((dim,dim)); inverse = np.zeros((dim,dim))
    for ix, order, m in source.blocks:
        (w,u),(w0,u0) = source.spectra[m]
        inv = ((u0*np.exp(-s*w0/2))@u0.T)@((u*np.exp(s*w/2))@u.T)
        E[np.ix_(ix,ix)] = local[m][np.ix_(order,order)]
        inverse[np.ix_(ix,ix)] = inv[np.ix_(order,order)]
    R = source.hout@E-(source.hout@E.T).T
    logarithmic = R@inverse
    norm = float(svdvals(logarithmic)[0])
    identity_error = float(np.linalg.norm(E@inverse-np.eye(dim),ord=np.inf))
    return dict(s=s, one_edge_logarithmic_commutator_norm=norm,
        Schur_upper_numeric=float(np.sqrt(np.max(np.sum(np.abs(logarithmic),axis=0))*
                                         np.max(np.sum(np.abs(logarithmic),axis=1)))),
        inverse_identity_diagnostic=identity_error)


def run():
    start=time.monotonic();rows=[]
    for ell in (1,2):
        source=LocalSeam(ell)
        samples=[measure(source,s)for s in (0,.125,.25,.5,.75,1.,1.5)]
        row=dict(ell=ell,min_block_length=2*ell+2,
            all_Schatten_local_error_density_samples=samples)
        rows.append(row)
        print('ell',ell,'beta.75 residual',samples[4],flush=True)
    result=dict(status='ACTUAL_MULTIPLICATIVE_RESIDUAL_MEASURED_NOT_YET_CERTIFIED',
        rows=rows,elapsed_seconds=time.monotonic()-start,
        theorem='For A(0)=I, eta=exp(integral||(A_prime+H*A/2)*A_inverse||)-1 bounds every Schatten-p relative amplitude error.',
        normalized_purity_log_error='4 log((1+eta)/(1-eta)) when eta<1; one amplitude A(beta) supplies both Schatten2 and4, so no independently supplied2beta approximation is assumed.',
        failure_scope='The chosen small-collar ansatz has not acquired the required cold tolerance. Source values remain numerical discovery data, not a certified Gibbs purity.')
    (BASE/'results/MULTIPLICATIVE_RESIDUAL_DISCOVERY.json').write_text(json.dumps(result,indent=2)+'\n')
    print('elapsed',result['elapsed_seconds'])


if __name__=='__main__':run()
