"""Standard reversible return-kernel route to a rare global-pattern mean.

This is a CONVENTIONAL COMPETITOR, not a claimed new principle or scalable
Gaussian implementation. Full 2**n generator is deliberately used to verify
the identity independently against the killed backward equation.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh, solve


def run(n=8, coupling=1.2, relative_tolerance=.01):
    states=np.arange(2**n)
    spins=2*((states[:,None]>>np.arange(n))&1)-1
    logw=coupling*np.sum(spins*np.roll(spins,1,axis=1),axis=1)
    pi=np.exp(logw-logw.max()); pi/=pi.sum()
    gamma=np.tanh(2*coupling)
    rates=.5*(1-.5*gamma*spins*(np.roll(spins,1,axis=1)+np.roll(spins,-1,axis=1)))
    Q=np.zeros((2**n,2**n))
    for j in range(n): Q[states,states^(1<<j)]=rates[:,j]
    Q[np.diag_indices_from(Q)]=-rates.sum(axis=1)
    target=sum(1<<j for j in range(0,n,2))
    H=-np.sqrt(pi)[:,None]*Q/np.sqrt(pi)[None,:]
    eigen,vec=eigh((H+H.T)/2)
    A=np.sum(vec[target,1:]**2/eigen[1:])
    kernel_mean=A/(pi[target]*(1-pi[target]))
    keep=states!=target
    direct=solve(-Q[keep][:,keep],np.ones(keep.sum()),assume_a='gen')
    direct_mean=np.dot(pi[keep],direct)/(1-pi[target])
    gap=1-gamma
    upper=2*n
    # Positive spectral weights give numerator >= (1-pi_b)/upper.
    # This T makes omitted numerator at most delta*(1-pi_b)/upper.
    T=np.log(upper/(gap*relative_tolerance))/gap
    tail=np.sum(vec[target,1:]**2*np.exp(-eigen[1:]*T)/eigen[1:])
    return dict(n=n,coupling_beta_J=coupling,target_integer=target,
                target_probability=float(pi[target]),
                source='exact equilibrium conditioned off target',
                gap_formula=float(gap),gap_from_full_spectrum=float(eigen[1]),
                spectral_upper_bound=upper,return_numerator=float(A),
                kernel_mfpt=float(kernel_mean),killed_equation_mfpt=float(direct_mean),
                relative_identity_discrepancy=float(abs(kernel_mean-direct_mean)/kernel_mean),
                requested_relative_tail_bound=relative_tolerance,
                integration_horizon=float(T),horizon_over_mfpt=float(T/kernel_mean),
                spectral_relative_tail_estimate=float(tail/A),
                scope='Dense verifier only. Does NOT implement polynomial Gaussian return probability.')


if __name__=='__main__':
    result=run()
    Path(__file__).with_name('return_kernel_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
