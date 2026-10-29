#!/usr/bin/env python3
"""Scoped population checks for the finite-duration LC operation.

Requires numpy/scipy from the declared primary runtime. No simulated data,
calibration, asymptotic theorem, or apparatus validation is represented.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm


def cell(k, g, h=1.0, tau=1.0, a=1.0):
    b = 2.0*np.sin(k/2.0)
    # Coordinates (x, q, p, sqrt(tau)*v); a phase rotation makes B=b real.
    K = np.array([[0., 0., 0., b/np.sqrt(tau)],
                  [0., 0., -a*b, g/np.sqrt(tau)],
                  [0., a*b, 0., 0.],
                  [-b/np.sqrt(tau), -g/np.sqrt(tau), 0., 0.]])
    U = expm(h*K)
    return K, U, U[:3,:3], U[:3,3]


def main():
    records = []
    worst = {'orthogonality': 0., 'gibbs_noise': 0.,
             'zero_mode_counter': 0.}
    for g in (0.2, 0.4, 0.7):
        for k in (0., 0.02, 0.2, 1.1):
            K, U, C, f = cell(k,g)
            worst['orthogonality'] = max(worst['orthogonality'],
                float(np.max(np.abs(U.T@U-np.eye(4)))))
            worst['gibbs_noise'] = max(worst['gibbs_noise'],
                float(np.max(np.abs(C@C.T+np.outer(f,f)-np.eye(3)))))
        # Add the integrated current to the zero-mode Hamiltonian flow.
        K,_,_,_ = cell(0.,g)
        Aug = np.zeros((5,5)); Aug[:4,:4]=K; Aug[4,3]=1.
        UJ = expm(Aug)
        counter = np.array([0.,1.,0.,0.,-g])
        worst['zero_mode_counter'] = max(worst['zero_mode_counter'],
            float(np.max(np.abs(counter@UJ-counter))))
        # The finite cell's low-frequency Schur complement, not an Euler step.
        k = 1.e-4
        _,_,C,_ = cell(k,g)
        slow=(0,2)
        Schur=C[np.ix_(slow,slow)]+np.outer(C[list(slow),1],C[1,list(slow)])/(1.-C[1,1])
        target=np.array([[0.,1./g],[-1./g,-2./g**2]])
        cell_error=float(np.max(np.abs((Schur-np.eye(2))/k**2-target)))
        records.append({'g':g,'k':k,'schur_coefficient_max_error':cell_error})
    modes=[]
    for N in (64,256,1024,4096):
        g=(np.log(N+1.))**(-.5)
        k=2*np.pi/N
        _,_,C,_=cell(k,g)
        vals,vecs=np.linalg.eig(C)
        # The density branch is the eigenvector with largest x-coordinate.
        choice=int(np.argmax(np.abs(vecs[0,:])/np.linalg.norm(vecs,axis=0)))
        lam=float(np.real(vals[choice]))
        v=np.real(vecs[:,choice]/vecs[0,choice])
        Dg=(1./g**2)*(1.-np.sqrt(1.-g**2))
        m=int(N*N*.1/2.)  # physical macro t=.1, period h+b=2
        P=np.linalg.matrix_power(C,m)
        variance=float((np.eye(3)-P@P.T)[0,0])
        target_mean=np.exp(-.25*(2*np.pi)**2*.1)
        target_var=1.-np.exp(-.5*(2*np.pi)**2*.1)
        modes.append({'N':N,'g':g,'density_eigenvalue':lam,
            'observed_cycle_diffusivity':(1.-lam)/k**2,
            'cell_limit_diffusivity':Dg,
            'density_eigenvector':[float(t) for t in v],
            'macro_mean_transfer':float(P[0,0]),
            'heat_mean_limit':float(target_mean),
            'zero_start_density_variance':variance,
            'heat_variance_limit':float(target_var)})
    assert worst['orthogonality']<1.e-12
    assert worst['gibbs_noise']<1.e-12
    assert worst['zero_mode_counter']<1.e-12
    assert max(r['schur_coefficient_max_error'] for r in records)<.002
    out={'scope':'Population matrix and exact-operation checks; no acquisition or apparatus claim.',
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'max_residuals':worst,'cell_coefficients':records,'low_mode_receivers':modes,
         'all_required_checks_passed':True}
    target=Path(__file__).with_name('FINITE_PULSE_LC_CHECK.json')
    target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
