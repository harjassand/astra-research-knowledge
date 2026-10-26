#!/usr/bin/env python3
"""Exact failures: fine EPR test records and unaudited last logical output gate."""
from pathlib import Path
import json
import numpy as np
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1.,-1.]).astype(complex)
e0=np.array([1.,0.],complex); e1=np.array([0.,1.],complex)
phi_plus=(np.kron(e0,e0)+np.kron(e1,e1))/np.sqrt(2)
phi_minus=(np.kron(e0,e0)-np.kron(e1,e1))/np.sqrt(2)
psi=(np.kron(phi_plus,e0)+np.kron(phi_minus,e1))/np.sqrt(2)
rho=np.outer(psi,psi.conj())
# The retained bath is in the third qubit; fine outcomes j=ZZ are 00,11.
# Compare complete flagged memory channels actual vs Bell-pinched resource.
proj_plus=np.outer(phi_plus,phi_plus.conj())
proj_minus=np.outer(phi_minus,phi_minus.conj())
Bpinch=sum(np.kron(p,I)@rho@np.kron(p,I) for p in [proj_plus,proj_minus])

def record_state(R, xy):
    v=np.kron(xy[:,None],I) # isometry from M into RBM
    return v.conj().T@R@v

Dflag=0;out=[]
for lab,v in [('00',np.kron(e0,e0)),('11',np.kron(e1,e1))]:
    real=record_state(rho,v)
    ideal=record_state(Bpinch,v)
    diff=real-ideal
    err=np.sum(abs(np.linalg.eigvalsh((diff+diff.conj().T)/2)))/2
    Dflag+=err
    out.append({'fine_result':lab,'probability':float(np.trace(real).real),
                'bath_X_expectation_after_given_record':float(np.trace(X@real).real/np.trace(real).real),
                'half_trace_contribution':float(err)})

# Forgetting the fine result and recording only parity + gives equal bath state.
bath_real=sum(record_state(rho,v) for v in [np.kron(e0,e0),np.kron(e1,e1)])
bath_ideal=sum(record_state(Bpinch,v) for v in [np.kron(e0,e0),np.kron(e1,e1)])
coarse_residual=float(np.linalg.norm(bath_real-bath_ideal))
assert abs(Dflag-.5)<1e-12 and coarse_residual<1e-12
# Last untrusted output X after a flawless upstream EPR check flips |0>.
zero_out=np.outer(e0,e0)
bad_out=X@zero_out@X
lastgate_d=.5*np.sum(abs(np.linalg.eigvalsh(zero_out-bad_out)))
assert abs(lastgate_d-1)<1e-12
res={'source':'coherent superposition of two Bell sectors entangled with a retained bath qubit',
     'Bell_target_probability':.5,
     'ZZ_parity_test_failure_probability':0,
     'fine_Z_outcomes':out,
     'full_flagged_bath_difference_half_trace':float(Dflag),
     'coarsened_parity_only_bath_update_difference_Frobenius':coarse_residual,
     'unaudited_terminal_X_causes_orthogonal_logical_output_D':float(lastgate_d),
     'limitations':'Fine local test outcomes must be retired for the full-memory Bell-path identity. Upstream EPR tests do not certify unaudited terminal gates.'}
Path(__file__).with_name('fine_record_and_last_gate_no_go_results.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
