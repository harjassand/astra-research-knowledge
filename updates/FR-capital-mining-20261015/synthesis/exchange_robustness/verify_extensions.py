#!/usr/bin/env python3
"""Finite synthetic checks, not physical validation or a priority assessment.

Run with Python 3.10+ and NumPy. Writes only beside this script. Imports the
incoming verifier without executing its source-writing __main__ block.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
INCOMING = Path('/Users/harjas/Downloads/astra_conditional_exchange/verify.py')
spec = importlib.util.spec_from_file_location('incoming_exchange_verify', INCOMING)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
RNG = np.random.default_rng(202610151)
TOL = 4e-12
I = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex)
Z = np.diag([1.,-1.])
H = np.array([[1,1],[1,-1]], dtype=complex)/np.sqrt(2)


def random_state(d):
    a = RNG.normal(size=(d,d)) + 1j*RNG.normal(size=(d,d))
    r = a @ a.conj().T
    return r / np.trace(r)


def map_measure_prepare(sigma, sign):
    """Input R,S -> R,S: random Pauli measure; same/opposite preparation."""
    out = np.zeros_like(sigma)
    for pauli in [X,Y,Z]:
        for x in [-1,1]:
            effect = (I+x*pauli)/2
            prep = (I+sign*x*pauli)/2
            unnormalized_R = v.marginal(v.tensor(I,effect) @ sigma,(2,2),(0,))
            out += v.tensor(unnormalized_R,prep)/3
    return out


def main():
    source = v.run()
    (HERE/'incoming_replay_results.json').write_text(json.dumps(source,indent=2)+'\n')
    results = {'scope':'Synthetic finite checks and exact rational examples only',
               'seed':202610151, 'source_replay_passed':source['all_assertions_passed']}

    # Coarse labels z match while donor fine record u and reference are retained.
    # Local S unitaries change RS but leave E marginal fixed within z.
    base = [random_state(8),random_state(8)]
    states = []
    for z in range(2):
        for u in range(2):
            gate = v.tensor(I,H if u else I,I)
            states.append(gate @ base[z] @ gate.conj().T)
    dims = (2,)*6
    swap_s = v.swap_matrix(dims,1,4)
    coarse_error = 0.
    donor_preservation_error = 0.
    for c,d in [(0,1),(1,0),(2,3),(3,2)]:
        pair = v.tensor(states[c],states[d])
        # Site 1 donor c receives d at site 2: retain R1,S2,E2.
        graft = v.marginal(v.apply_permutation(pair,swap_s),dims,(0,4,5))
        target = v.tensor(v.marginal(states[c],(2,2,2),(0,1)),
                          v.marginal(states[d],(2,2,2),(2,)))
        ideal_fine = v.tensor(v.marginal(states[c],(2,2,2),(0,1)),
                             v.marginal(states[c],(2,2,2),(2,)))
        coarse_error = max(coarse_error,v.td(graft,target),v.td(graft,ideal_fine))
        donor_preservation_error = max(donor_preservation_error,
            v.td(v.marginal(graft,(2,2,2),(0,1)),v.marginal(states[c],(2,2,2),(0,1))))
    assert coarse_error < TOL and donor_preservation_error < TOL
    # Directly enumerate random-record batches; no large tensor state needed.
    p = [Q(9,20),Q(9,20),Q(1,20),Q(1,20)]
    q = [Q(9,10),Q(1,10)]
    original_scores = [Q(1),Q(4,5),Q(3,5),Q(2,5)]
    graft_scores = [Q(1,5),Q(2,5),Q(7,10),Q(9,10)]
    enum_error = Q(0)
    for n in range(2,7):
        enum = Q(0)
        for labels in product(range(4),repeat=n):
            prob = Q(1)
            for c in labels: prob *= p[c]
            score = sum(original_scores[c] if sum(d//2==c//2 for d in labels)==1
                        else graft_scores[c] for c in labels)/n
            enum += prob*score
        formula = sum(pc*((1-q[c//2])**(n-1)*original_scores[c]
                        +(1-(1-q[c//2])**(n-1))*graft_scores[c])
                      for c,pc in enumerate(p))
        enum_error = max(enum_error,abs(enum-formula))
    assert enum_error == 0
    M = 2**128
    fine_s = (1-Q(1,2*M))**31
    coarse_s = Q(1,2)**31
    results['coarse_matching'] = {
        'density_matrix_trace_distance':coarse_error,
        'donor_RS_preservation_error':donor_preservation_error,
        'exact_batch_enumeration_error':str(enum_error),
        'nonce_example':{'fine_labels':str(2*M),'batch_size':32,
            'fine_unmatched_mass_exact':str(fine_s),
            'fine_unmatched_mass_lower_bound':'1 - 31 / 2^129',
            'coarse_unmatched_mass':float(coarse_s)}}

    # Global iid is unnecessary: three even-parity hidden bits, every pair iid.
    parity_pair = np.zeros((64,64),dtype=complex)
    bit_pair_distribution = {}
    for bits in product([0,1],repeat=3):
        if sum(bits)%2: continue
        key = (bits[0],bits[1])
        bit_pair_distribution[key] = bit_pair_distribution.get(key,Q(0))+Q(1,4)
    assert all(x==Q(1,4) for x in bit_pair_distribution.values())
    for (x,y),p_xy in bit_pair_distribution.items():
        parity_pair += float(p_xy)*v.tensor(v.memory_state(x),v.memory_state(y))
    parity_graft = v.marginal(v.apply_permutation(parity_pair,swap_s),dims,(3,1,2))
    parity_target = v.tensor(v.marginal(v.memory_state(.5),(2,2,2),(0,1)),I/2)
    parity_error = v.td(parity_graft,parity_target)
    assert parity_error<TOL
    results['partial_independence'] = {'source':'Three fair hidden bits conditioned on even parity',
        'fully_independent':False,'pairwise_independent':True,
        'graft_trace_distance':parity_error,'echo':v.bell_success(parity_graft,True)}

    # Stronger hidden operation: exchange both data and baths. Bath joint state
    # is invariant, and all independent reset-probe calibrations are identical.
    swap_e = v.swap_matrix(dims,2,5)
    bad = swap_e @ swap_s
    rho = v.memory_state(.2)
    pair = v.tensor(rho,rho)
    good_pair = v.apply_permutation(pair,swap_s)
    bad_pair = v.apply_permutation(pair,bad)
    good_local = v.marginal(good_pair,dims,(3,1,2))
    bad_local = v.marginal(bad_pair,dims,(3,1,2))
    bath_error = v.td(v.marginal(good_pair,dims,(2,5)),v.marginal(bad_pair,dims,(2,5)))
    accessible_error = v.td(v.marginal(good_pair,dims,(0,1,3,4)),
                           v.marginal(bad_pair,dims,(0,1,3,4)))
    probe_error = 0.
    tau = v.marginal(rho,(2,2,2),(2,))
    # Order input accessible A=(R1,S1,R2,S2), baths=(E1,E2), then reorder.
    for _ in range(24):
        product_input = v.tensor(random_state(16),tau,tau)
        # Existing order R1,S1,R2,S2,E1,E2 -> R1,S1,E1,R2,S2,E2.
        order = (0,1,4,2,3,5)
        product_input = product_input.reshape((2,)*12).transpose(order+tuple(i+6 for i in order)).reshape(64,64)
        probe_error = max(probe_error,v.td(v.apply_permutation(product_input,swap_s),
                                           v.apply_permutation(product_input,bad)))
    assert bath_error<TOL and accessible_error<TOL and probe_error<TOL
    assert abs(v.bell_success(good_local,True)-.68)<TOL
    assert abs(v.bell_success(bad_local,True)-1)<TOL
    results['hidden_bath_swap_counterexample'] = {
        'native_phase_probability':.2,'ideal_tagged_echo':v.bell_success(good_local,True),
        'bad_tagged_echo':v.bell_success(bad_local,True),
        'entire_bath_joint_marginal_trace_distance':bath_error,
        'accessible_gate_trace_distance':accessible_error,
        'reset_probe_complete_joint_state_error':probe_error,
        'round_trip_error':float(np.linalg.norm(bad@bad-np.eye(64))),
        'interpretation':'Bath-state and reset-probe audits do not bound action on original correlations.'}

    # Root-supplied reference-pairing falsifier, independently computed here.
    # Each input has S=0 and R,E maximally entangled.
    re = v.tensor(v.BELL,v.P0)
    order = (0,2,1)
    re = re.reshape((2,)*6).transpose(order+tuple(i+3 for i in order)).reshape(8,8)
    blank_pair = v.tensor(re,re)
    blank_after = v.apply_permutation(blank_pair,swap_s)
    global_error = v.td(blank_pair,blank_after)
    future = v.swap_matrix(dims,1,2) @ v.swap_matrix(dims,4,5)
    final = v.apply_permutation(blank_after,future)
    resident = v.marginal(final,dims,(0,1))
    donor = v.marginal(final,dims,(3,1))
    resident_score = float(np.trace(v.BELL@resident).real)
    donor_score = float(np.trace(v.BELL@donor).real)
    assert global_error<TOL and abs(resident_score-1)<TOL and abs(donor_score-.25)<TOL
    results['reference_pairing_counterexample'] = {
        'provenance':'Invented by quantum_information_operation worker, relayed by root; independently computed here',
        'global_state_change':global_error,'resident_reference_score':resident_score,
        'donor_reference_score':donor_score,
        'interpretation':'Tagged job/reference assignment can change the score without physical state change.'}

    # Known optimal identity-channel cutting, specialized to the graft score.
    virtual_error = 0.
    positivity_error = 0.
    for _ in range(32):
        rs = random_state(4)
        dp = map_measure_prepare(rs,+1)
        dm = map_measure_prepare(rs,-1)
        virtual_error = max(virtual_error,v.td(2*dp-dm,rs))
        positivity_error = max(positivity_error,max(0.,-float(np.linalg.eigvalsh(dp).min())),
                               max(0.,-float(np.linalg.eigvalsh(dm).min())))
    assert virtual_error<TOL and positivity_error<TOL
    # End-to-end Bell-phase estimate is weighted2 D+ minus D- at fixed tau.
    rs = v.marginal(rho,(2,2,2),(0,1))
    fp = v.bell_success(v.tensor(map_measure_prepare(rs,+1),tau),True)
    fm = v.bell_success(v.tensor(map_measure_prepare(rs,-1),tau),True)
    virtual_score = 2*fp-fm
    assert abs(virtual_score-.68)<TOL
    results['virtual_graft_estimator'] = {
        'known_method':'Optimal wire cutting with classical communication',
        'identity_reconstruction_maximum_trace_distance':virtual_error,
        'measure_prepare_positivity_error':positivity_error,
        'phase_model_echo':virtual_score,
        'coefficient_l1_norm':3,'centered_Hoeffding_sample_multiplier':9,
        'm_qubit_collective_overhead':'(2^(m+1)-1)^2',
        'restriction':'Estimates tagged score; produces no entanglement-preserving routed state.'}
    results['all_assertions_passed'] = True
    (HERE/'extension_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))


if __name__=='__main__':
    main()
