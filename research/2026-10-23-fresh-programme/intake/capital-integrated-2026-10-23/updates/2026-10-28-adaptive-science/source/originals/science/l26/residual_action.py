#!/usr/bin/env python3
"""Finite residual-action implementation of CORE_THEOREM.md equation (3).

The mathematical convention uses exact Gaussian seeds and real arithmetic.
This NumPy implementation verifies floating implementation algebra; it does
not certify continuous-law TV or supply an original-g residual oracle.
"""
import json
import math
from pathlib import Path
import numpy as np


def correction(G, Z, kappa, residual_action, rng):
    """One call residual_action(YG,YZ,V), including one per batch element.

    All arrays have final axis d. No random loop, derivative, mean, potential,
    or conditional expectation is evaluated. Return correction and diagnostics.
    """
    a = math.sqrt(1-kappa*kappa)
    seeds = rng.normal(size=G.shape[:-1]+(4,))
    num = np.sum(seeds[..., :3]**2, axis=-1, keepdims=True)
    den = np.sum(seeds**2, axis=-1, keepdims=True)
    q = np.divide(num, den, out=np.full_like(num, .5), where=den>0)
    W1, W2 = rng.normal(size=G.shape), rng.normal(size=G.shape)
    YZ = q*Z+np.sqrt(1-q*q)*W1
    YG = (a*G-kappa*(1-q)*Z+kappa*q*np.sqrt((1-q)/(1+q))*W1
          +kappa*np.sqrt(2*q/(1+q))*W2)
    V = (np.sqrt(2*q*(1-q))*Z-np.sqrt(2)*q*np.sqrt(q/(1+q))*W1
         +np.sqrt((1-q)/(1+q))*W2)
    U = -math.pi/(2*math.sqrt(2)*a)*residual_action(YG,YZ,V)
    return U, (YG,YZ,V)


def check():
    rng = np.random.default_rng(27626)
    kappa, d, count = .5, 4, 250000
    a = math.sqrt(1-kappa*kappa)
    G, Z = rng.normal(size=(count,d)), rng.normal(size=(count,d))
    R = np.array([[.2,.1,0,0],[.1,-.3,.05,0],[0,.05,.15,.02],[0,0,.02,.1]])
    action = lambda yg,yz,v: v@R.T
    U, (YG,YZ,V) = correction(G,Z,kappa,action,rng)
    stacked = np.concatenate([YG,YZ,V],axis=1)
    cov = np.cov(stacked,rowvar=False)
    expected_energy = math.pi**2/(8*a*a)*np.sum(R*R)
    target_cond = -(Z@R.T)/(2*a)
    # Conditional means tested using fixed outer points, not only marginals.
    ptsG=np.array([[.2,-.4,.8,1.],[-1.,.3,.1,-.5]])
    ptsZ=np.array([[.7,.2,-.3,.4],[-.1,-.6,.5,1.2]])
    mean_errors=[]
    for g,z in zip(ptsG,ptsZ):
        gg=np.broadcast_to(g,(count,d)); zz=np.broadcast_to(z,(count,d))
        uu,_=correction(gg,zz,kappa,action,rng)
        target=-(R@z)/(2*a)
        mean_errors.append(float(np.linalg.norm(np.mean(uu,axis=0)-target)))
    out={
        'sample_count':count,'dimension':d,
        'product_Gaussian_covariance_max_abs_error':float(np.max(np.abs(cov-np.eye(3*d)))),
        'actual_second_moment':float(np.mean(np.sum(U*U,axis=1))),
        'exact_second_moment':float(expected_energy),
        'second_moment_relative_error':float(abs(np.mean(np.sum(U*U,axis=1))/expected_energy-1)),
        'constant_matrix_conditional_mean_L2_errors':mean_errors,
        'proof_is_in_CORE_THEOREM_not_Monte_Carlo':True,
    }
    assert out['product_Gaussian_covariance_max_abs_error']<.02
    assert out['second_moment_relative_error']<.02
    assert max(mean_errors)<.01
    return out


if __name__=='__main__':
    out=check()
    (Path(__file__).resolve().parent/'action_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
