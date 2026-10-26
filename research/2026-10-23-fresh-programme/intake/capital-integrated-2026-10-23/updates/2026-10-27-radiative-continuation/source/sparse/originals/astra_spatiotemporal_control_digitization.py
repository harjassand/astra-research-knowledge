#!/usr/bin/env python3
"""Independent unitary piecewise-constant audit of sparse time-echo controls."""
import importlib.util, os, json, numpy as np
from scipy.linalg import eigh
spec=importlib.util.spec_from_file_location('sparse','/mnt/data/astra_spatiotemporal_sparse_echo.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
K=len(mod.freq)
base=np.zeros((4+K,4+K),dtype=complex)
base[4:,4:]=np.diag(mod.freq)
base[2:4,4:]=mod.W.conj().T
base[4:,2:4]=mod.W
psi0=np.zeros(4+K,complex);psi0[0]=1
wanted=np.zeros_like(psi0);wanted[1]=np.exp(-1j*mod.mu*mod.T)

def step_transfer(steps):
    dt=mod.T/steps;psi=psi0.copy()
    for j in range(steps):
        H=base.copy()
        H[:4,:4]=mod.state_controls((j+.5)*dt)[2]
        lam,V=eigh(H,check_finite=False,overwrite_a=True)
        psi=V @ (np.exp(-1j*lam*dt)*(V.conj().T@psi))
    return {'steps':steps,'full_state_error':float(np.linalg.norm(psi-wanted)),'vacuum_radiation_residual':float(np.linalg.norm(psi[4:])), 'storage_b_amplitude_abs':float(abs(psi[1])),'norm':float(np.linalg.norm(psi))}
result={'piecewise_constant':[]}
for steps in [16,32,64,128,256]:
    z=step_transfer(steps);result['piecewise_constant'].append(z);print(z,flush=True)
with open('/mnt/data/astra_spatiotemporal_control_digitization_results.json','w') as f:json.dump(result,f,indent=2)
