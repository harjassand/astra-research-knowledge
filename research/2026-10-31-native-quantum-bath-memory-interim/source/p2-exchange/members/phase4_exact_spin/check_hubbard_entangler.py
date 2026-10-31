"""Finite-charge test of the eight-spin entangler in the SAME Hubbard regime.

Keeps all4900 half-filled N_up=N_down=4 charge states. No intermediate charge
projection. A numerical point, not a full-device or diamond-error certificate.
"""
import sys
from pathlib import Path
from itertools import combinations
from math import pi,sqrt
import json,time
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import expm_multiply
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from phase4_hubbard.check_finite_hubbard import fock_basis,hopping_matrix,ramp

def code():
    s=np.array([0,1,-1,0])/sqrt(2)
    p=np.array([1,0,0,0]);z=np.array([0,1,1,0])/sqrt(2);m=np.array([0,0,0,1])
    b=np.column_stack([np.kron(s,s),(np.kron(p,m)+np.kron(m,p)-np.kron(z,z))/sqrt(3)])
    return np.kron(b,b)

def main():
    start=time.time()
    basis=fock_basis(8,4,4);lookup={w:k for k,w in enumerate(basis)}
    doubles=np.array([sum(((a>>(2*i))&3)==3 for i in range(8)) for a in basis])
    onsite=diags(doubles,dtype=complex).tocsr()
    intra=list(combinations(range(4),2))+list(combinations(range(4,8),2))
    cross=[(i,j) for i in [0,1] for j in [4,5]]
    h_intra=hopping_matrix(basis,intra);h_cross=hopping_matrix(basis,cross)
    bc=code();load=np.zeros((len(basis),4),complex)
    for n in range(256):
        if n.bit_count()!=4:continue
        word=sum(1<<(2*i+((n>>(7-i))&1)) for i in range(8))
        load[lookup[word]]=bc[n]
    ratio=50.;t=.5/sqrt(ratio);ramp_time=40.;J=(sqrt(1+16*t*t)-1)/2
    gtime=2*pi/sqrt(7);phi=2*pi*(1-2/sqrt(7))
    grid=np.linspace(0,1,4001);shape=np.sin(pi*grid/2)**2
    gap=(np.sqrt(1+16*(t*shape)**2)-1)/2
    ramp_angle=2*ramp_time*np.trapezoid(gap,grid)
    plateau=(gtime-ramp_angle)/J
    assert plateau>0
    hopping=t*(h_intra+h_cross)
    results={'hilbert_dimension':len(basis),'U_over_J_nominal':ratio,'t_over_U':t,
             'pair_calibrated_J':J,'ramp_time_U_units':ramp_time,
             'plateau_time_U_units':float(plateau),'full_gate_time_U_units':float(plateau+2*ramp_time),
             'target_controlled_phase':phi,'cases':[]}
    previous=None
    for steps in [40,80]:
        state=ramp(load.copy(),onsite,hopping,ramp_time,steps,False)
        state=expm_multiply(-1j*plateau*(onsite+hopping),state)
        state=ramp(state,onsite,hopping,ramp_time,steps,True)
        K=load.conj().T@state
        code_effect=K.conj().T@K
        sing=state[doubles==0]
        charge_effect=np.eye(4)-sing.conj().T@sing
        target=np.diag([1,1,1,np.exp(1j*phi)])
        alpha=np.trace(target.conj().T@K)/4
        phases=np.angle(np.diag(K))
        conditional=np.angle(K[3,3]*K[0,0]/(K[1,1]*K[2,2]))
        row={'ramp_steps':steps,
             'norm_preservation_error':float(np.linalg.norm(state.conj().T@state-np.eye(4),2)),
             'worst_code_rejection_probability':float(np.linalg.eigvalsh(np.eye(4)-code_effect)[-1]),
             'worst_charge_probability':float(np.linalg.eigvalsh(charge_effect)[-1]),
             'accepted_target_operator_error':float(np.linalg.norm(K-alpha*target,2)),
             'code_offdiagonal_norm':float(np.linalg.norm(K-np.diag(np.diag(K)),2)),
             'actual_conditional_phase':float(conditional),
             'conditional_phase_error':float(conditional-phi),
             'accepted_amplitudes_real':np.diag(K).real.tolist(),
             'accepted_amplitudes_imag':np.diag(K).imag.tolist()}
        if previous is not None:row['refinement_operator_difference']=float(np.linalg.norm(K-previous,2))
        results['cases'].append(row);previous=K
    results['wall_time_seconds']=time.time()-start
    out=Path(__file__).with_name('hubbard_entangler_results.json')
    out.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__':main()
