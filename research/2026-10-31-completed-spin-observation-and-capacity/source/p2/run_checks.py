"""Reproduce the finite-model checks and the conservative resource table.

Analytic inequalities are proved in DERIVATION.md. Except for the
Fraction teleportation certificate, matrix checks use ordinary floating
point and are NOT certified interval calculations.
"""
import json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from spin_interface import (I2,X,Y,Z,PS,PT,singlet,norm,hubbard,hermitian,
    positive,physical_pulse,finite_instrument,source_window_bounds,
    detector_qualification,two_setting_detector,charge_detuned_bound,schedule,st_bound,
    teleport_tail,source_tail)
from exact_teleportation import certify
from exact_bounds import certify as certify_bounds

RNG=np.random.default_rng(276019)


def fock_checks():
    m=hubbard(); v=m['scharge']; hp=v.conj().T@m['hop']@v
    expected=-math.sqrt(2)*np.array([[0,1,1],[1,0,0],[1,0,0]],complex)
    comm=max(norm(m['hop']@j-j@m['hop']) for j in m['generators'])
    assert norm(hp-expected)<1e-14 and comm<1e-14
    assert norm(m['hop']@m['triplets'])<1e-14
    # D_minus is a dark state at charge resonance. A claim of uniform
    # return from an arbitrary unresolved two-dimensional double sector
    # is therefore false.
    dark=(m['dl']-m['dr'])/math.sqrt(2)
    assert norm((m['hop']@dark).reshape(-1,1))<1e-14
    return {'hopping_spin_commutator':comm,'singlet_charge_matrix_residual':norm(hp-expected),
            'triplet_hopping_norm':norm(m['hop']@m['triplets']),
            'unresolved_double_dark_state_hopping_norm':float(np.linalg.norm(m['hop']@dark))}


def source_checks():
    model=hubbard(); d=3; enc=np.kron(model['scharge'],np.eye(d))
    rmax=0.; pmin=1.; tripmax=0.; samples=0
    bounds=source_window_bounds()
    for hscale in [0.,1.,30.,1000.]:
        for trial in range(12):
            tau=RNG.uniform(bounds['tau_low'],bounds['tau_high'])
            u=np.eye(6*d,dtype=complex)
            for piece in range(7):
                step=physical_pulse(hscale*hermitian(RNG,d),positive(RNG,d),
                                    .02*hermitian(RNG,d),.02*hermitian(RNG,d),tau/7)
                u=step['unitary']@u
                tripmax=max(tripmax,step['triplet_factor_residual'])
            uc=enc.conj().T@u@enc
            rmax=max(rmax,norm(uc[:d,:d]))
            for site in [1,2]:
                block=uc[:d,site*d:(site+1)*d]
                pmin=min(pmin,float(np.linalg.eigvalsh(block.conj().T@block)[0]))
            samples+=1
    assert rmax<=bounds['r_search']+1e-10
    assert pmin>=bounds['return_probability']-1e-10
    # Separately exercise the nonresonant guarantee without projecting
    # out either doubly occupied site.
    detuned=[]
    for dcharge in [0.,1.,10.,100.]:
        bound=charge_detuned_bound(1.,2.,dcharge)
        smallest=1.
        for trial in range(8):
            step=physical_pulse(100*hermitian(RNG,3),positive(RNG,3),
                                dcharge*hermitian(RNG,3),dcharge*hermitian(RNG,3),bound['tau'])
            for a,b in [(0,1),(1,0),(0,2),(2,0)]:
                block=step['blocks'][a][b]
                smallest=min(smallest,float(np.linalg.eigvalsh(block.conj().T@block)[0]))
        assert smallest+1e-10>=bound['return_probability_lower']
        detuned.append({'charge_bound':dcharge,**bound,'sampled_probability_minimum':smallest})
    return {'windows':samples,'pieces_per_window':7,'bath_norms':[0,1,30,1000],
            'maximum_sampled_search_stay_norm':rmax,'minimum_sampled_return_probability':pmin,
            'maximum_triplet_factor_residual':tripmax,'analytic_bounds':bounds,
            'off_resonant_bounds':detuned}


def finite_checks():
    out=[]
    for trial in range(8):
        def pulse():
            return physical_pulse(100*hermitian(RNG,2),positive(RNG,2),
                 .02*hermitian(RNG,2),.02*hermitian(RNG,2),
                 RNG.uniform(.95,1.05)*math.pi/6,read_time=13.)
        n=4; r=4
        ins=finite_instrument([pulse() for _ in range(n)],[pulse() for _ in range(r)])
        bound=st_bound(n,r)['intrinsic']
        assert ins['completeness_defect']<1e-9
        assert ins['half_diamond_upper']<=bound+1e-9
        assert ins['t_branch_amplitude_error']<=.6**n+1e-10
        assert ins['abort_probability_max']<=.7**r+1e-10
        out.append({key:ins[key] for key in ['completeness_defect','t_branch_amplitude_error',
                    's_branch_isometry_error','abort_probability_max','half_diamond_upper']})
    return {'search_windows':4,'release_windows':4,'uniform_bound':bound,'samples':out}


