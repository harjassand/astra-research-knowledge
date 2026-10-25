#!/usr/bin/env python3
"""Audit of selective-source completion: load proper logical subcode with
complement source switched off, then turn it on while tracking the EXACT matrix
counterterm. Includes random noncommuting completed controllers.
"""
import numpy as np,json
from scipy.linalg import eigh
rng=np.random.default_rng(10262026)

def randc(shape):
    return rng.normal(size=shape)+1j*rng.normal(size=shape)

results=[]
for trial in range(20):
    n=5; c=2; d=2;B=1.25
    X=randc((n,n)); Q=B*np.eye(n)+X.conj().T@X
    WC=randc((n,c)) * .25
    WD=randc((n,d)) * (10 if trial%2 else 1)
    AD=randc((d,d)); AD=AD.conj().T@AD+.4*np.eye(d)
    A=np.zeros((c+d,c+d),complex);A[c:,c:]=AD
    IC=np.eye(c)
    LC=WC.conj().T@WC
    l,V=eigh(LC)
    C=V@np.diag(1/np.sqrt(1+l))@V.conj().T
    Vcode=np.vstack((C,np.zeros((d,c)), -WC@C))
    residual=[]; derivative_res=[];gaps=[]
    for tau in [0,.00001,.25,.5,.9,1.0]:
        W=np.column_stack((WC,tau*WD))
        G=Q@W
        DD=W.conj().T@Q@W
        HH=np.block([[DD+A,G.conj().T],[G,Q]])
        rr=np.linalg.norm(HH@Vcode)
        # Derivative of R* Q R annihilates code because R V = R' V = 0.
        Wprime=np.column_stack((np.zeros_like(WC),WD))
        Dprime=Wprime.conj().T@Q@W+W.conj().T@Q@Wprime
        Gprime=Q@Wprime
        Hprime=np.block([[Dprime,Gprime.conj().T],[Gprime,np.zeros_like(Q)]])
        rd=np.linalg.norm(Hprime@Vcode)
        if tau in [0,1]:
            ev=eigh(HH,eigvals_only=True)
            gaps.append(float(ev[c]))
        residual.append(float(rr)); derivative_res.append(float(rd))
    Wfull=np.column_stack((WC,WD))
    Lfull=Wfull.conj().T@Wfull
    comm=np.linalg.norm(A@Lfull-Lfull@A)
    results.append({'trial':trial,'offcode_source_scale':10 if trial%2 else 1,
        'controller_noncommutator_norm':float(comm),
        'max_code_eigen_residual':max(residual),
        'max_driven_hamiltonian_derivative_residual':max(derivative_res),
        'code_isometry_residual':float(np.linalg.norm(Vcode.conj().T@Vcode-np.eye(c))),
        'gap_comparison':[float(v) for v in gaps]})
ans={'trials':len(results),'max_noncommutator':max(r['controller_noncommutator_norm'] for r in results),
 'max_eigen_residual':max(r['max_code_eigen_residual'] for r in results),
 'max_derivative_residual':max(r['max_driven_hamiltonian_derivative_residual'] for r in results),
 'max_isometry_residual':max(r['code_isometry_residual'] for r in results),
 'selected_trials':[results[0],results[1],results[19]],
 'scope':'exact coherent code invariance during source completion, assuming off-code coupling and full cross-counterterm controls; not endpoint-only realization'}
with open('/mnt/data/astra_selective_source_completion.json','w') as f:json.dump(ans,f,indent=2)
print(json.dumps(ans,indent=2))
