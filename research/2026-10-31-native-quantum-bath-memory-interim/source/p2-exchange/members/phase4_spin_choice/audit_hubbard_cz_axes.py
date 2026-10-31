"""One targeted audit: the compiler's abstract axes in its physical Fock basis.

The native cell and verifier are not re-optimized or re-run. Each reported
local pulse is propagated in the full 36-state, four-site Hubbard sector
to check the physical pair sign, return, schedule, and compiled CZ phase.
"""
from pathlib import Path
import json, sys
import numpy as np
from scipy.linalg import expm, norm
from itertools import combinations

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from phase4_hubbard.check_finite_hubbard import fock_basis,hopping_matrix


def phase_error(a,b):
    c=np.trace(b.conj().T@a)/len(a)
    return float(norm(a-c/abs(c)*b,2))


def main():
    record=json.loads((ROOT/'phase4_exact_spin/finite_hubbard_cz_compiler_results.json').read_text())
    cell=json.loads((ROOT/'phase4_exact_spin/joint_hubbard_cell_results.json').read_text())
    s=np.array([0,1,-1,0])/np.sqrt(2)
    p=np.array([1,0,0,0]);z=np.array([0,1,1,0])/np.sqrt(2);m=np.array([0,0,0,1])
    b=np.column_stack([np.kron(s,s),(np.kron(p,m)+np.kron(m,p)-np.kron(z,z))/np.sqrt(3)])
    basis=fock_basis(4,2,2);lookup={w:k for k,w in enumerate(basis)}
    load=np.zeros((len(basis),2),complex)
    for n in range(16):
        if n.bit_count()!=2:continue
        w=sum(1<<(2*i+((n>>(3-i))&1)) for i in range(4))
        load[lookup[w]]=b[n]
    doubles=np.array([sum(((w>>(2*i))&3)==3 for i in range(4)) for w in basis])
    h0=np.diag(doubles)
    hops={a:hopping_matrix(basis,[edge]).toarray() for a,edge in [('z',(0,1)),('n',(1,2))]}
    X=np.array([[0,1],[1,0]],complex);Z=np.diag([1.,-1.]);axisn=np.sqrt(3)/2*X+.5*Z
    all_locals={};rows=[]
    for local in record['local_controls']:
        state=load.copy();abstract=np.eye(2,dtype=complex)
        for pulse in local['pair_pulses']:
            h=h0+pulse['t_over_U']*hops[pulse['axis']]
            state=expm(-1j*pulse['duration_U_units']*h)@state
            abstract=expm(-.5j*pulse['angle']*(Z if pulse['axis']=='z' else axisn))@abstract
        k=load.conj().T@state
        leftover=float(norm(state-load@k,2))
        err=phase_error(k,abstract)
        assert leftover<2e-12 and err<2e-12
        all_locals[local['name']]=k
        rows.append(dict(name=local['name'],full_fock_charge_or_spin_return_amplitude=leftover,
                         physical_abstract_axis_error_up_to_phase=err))
    native=np.diag(np.exp(1j*np.array(cell['cases'][-1]['gate_phase_angles'])))
    cp=[np.kron(all_locals[f'A native phase correction {i}'],
                all_locals[f'B native phase correction {i}'])@native for i in range(1,4)]
    eye=np.eye(2)
    total=(np.kron(all_locals['A final phase'],eye)
           @np.kron(eye,all_locals['B after third cell'])
           @cp[2]@cp[1]
           @np.kron(eye,all_locals['B between first and second cell'])
           @cp[0]@np.kron(eye,all_locals['B before first cell']))
    target=np.diag([1,1,1,-1])
    err=phase_error(total,target)
    assert err<5e-12
    report=dict(full_local_hubbard_dimension=len(basis),local_pair_pulses=record['local_pair_pulse_count'],
                local_axes_checks=rows,compiled_CZ_error_up_to_global_phase=err,
                maximum_t_over_U=max(p['t_over_U'] for x in record['local_controls'] for p in x['pair_pulses']),
                scope='Independent exact finite-Hubbard local-axis and schedule audit; native target uses the already calibrated cell phases.')
    Path(__file__).with_name('hubbard_cz_axes_audit_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
