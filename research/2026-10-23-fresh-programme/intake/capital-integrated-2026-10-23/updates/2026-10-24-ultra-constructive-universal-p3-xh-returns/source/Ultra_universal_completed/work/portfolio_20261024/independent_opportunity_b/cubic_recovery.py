#!/usr/bin/env python3
"""Finite exact-structure checks of the cubic-kernel recovery construction.

No hardware acquisition or noisy-processor performance is represented. The
native kernel and local dephasing parameters are explicit model inputs. All
state/input branches are checked through channel Kraus/Choi matrices.
"""
import itertools
import json
import math
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent


def bits(mask,n):
    return np.array([(mask>>i)&1 for i in range(n)],dtype=np.uint8)


def mask(vector):
    return sum(int(v)<<i for i,v in enumerate(vector))


def gf2_inverse(matrix):
    n = len(matrix)
    a = np.c_[matrix.copy(),np.eye(n,dtype=np.uint8)]
    for j in range(n):
        pivot = next(i for i in range(j,n) if a[i,j])
        a[[j,pivot]] = a[[pivot,j]]
        for i in range(n):
            if i != j and a[i,j]:
                a[i] ^= a[j]
    assert np.array_equal(a[:,:n],np.eye(n,dtype=np.uint8))
    return a[:,n:]


def cnot_circuit(matrix):
    n = len(matrix)
    a = matrix.copy()
    reducing = []
    def add(target,control):
        a[target] ^= a[control]
        reducing.append((target,control))
    for j in range(n):
        pivot = next(i for i in range(j,n) if a[i,j])
        if pivot != j:
            add(j,pivot); add(pivot,j); add(j,pivot)
        for i in range(n):
            if i != j and a[i,j]:
                add(i,j)
    assert np.array_equal(a,np.eye(n,dtype=np.uint8))
    circuit = list(reversed(reducing))
    for x in range(1<<n):
        y = bits(x,n)
        for target,control in circuit:
            y[target] ^= y[control]
        assert np.array_equal(y,(matrix@bits(x,n))%2)
    return circuit


def symplectic_basis(alternating):
    n = len(alternating)
    remaining = [v for v in np.eye(n,dtype=np.uint8)]
    paired = []
    form = lambda u,v:int(u@alternating@v)%2
    while True:
        pair = next(((i,j) for i in range(len(remaining))
                     for j in range(i+1,len(remaining)) if form(remaining[i],remaining[j])),None)
        if pair is None:
            break
        i,j = pair
        u,v = remaining[i],remaining[j]
        paired.extend([u,v])
        rest = [w for k,w in enumerate(remaining) if k not in pair]
        remaining = [(w+form(w,v)*u+form(w,u)*v)%2 for w in rest]
    s = np.array(paired+remaining,dtype=np.uint8).T
    canonical = (s.T@alternating@s)%2
    expected = np.zeros_like(alternating)
    for j in range(0,len(paired),2):
        expected[j,j+1] = expected[j+1,j] = 1
    assert np.array_equal(canonical,expected)
    return s,len(paired)//2


