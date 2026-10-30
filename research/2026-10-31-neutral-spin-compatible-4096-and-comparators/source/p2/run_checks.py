"""Run finite-matrix witnesses and exact integer/algebraic checks.

These numerical checks do not certify a real device, an uncertainty box,
or a numerical fault-tolerance threshold. Analytic proofs are in
DERIVATION.md. Run: python p2_neutral_blocks/run_checks.py
"""
import json
import math
from pathlib import Path
import sys
import numpy as np
from scipy.linalg import expm
from native import (fock,code4,norm,kron,source_pulses,source_unitary,
                    capture_phase,pair_phase,hadamard_physical,
                    logical_hadamard_program,pair_phase_duration,
                    apply_cz,apply_local_two,cz_duration,phase_distance,
                    charge_patterns,apply_diagonal_charge_gate,
                    capacitive_energies,X,Y,Z)
from lru import check_lru
from calibration import check_calibration
from resources import (readout_amplitude,readout_probes,reset_time,
                       preparation_duration,PAIR_CONSTANT,
                       scalar_calibration_shots,optimize_local_readout,
                       cap_weak_during_capture_error)


def matrix_checks():
    m=fock(); c=code4(); p=c@c.conj().T; d=len(p); eye=np.eye(d)
    cap=source_unitary(); rev=source_unitary(reverse=True)
    chi=cap@c; phi=capture_phase()
    results={}
    results['fock_dimension_N4']=d
    s2=sum(s@s for s in m['total'])
    results['spin_zero_dimension_N4']=int(np.sum(np.abs(np.linalg.eigvalsh(s2))<1e-10))
    results['code_spin_annihilation']=max(norm(s@c) for s in m['total'])
    results['native_spin_commutator']=max(
        norm(q['H']@s-s@q['H']) for q in source_pulses()
        for s in m['total'])
    results['reciprocal_transpose_error']=norm(rev-cap.T)
    patterns=charge_patterns()
    results['capture_charge_pattern_error']=max(
        norm(m['n'][i]@chi-chi@np.diag(patterns[:,i])) for i in range(4))
    loop=rev@expm(-2j*phi*m['charging'])@cap
    results['corrected_loop_identity_error']=norm(loop@c-c)
    results['all_charge_operators_reduce_code']=max(
        norm((eye-p)@cap.conj().T@n@cap@p) for n in m['n'])
    phase_errors=[]
    for angle in [0.,math.pi/4,math.pi,3.7]:
        phase_errors.append(norm(pair_phase(angle)@c-c@np.diag([np.exp(-1j*angle),1.])))
    results['pair_phase_error']=max(phase_errors)
    h=np.array([[1,1],[1,-1]],complex)/np.sqrt(2)
    results['logical_hadamard_error']=phase_distance(hadamard_physical()@c,c@h)
    cc=np.kron(c,c)
    cz=np.diag([1.,1.,1.,-1.])
    results['cz_code_isometry_error']=norm(apply_cz(cc)-cc@cz)

    # Every projected one-spin vector vanishes. A raw cross-block exchange
    # has no first-order encoded action, but it DOES leave the local DFSs.
    results['projected_single_spin_norm']=max(
        norm(c.conj().T@s@c) for site in m['spin'] for s in site)
    cross=sum(apply_local_two(cc,m['spin'][0][a],m['spin'][0][a]) for a in range(3))
    results['cross_exchange_projected_norm']=norm(cc.conj().T@cross)
    results['cross_exchange_leakage_witness']=norm(cross-cc@(cc.conj().T@cross))
    gradient=m['spin'][0][2]-m['spin'][1][2]
    results['gradient_leakage_generator_norm']=norm((eye-p)@gradient@c)

    # Arbitrary leaked neighbor, including neutral orbital leakage, with
    # coherent columns representing an external reference.
    rng=np.random.default_rng(82173)
    raw=rng.normal(size=(d,5))+1j*rng.normal(size=(d,5))
    leak=np.linalg.qr((eye-p)@raw)[0]
    v=np.kron(c,leak)
    out=apply_cz(v)
    projected=apply_local_two(out,p,eye)
    results['cz_valid_block_with_leaked_neighbor']=norm(out-projected)
    V=rng.uniform(.01,.3,size=(4,4))
    t=1.37
    out=apply_diagonal_charge_gate(cc,V,t)
    target=cc@np.diag(np.exp(-1j*t*capacitive_energies(V)).reshape(-1))
    results['general_capacitance_matrix_code_error']=norm(out-target)
    out=apply_diagonal_charge_gate(v,V,t)
    results['general_capacitance_with_leaked_neighbor']=norm(out-apply_local_two(out,p,eye))

    # An interacting quantum memory, fast compared with the charge source.
    # Norm-free immunity is an analytic commutation fact; this finite test
    # exercises retained-reference columns for one noncommuting example.
    hm=7*X+3*Z
    bs=[11*X+2*Z,-5*Y+X,13*Z+4*Y]
    strong=kron(eye,hm)+sum(kron(s,b) for s,b in zip(m['total'],bs))
    w=kron(c,np.eye(2))
    total_time=0.
    for q in source_pulses():
        w=expm(-1j*q['time']*(kron(q['H'],np.eye(2))+strong))@w
        total_time+=q['time']
    expected=kron(cap@c,expm(-1j*hm*total_time))
    results['noncommuting_collective_bath_reference_error']=norm(w-expected)

    results['capture_duration_U1']=total_time
    results['cz_duration_U1_chi1']=cz_duration()
    results['H_duration_U1']=sum(pair_phase_duration(a) for _,a in logical_hadamard_program())
    results['CNOT_duration_U1_chi1']=2*results['H_duration_U1']+cz_duration()
    results['capture_windows']=5
    results['pair_phase_windows']=11
    results['CZ_windows_with_parallel_local_capture']=12
    return results