def detector_checks():
    q=two_setting_detector(); samples=[]
    for setting in ['short','long']:
        tlo=q['short']['tau_low'] if setting=='short' else q['long_tau_low']
        thi=q['short']['tau_high'] if setting=='short' else q['long_tau_high']
        intervals=q['short']['physical_intervals'] if setting=='short' else q['long_physical_intervals']
        for n in [0,1,2]:
            lowest=1.; highest=0.
            for trial in range(40):
                d=3; up=np.eye(d,dtype=complex); um=up.copy()
                tau=RNG.uniform(tlo,thi)
                for piece in range(9):
                    h=1000*hermitian(RNG,d); f=positive(RNG,d,1.,1.2)
                    up=expm(-1j*(h+n*f)*tau/9)@up
                    um=expm(-1j*(h-n*f)*tau/9)@um
                b=(up-um)/2
                vals=np.linalg.eigvalsh(b.conj().T@b)
                lowest=min(lowest,float(vals[0])); highest=max(highest,float(vals[-1]))
            lo,hi=intervals[n]
            assert lowest>=lo-1e-10 and highest<=hi+1e-10
            samples.append({'setting':setting,'charge':n,'minimum_sampled_click_effect':lowest,
                            'maximum_sampled_click_effect':highest,'analytic_interval':[lo,hi]})
    return {'qualification':q,'samples':samples}


def source_and_failures():
    # B is maximally entangled with an old memory qubit M. C is fresh I/2.
    # Build register order B,C,M explicitly.
    rho=np.zeros((8,8),complex)
    for c in [0,1]:
        v=np.zeros(8,complex)
        for b in [0,1]: v[4*b+2*c+b]=1/math.sqrt(2)
        rho+=np.outer(v,v.conj())/2
    projector=np.kron(PS,I2)
    result=projector@rho@projector
    target=np.kron(PS,I2/2)/4
    assert norm(result-target)<1e-14
    # A correlated C with the same maximally mixed marginal can instead
    # have zero singlet probability.
    phi=np.array([1,0,0,1],complex)/math.sqrt(2)
    bad_source_probability=float(np.vdot(phi,PS@phi).real)
    assert abs(bad_source_probability)<1e-14
    # Correct t-bit, wrong instrument: resolving the three triplet basis
    # states destroys (|00>+|11>)/sqrt(2).
    wrong=np.diag([.5,0,0,.5]).astype(complex)
    original=np.outer(phi,phi.conj())
    disturbance=float(np.linalg.norm(original-wrong,ord='nuc')/2)
    assert abs(disturbance-.5)<1e-14
    # SU(2)-invariant exchange acts on the multiplicity degree of three
    # spins: |s_AB>|up_C> and the orthogonal J=1/2 state have opposite
    # swap_AB eigenvalues. Global rotational symmetry alone is no fix.
    swap=np.eye(4)-2*PS
    v0=np.kron(singlet,np.array([1,0]))
    v1=np.array([0,math.sqrt(2/3),-1/math.sqrt(6),0,
                 -1/math.sqrt(6),0,0,0],complex)
    sub=np.column_stack([v0,v1]); logical=sub.conj().T@np.kron(swap,I2)@sub
    assert norm(logical-np.diag([-1,1]))<1e-14
    return {'independent_mixed_source_identity_residual':norm(result-target),
            'correlated_mixed_marginal_singlet_probability':bad_source_probability,
            'perfect_triplet_bit_but_trace_distance_disturbance':disturbance,
            'three_spin_invariant_exchange_on_multiplicity':logical.real.tolist()}


def resource_checks():
    schedules=[schedule(e) for e in [1e-2,1e-4,1e-6,1e-8]]
    for row in schedules: assert row['st_error_bound']<=row['epsilon']
    ks=50; kt=31; lmax=ks+2*kt-1
    failure=source_tail(ks)+teleport_tail(kt) # union bound, slightly conservative
    per_call=1e-6/(4*lmax); spec=schedule(per_call)
    delta=lmax*spec['st_error_bound']
    conditional=2*delta/(1-failure-delta)
    return {'schedules':schedules,'capped_singlet_and_teleport_example':{
            'source_cap':ks,'AB_attempt_cap':kt,'maximum_ST_calls':lmax,
            'ideal_failure_union_bound':failure,'per_ST_requested_error':per_call,
            'per_ST_schedule':spec,'complete_instrument_error_bound':delta,
            'conditional_success_error_bound':conditional,
            'maximum_fresh_probe_slots':lmax*spec['total_fresh_probe_slots']}}


if __name__=='__main__':
    results={'status':'working derivation; ordinary floating-point checks except exact rational certificate',
       'fock_hamiltonian':fock_checks(),'source_windows':source_checks(),
       'full_finite_instrument':finite_checks(),'finite_charge_detector':detector_checks(),
       'exact_forced_teleportation':certify(),'source_and_failure_witnesses':source_and_failures(),
       'exact_reverse_teleportation':certify(reverse=True),
       'rational_qualification_certificate':certify_bounds(),
       'resources':resource_checks()}
    target=Path(__file__).with_name('results.json')
    target.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({'checks':'passed','output':str(target),
        'source':results['source_windows']['analytic_bounds'],
        'detector_effective_exponent':results['finite_charge_detector']['qualification']['effective_exponent'],
        'resources':results['resources']},indent=2))
