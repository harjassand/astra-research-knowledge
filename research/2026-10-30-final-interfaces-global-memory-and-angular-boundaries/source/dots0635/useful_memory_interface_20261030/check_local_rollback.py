#!/usr/bin/env python3
"""Clean initialized-entry operator regression; NOT a malformed-state test."""
import json
import numpy as np
from scipy.linalg import block_diag,expm
rng=np.random.default_rng(20261030)
L=4;d=2;w=2;p=2;payload=d*w*p
I=np.eye(payload,dtype=complex)
def unitary(n):
    z=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
    q,r=np.linalg.qr(z)
    diag=np.diag(r);return q@np.diag(diag/np.abs(diag))
U=[None]+[block_diag(unitary(d*w),unitary(d*w)) for _ in range(L)]
V=[I]
for j in range(1,L+1):V.append(U[j]@V[-1])
FC=block_diag(*V)
kappa=.8;results=[];max_scalar=max_watch=max_reset=0.
for j0 in range(L+1):
    c=j0+1;H=np.zeros((c*payload,c*payload),complex)
    hc=np.zeros((c,c),complex)
    for ell in range(1,c):
        g=.7+.1*ell
        H[(ell-1)*payload:ell*payload,ell*payload:(ell+1)*payload]=g*U[ell].conj().T
        H[ell*payload:(ell+1)*payload,(ell-1)*payload:ell*payload]=g*U[ell]
        hc[ell-1,ell]=hc[ell,ell-1]=g
    F=block_diag(*V[:c]);scalar_err=np.linalg.norm(F.conj().T@H@F-np.kron(hc,I))
    J=np.zeros((c*payload,(L+1)*payload),complex)
    J[j0*payload:(j0+1)*payload,j0*payload:(j0+1)*payload]=I
    bare=np.zeros_like(J);bare[j0*payload:(j0+1)*payload,j0*payload:(j0+1)*payload]=I
    watch_err=np.linalg.norm(F.conj().T@J@FC-bare)
    P0=np.zeros((c,c),complex);P0[0,0]=1
    killed=-1j*hc-kappa*P0/2
    T=3.*c;E=expm(killed*T)
    gram=np.eye(c)-E.conj().T@E
    eigmin=float(np.linalg.eigvalsh((gram+gram.conj().T)/2)[0])
    assert eigmin>1e-8
    # First-reset density at t, following watchdog entry at this exact prefix.
    t=.61+0.17*j0
    full=expm((-1j*H-kappa*np.kron(P0,I)/2)*t)
    block=full[:payload,j0*payload:(j0+1)*payload]
    scalar=expm(killed*t)[0,j0]
    reset_err=0.
    for prog in range(p):
        entry=np.zeros((payload,d),complex)
        for data in range(d):entry[prog*d*w+data*w,data]=1
        superop=np.zeros((d*d,d*d),complex)
        for outprog in range(p):
            for work in range(w):
                erase=np.zeros((d,payload),complex)
                for data in range(d):erase[data,outprog*d*w+data*w+work]=1
                K=np.sqrt(kappa)*erase@block@V[j0]@entry
                superop+=np.kron(K,K.conj())
        reset_err=max(reset_err,float(np.linalg.norm(superop-kappa*abs(scalar)**2*np.eye(d*d))))
    max_scalar=max(max_scalar,float(scalar_err));max_watch=max(max_watch,float(watch_err));max_reset=max(max_reset,reset_err)
    results.append({'entry_prefix':j0,'rail_dimension':c,'reset_window_T':T,
                    'minimum_absorption_effect_eigenvalue':eigmin,
                    'scalar_gauge_error':float(scalar_err),
                    'watchdog_intertwining_error':float(watch_err),
                    'coarse_grained_abort_identity_superoperator_error':reset_err})
assert max(max_scalar,max_watch,max_reset)<1e-10
print(json.dumps({'seed':20261030,'payload':'program qubit + DATA qubit + workspace qubit',
 'scope':'clean initialized entry, fixed program values; reset labels summed',
 'cases':results,'passed':True},indent=2))
