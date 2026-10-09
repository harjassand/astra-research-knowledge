"""Deterministic numerical checks of affine stationary-tilt tomography formulas.

Not formal verification: these tests look for sign/transposition errors, not
novelty or all-quantifier correctness. Execute: python proof_checks.py
"""
import json
import numpy as np
from stationary_tilt_experiment import H, QUARTIC, D, K, B, A_TRUE, U, DIM


def test_exact_fp():
    rng=np.random.default_rng(103)
    xs=rng.normal(size=(1000, DIM))*1.5
    s=-(xs@H)-QUARTIC*xs**3
    hess=-H[None,:,:]-np.array([3*QUARTIC*np.diag(x*x) for x in xs])
    errs=[]
    for i in range(DIM+1):
        a=np.zeros(DIM) if i==0 else A_TRUE[:,i-1]
        u=np.zeros(DIM) if i==0 else U[:,i-1]
        scored=s+a
        drift=s@B.T+u
        divb=np.einsum('ab,nba->n',B,hess)
        # FP divided by p_i = div b+(b+u).score - D:(Hess logp+score score^T)
        val=divb+np.einsum('ni,ni->n',drift,scored)-np.einsum('ij,nji->n',D,hess)-np.einsum('ni,ij,nj->n',scored,D,scored)
        errs.append(float(np.max(np.abs(val))))
    assert max(errs)<1e-10, errs
    return errs


def test_pairwise_identity_affine():
    aa=np.column_stack((np.zeros(DIM),A_TRUE))
    uu=np.column_stack((np.zeros(DIM),U))
    er=[]
    for i in range(DIM+1):
        for j in range(i+1,DIM+1):
            a=aa[:,i]-aa[:,j]
            er.append(abs(float((uu[:,i]-uu[:,j])@a-a@D@a)))
    assert max(er)<1e-12
    return max(er)


def test_lower_bound():
    # Only baseline and first two perturbations observed in d=3.
    _,_,vt=np.linalg.svd(A_TRUE[:,:2].T)
    w=vt[-1,:]
    v=np.array([0.8,-0.6,0.7]);v/=np.linalg.norm(v)
    delta=0.18*np.outer(v,w)
    B_alt=B+delta
    D_alt=(B_alt+B_alt.T)/2
    invisible=np.linalg.norm(B_alt@A_TRUE[:,:2]-U[:,:2])
    assert invisible<1e-12
    assert np.linalg.eigvalsh(D_alt).min()>.1
    assert np.linalg.norm(B_alt-B)>.1
    # The unseen third perturbation breaks the nonidentifiability.
    visible=np.linalg.norm(B_alt@A_TRUE[:,2]-U[:,2])
    assert visible>1e-3
    return {'invisible_two_controls_residual':float(invisible),
            'alternative_generator_distance':float(np.linalg.norm(B_alt-B)),
            'alternative_diffusion_min_eigenvalue':float(np.linalg.eigvalsh(D_alt).min()),
            'third_control_mismatch':float(visible)}


def main():
    out={'fp_density_residual_max_by_regime':test_exact_fp(),
         'pairwise_Fisher_residual_max':test_pairwise_identity_affine(),
         'two_controls_not_enough':test_lower_bound()}
    print(json.dumps(out,indent=2))
    with open('proof_checks_results.json','w') as f:json.dump(out,f,indent=2)

if __name__=='__main__':main()