def main(n=5,seed=902411):
    rng = np.random.default_rng(seed)
    triples = [t for t in itertools.combinations(range(n),3) if rng.integers(2)]
    if not triples:
        raise RuntimeError('Choose nontrivial fixture')
    dim = 1<<n
    def f(x):
        return sum(all((x>>i)&1 for i in t) for t in triples)%2
    phases = np.array([(-1)**f(x) for x in range(dim)])
    u = np.diag(phases).astype(complex)
    r = math.ceil(math.log2(n+1))
    check_masks = [sum(1<<i for i in range(n) if ((i+1)>>j)&1) for j in range(r)]
    def xpauli(a):
        return np.eye(dim,dtype=complex)[np.arange(dim)^a]
    def zpauli(e):
        return np.diag([(-1)**((x&e).bit_count()%2) for x in range(dim)]).astype(complex)
    qs = [xpauli(h) for h in check_masks]
    ps = [u.conj().T@q@u for q in qs]
    synthesis = []
    maximum_polynomial_residual = 0
    for h in check_masks:
        qvalue = lambda x:f(x)^f(x^h)
        constant = qvalue(0)
        alternating = np.zeros((n,n),dtype=np.uint8)
        for i,j in itertools.combinations(range(n),2):
            value = qvalue((1<<i)|(1<<j))^qvalue(1<<i)^qvalue(1<<j)^constant
            alternating[i,j] = alternating[j,i] = value
        s,pairs = symplectic_basis(alternating)
        transform = gf2_inverse(s)
        circuit = cnot_circuit(transform)
        linear = np.array([qvalue(mask(s[:,i]))^constant for i in range(n)],dtype=np.uint8)
        for x in range(dim):
            y = (transform@bits(x,n))%2
            reconstructed = (constant+int(linear@y)+sum(int(y[2*j]*y[2*j+1]) for j in range(pairs)))%2
            maximum_polynomial_residual = max(maximum_polynomial_residual,abs(qvalue(x)-reconstructed))
        assert maximum_polynomial_residual == 0
        synthesis.append({'check_mask':h,'quadratic_polar_rank':2*pairs,
                          'trusted_CCZ_gates':pairs,
                          'basis_CNOTs_each_direction':len(circuit),
                          'controlled_linear_CZ_gates':int(linear.sum()),
                          'controlled_X_pre_and_post_CNOTs':2*h.bit_count(),
                          'constant_Z_on_control':constant})
    # Independent matrix sandwich: form each routing branch using the actual
    # pre/post matrices, Walsh-transform the ancillas, correct and form Choi.
    routes = 1<<r
    pre,post = [],[]
    for a in range(routes):
        pin,pout = np.eye(dim,dtype=complex),np.eye(dim,dtype=complex)
        for j in range(r):
            if (a>>j)&1:
                pin = ps[j]@pin
                pout = qs[j]@pout
        pre.append(pin)
        post.append(pout.conj().T)
    p = .02
    integrated_dephasing = -math.log(1-2*p)/2
    native_generator_residual = 0.0
    integer_f = [sum(all((x>>i)&1 for i in t) for t in triples) for x in range(dim)]
    for x in range(dim):
        for y in range(dim):
            # Exact diagonal Lindblad generator, integrated over the ENTIRE
            # native interval, independently of the endpoint recovery algebra.
            actual_multiplier = np.exp(-1j*math.pi*(integer_f[x]-integer_f[y])
                                       -2*integrated_dephasing*((x^y).bit_count()))
            product_channel = phases[x]*phases[y]*(1-2*p)**((x^y).bit_count())
            native_generator_residual = max(native_generator_residual,abs(actual_multiplier-product_channel))
    all_triples = list(itertools.combinations(range(n),3))
    character_overlaps = []
    for coefficient_mask in range(1,1<<len(all_triples)):
        values = [sum(all((x>>i)&1 for i in triple) for j,triple in enumerate(all_triples)
                      if (coefficient_mask>>j)&1)%2 for x in range(dim)]
        character_overlaps.append(abs(1-2*sum(values)/dim))
    assert max(character_overlaps) <= .75
    assert native_generator_residual < 1e-12
    choi = np.zeros((dim,dim),complex)
    max_single_error_residual = 0.0
    max_syndrome_leak = 0.0
    max_offdiagonal = 0.0
    for e in range(dim):
        weight = e.bit_count()
        probability = p**weight*(1-p)**(n-weight)
        z = zpauli(e)
        route_kraus = [post[a]@z@u@pre[a] for a in range(routes)]
        expected_syndrome = 0
        for i in range(n):
            if (e>>i)&1:
                expected_syndrome ^= i+1
        for syndrome in range(routes):
            k = sum(((-1)**((a&syndrome).bit_count()%2))*route_kraus[a]
                    for a in range(routes))/routes
            if syndrome != expected_syndrome:
                max_syndrome_leak = max(max_syndrome_leak,float(np.max(abs(k))))
            correction = zpauli(1<<(syndrome-1)) if 1 <= syndrome <= n else np.eye(dim)
            k = correction@k
            if weight <= 1 and syndrome == expected_syndrome:
                max_single_error_residual = max(max_single_error_residual,float(np.max(abs(k-u))))
            diagonal = np.diag(k)
            max_offdiagonal = max(max_offdiagonal,float(np.max(abs(k-np.diag(diagonal)))))
            v = diagonal/math.sqrt(dim)
            choi += probability*np.outer(v,v.conj())
    ideal = phases/math.sqrt(dim)
    ideal_choi = np.outer(ideal,ideal)
    choi_distance = float(np.abs(np.linalg.eigvalsh(choi-ideal_choi)).sum()/2)
    tail = 1-(1-p)**n-n*p*(1-p)**(n-1)
    bare = 1-(1-p)**n
    assert max_single_error_residual < 1e-12 and max_syndrome_leak < 1e-12
    assert max_offdiagonal < 1e-12 and abs(np.trace(choi).real-1) < 1e-12
    assert abs(choi_distance-tail) < 1e-12
    cnot = sum(2*s['basis_CNOTs_each_direction']+s['controlled_X_pre_and_post_CNOTs'] for s in synthesis)
    ccz = sum(s['trusted_CCZ_gates'] for s in synthesis)
    cz = sum(s['controlled_linear_CZ_gates'] for s in synthesis)
    # Conservative primitive count includes every check gate, 2r Hadamards,
    # r preparations + r measurements + r resets, and one feedforward Z.
    clean_gates = cnot+ccz+cz+sum(s['constant_Z_on_control'] for s in synthesis)+5*r+1
    epsilon_clean = 1e-5
    full_bound = tail+clean_gates*epsilon_clean
    incidences = [sum(i in t for t in triples) for i in range(n)]
    output = {'status':'MODEL_DERIVED_CLOSED_CPTP_RECOVERY_CHECK',
              'n':n,'seed':seed,'cubic_monomials':triples,'syndrome_qubits':r,
              'check_masks':check_masks,'quadratic_synthesis':synthesis,
              'maximum_quadratic_reconstruction_residual':maximum_polynomial_residual,
              'maximum_correctable_error_matrix_residual':max_single_error_residual,
              'maximum_wrong_syndrome_amplitude':max_syndrome_leak,
              'maximum_corrected_Kraus_offdiagonal':max_offdiagonal,
              'native_Z_flip_probability_per_qubit':p,
              'equivalent_native_integrated_dephasing':integrated_dephasing,
              'maximum_native_Lindblad_vs_output_channel_residual':native_generator_residual,
              'exhaustive_cubic_difference_polynomials':len(character_overlaps),
              'maximum_distinct_target_Choi_overlap':max(character_overlaps),
              'uncorrected_normalized_diamond_error':bare,
              'corrected_normalized_diamond_error_exact':tail,
              'computed_corrected_Choi_trace_distance':choi_distance,
              'union_pair_tail_bound':math.comb(n,2)*p*p,
              'trusted_primitive_counts':{'CNOT':cnot,'CCZ':ccz,'CZ':cz,
                 'total_including_H_prep_measure_reset_feedforward':clean_gates},
              'per_trusted_primitive_diamond_error_premise':epsilon_clean,
              'full_hybrid_diamond_error_upper_bound':full_bound,
              'constant_accuracy_counting_regime_satisfied':full_bound < 1/16,
              'native_hardware':{'nonzero_three_body_projector_terms':len(triples),
                   'site_incidences':incidences,'maximum_site_incidence':max(incidences),
                   'minimum_Jloc_times_tau':math.pi*max(incidences),
                   'interaction_action_over_hbar':math.pi*len(triples),
                   'gamma_over_Jloc_at_fastest_native_time':integrated_dephasing/(math.pi*max(incidences))},
              'scope':['Synthetic small-channel diagnostic, not hardware or scaling validation.',
                       'Per-gate quality and native Hamiltonian are stated resources, not acquired.',
                       'CPC/quantum-filter incumbents can implement the same recovery.',
                       'No general non-Clifford fault model or total-runtime advantage is established.']}
    (ROOT/'CUBIC_RECOVERY_RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__ == '__main__':
    main()