def infection_counterexample(n_targets=4,delta=.01):
    """One leaked block activates order-one errors on arbitrarily many others.

    All targets initially |0>; exp[-i(pi/2) sum X] flips every target.
    The large coupling vanishes on the all-valid input subspace.
    """
    d=2**n_targets
    ht=np.zeros((d,d),complex)
    for j in range(n_targets):
        ht+=kron(*[X if k==j else np.eye(2) for k in range(n_targets)])
    init=np.zeros(d,complex); init[0]=1
    leaked_branch=expm(-1j*math.pi*ht/2)@init
    return dict(targets=n_targets,one_leak_amplitude=delta,
                all_targets_flipped_amplitude=delta*abs(leaked_branch[-1]),
                hypothetical_independent_fault_amplitude=delta**n_targets)


def steane_check():
    """Exact binary syndrome/encoder check, not an exRec threshold proof.

    The outer FT gadgets are the verified-ancilla circuits of AGP and
    Aliferis--Terhal; we do not substitute this ideal decoder for them.
    """
    H=np.array([[1,0,0,0,1,1,1],
                [0,1,0,1,0,1,1],
                [0,0,1,1,1,0,1]],dtype=int)
    assert np.all((H@H.T)%2==0)
    columns=[tuple(H[:,j]) for j in range(7)]
    assert len(set(columns))==7 and (0,0,0) not in columns
    words=[]
    for x in range(8):
        coeff=np.array([(x>>i)&1 for i in range(3)])
        words.append(tuple((coeff@H)%2))
    assert len(set(words))==8
    # |0bar> = uniform superposition of this row span. H on sites 0,1,2,
    # then each pivot controls CNOTs to the 1s in its row at sites 3..6.
    encoder=[('H',j) for j in range(3)]
    encoder += [('CNOT',j,k) for j in range(3) for k in range(3,7) if H[j,k]]
    syndromes=[]
    for j in range(7):
        for pauli in ['X','Y','Z']:
            sx=columns[j] if pauli in ['Z','Y'] else (0,0,0)
            sz=columns[j] if pauli in ['X','Y'] else (0,0,0)
            syndromes.append((sx,sz))
    assert len(set(syndromes))==21
    return dict(stabilizer_binary_rows=H.tolist(),single_Pauli_error_syndromes=21,
                zero_encoder=encoder,
                caveat='Syndrome/encoder identity only; FT uses published verified ancillas and LRUs.')


def exact_detector_check():
    # Reuse, do not weaken or rewrite, the earlier exact Chernoff proof.
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'p2_spin_interface'))
    from exact_bounds import kl_interval
    from fractions import Fraction as F
    values=[]
    for p in [F(21,100),F(84,100)]:
        lower,upper=kl_interval(F(107,200),p)
        assert lower>F(1,4)
        values.append(dict(p=str(p),lower=float(lower),upper=float(upper)))
    return values


if __name__=='__main__':
    result=dict(matrix=matrix_checks(),lru=check_lru(),
                calibration=check_calibration(),
                failed_all_valid_only_model=infection_counterexample(),
                steane=steane_check(),detector_exponents=exact_detector_check(),
                resources=dict(pair_noise_constant=PAIR_CONSTANT,
                    finite_exposure_example=[dict(lambda_per_U=lam,
                        **optimize_local_readout(lam,1.,2*sum(
                            p['time'] for p in source_pulses())+2*math.pi))
                        for lam in [1e-4,1e-5,1e-6]],
                    always_on_cap_bound_chi_over_U_0001=
                        cap_weak_during_capture_error(.001),
                    detector=[dict(amplitude_target=e,probes=readout_probes(e),
                                   achieved_bound=readout_amplitude(readout_probes(e)),
                                   reset_Gamma_time=reset_time(e),
                                   prep_time_U1_Gamma1=preparation_duration(e))
                              for e in [1e-2,1e-3,1e-4,1e-6]],
                    illustrative_calibration=dict(parameter_tolerance=1e-3,
                        slope_lower=1.,model_bias=2e-4,confidence_failure=.01,
                        shots=scalar_calibration_shots(1e-3,1.,2e-4,.01))),
                status='Analytic working construction; floating-point matrix checks; exact rational Chernoff check; no device threshold claimed.')
    for k,v in result['matrix'].items():
        if any(s in k for s in ['error','annihilation','commutator','projected_norm','reduce_code','with_leaked_neighbor']):
            assert v<1e-9,(k,v)
    assert result['lru']['valid_reference_map_error']<1e-12
    assert result['lru']['arbitrary_input_output_leakage']<1e-12
    path=Path(__file__).resolve().parent/'results.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
