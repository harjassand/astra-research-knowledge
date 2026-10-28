#!/usr/bin/env python3
"""Finite-memory operational contracts, exact rational model construction.

No imported worker code. Bloch coordinates (trace,x,y,z) make all qubit
operations real rational, including the informationally complete Y control.
No physical shots are executed. Large-shot plans are integer costs only.
"""
from collections import deque
from fractions import Fraction as F
from math import ceil
from pathlib import Path
import hashlib
import json
import time

P_SIGNS = ((1,1,1,1), (1,1,-1,-1),
           (1,-1,1,-1), (1,-1,-1,1))
STATE_BASIS = ((1,0,0,0),(1,1,0,0),(1,0,1,0),(1,0,0,1))


def probabilities(c):
    s = 1/(2*c-1)
    p = [(1-s)/4]*4
    p[2] = (1+3*s)/4
    assert sum(p)==1 and min(p)>=0
    return s,p


def control(v, x, y):
    # M_xy(rho)=rho_x Tr(rho_y rho), a selected branch. Its physical
    # complement can be rho_0 Tr[(I-rho_y)rho].
    scalar = sum(F(a)*b for a,b in zip(STATE_BASIS[y],v))/2
    return tuple(F(a)*scalar for a in STATE_BASIS[x])


def pauli(v,j):
    return tuple(a*b for a,b in zip(P_SIGNS[j],v))


def phi(v,c):
    s,_=probabilities(c)
    return (v[0],-s*v[1],s*v[2],-s*v[3])


def noise_memory(v,c,hazard):
    """20-vector: fresh sector, then heldI,heldX,heldY,heldZ sectors."""
    _,weights=probabilities(c)
    fresh=v[:4]
    out=[F(0)]*20
    fresh_out=phi(fresh,c)
    out[:4]=[(1-hazard)*z for z in fresh_out]
    for j,w in enumerate(weights):
        old=v[4+4*j:8+4*j]
        inc=pauli(fresh,j)
        hold=pauli(old,j)
        out[4+4*j:8+4*j]=[hold[k]+hazard*w*inc[k] for k in range(4)]
    assert sum(out[4*j] for j in range(5))==sum(v[4*j] for j in range(5))
    return tuple(out)


def step_actual(v,symbol,c,hazard):
    x,y=divmod(symbol,4)
    pre=tuple(z for j in range(5) for z in control(v[4*j:4*j+4],x,y))
    return noise_memory(pre,c,hazard)


def step_reference(v,symbol,c):
    return phi(control(v,*divmod(symbol,4)),c)


INITIAL=(F(1),F(0),F(0),F(1))


def word_probability(word,c,hazard):
    v=INITIAL+(F(0),)*16
    w=INITIAL
    for symbol in word:
        v=step_actual(v,symbol,c,hazard)
        w=step_reference(w,symbol,c)
    return sum(v[4*j] for j in range(5)),w[0]


def add_basis(v,basis):
    r=list(v)
    for pivot,b in basis:
        k=r[pivot]
        if k:
            r=[x-k*y for x,y in zip(r,b)]
    try:
        pivot=next(i for i,x in enumerate(r) if x)
    except StopIteration:
        return False
    r=tuple(x/r[pivot] for x in r)
    # Insertion in pivot order is safe here: prior rows have zeros at every
    # earlier pivot; eliminate the new pivot from old rows for reduced form.
    updated=[]
    for q,b in basis:
        k=b[pivot]
        updated.append((q,tuple(x-k*y for x,y in zip(b,r))))
    updated.append((pivot,r))
    updated.sort(key=lambda x:x[0])
    basis[:]=updated
    return True


def reachable_equivalence(c,hazard):
    """Exact finite linear realization check when the matrices are supplied.

    This is the ordinary reachable-span method, NOT a black-box acquisition
    algorithm. At most1+16*24 candidate vectors for this concrete model.
    """
    start=INITIAL+(F(0),)*16+INITIAL
    queue=deque([(start,())])
    basis=[]
    words=[]
    visited=0
    witness=None
    while queue:
        v,word=queue.popleft()
        visited+=1
        if not add_basis(v,basis):
            continue
        words.append(word)
        difference=sum(v[4*j] for j in range(5))-v[20]
        if difference and witness is None:
            witness={"word":list(word),"length":len(word),"difference":str(difference)}
        for a in range(16):
            nxt=step_actual(v[:20],a,c,hazard)+step_reference(v[20:],a,c)
            queue.append((nxt,word+(a,)))
    assert len(basis)<=24 and visited<=1+16*24
    return {"linear_dimension_bound":24,"reachable_rank":len(basis),
            "candidate_vectors_processed":visited,
            "max_basis_word_length":max(map(len,words)),
            "equivalent":witness is None,"first_witness":witness}


def isolated_average_checks(c,hazard):
    _,weights=probabilities(c)
    # For an independently prepared input, the environment has either fresh
    # mass f or held labels distributed p_j. f=0,1 suffice by linearity.
    for f in (F(0),F(1)):
        for i in range(4):
            v=tuple(F(i==j) for j in range(4))
            joint=tuple(f*x for x in v)+tuple((1-f)*w*x for w in weights for x in v)
            after=noise_memory(joint,c,hazard)
            marginal=tuple(sum(after[4*j+k] for j in range(5)) for k in range(4))
            assert marginal==phi(v,c)
    return True


def confidence_power(alpha):
    assert 0<alpha<F(1,2)
    k=1
    while F(1,1<<k)>alpha:
        k+=1
    return k


def echo_contract(threshold,alpha,c):
    """Accept fresh qualification unless the lastm echo results are allzero.

    threshold is either delta/H for finite-program qualification, or a
    promised positive hazard floor for exact all-depth classification.
    """
    assert 0<threshold<=1
    k=confidence_power(alpha)
    tail_blocks=2*k
    calls_per_half_life=ceil(1/threshold)
    burn_calls=k*calls_per_half_life
    blocks=tail_blocks+ceil(F(burn_calls,2))
    s,_=probabilities(c)
    a=(1+s*s)/2
    false_reject=a**tail_blocks
    assert false_reject<=F(1,1<<k)<=alpha
    result={"hazard_threshold":str(threshold),"alpha":str(alpha),"k":k,
            "tail_echo_blocks":tail_blocks,"total_echo_blocks":blocks,
            "total_local_noise_calls":2*blocks,
            "fresh_P_zero_per_echo":str(a),
            "fresh_false_reject_probability":str(false_reject),
            "unsafe_false_accept_upper":str(F(1,1<<k)),
            "decision":"reject if and only if all final tail-block Z results arezero",
            "trusted_environment_reset":"once at calibration start; again before future operation",
            "system_preparation":"|0> at every echo block",
            "control":"two identity/noise calls and final destructive Z readout"}
    # Exact law at a small fixture threshold, not at enormous planned counts.
    if calls_per_half_life<=128:
        p=threshold
        f=(1-p)**(2*(blocks-tail_blocks))
        held=1-f
        for _ in range(tail_blocks):
            f,held=a*(1-p)**2*f,held+(p+p*(1-p)*a)*f
        allzero=f+held
        false_accept=1-allzero
        assert false_accept<=F(1,1<<k)
        result["exact_false_accept_at_threshold"]=str(false_accept)
    return result


def finite_program_plan(horizon,delta,alpha,c):
    pmax=delta/horizon
    result=echo_contract(pmax,alpha,c)
    result.update({"qualification":"every future adaptive program with at mostH local noise calls",
                   "H":horizon,"desired_output_TV_delta":str(delta),
                   "conditional_model_family":"fresh/held-Pauli5-state memory only",
                   "arbitrary_depth_uniform_claim":False,
                   "future_TV_bound_if_hazard_below_threshold":str(horizon*pmax)})
    return result


def discrete_model_contract(h,D,Q,Qref,alpha):
    """General separated rational realization promise; cost calculator only.

    Transition matrices and initial vector have common denominator q<=Q;
    reference denominator qref<=Qref; final trace functional is integral.
    """
    assert h>=2 and D>=1 and Q>=1 and Qref>=1
    horizon=(h*D)**2+h*h-1
    alphabet=h**4
    words=sum(alphabet**ell for ell in range(1,horizon+1))
    gamma_den=(Q*Qref)**(horizon+1)
    x=F(2*words,1)/alpha
    b=0
    while (1<<b)<x:
        b+=1
    # ln(2S/alpha)<=b. Hoeffding plus union bound for errorgamma/4.
    shots_per_word=8*gamma_den*gamma_den*b
    return {"system_Hilbert_dimension":h,"memory_Hilbert_bound":D,
            "exact_word_horizon":horizon,"IC_branch_alphabet":alphabet,
            "number_nonempty_words":words,"actual_common_denominator_upper":Q,
            "reference_common_denominator_upper":Qref,
            "nonzero_word_gap_at_least":"1/"+str(gamma_den),
            "per_word_probability_estimation_error":"1/"+str(4*gamma_den),
            "acceptance_tolerance":"1/"+str(2*gamma_den),
            "shots_per_word_sufficient":shots_per_word,
            "total_independent_resets_sufficient":words*shots_per_word,
            "total_noise_calls_upper":horizon*words*shots_per_word,
            "rational_height_promise_acquired":False,
            "calibration_not_executed":True}


def main():
    started=time.perf_counter()
    c=F(7,4)
    p=F(1,7)
    s,_=probabilities(c)
    ref=reachable_equivalence(c,F(0))
    alt=reachable_equivalence(c,p)
    assert ref["equivalent"] and not alt["equivalent"]
    actual,reference=word_probability([15]*3,c,p)
    assert actual-reference==p*(1-s*s)/4
    plans=[finite_program_plan(100,F(1,10),F(1,100),c),
           finite_program_plan(1_000_000,F(1,100),F(1,1000),c)]
    gap=echo_contract(F(1,32),F(1,1000),c)
    gap["qualification"]="exact all-depth fresh-model classification underp=0 orp>=1/32"
    obstruction={
        "calibration_expected_noise_calls":1_000_000,
        "alternative_hazard":"1/1000000000",
        "calibration_transcript_TV_upper":"1/1000",
        "memory_classical_states":5,
        "long_echo_plan":echo_contract(F(1,1_000_000_000),F(1,1024),c),
        "long_transcript_TV_lower":"511/512",
        "zero_hazard_acceptance_ge_1_minus_alpha_implies_alt_acceptance_ge":
        "1-alpha-1/1000",
        "isolated_channel_exactly_same":True}
    result={
        "status":"abstract operational construction and exact replay; no physical measurements",
        "root_all_d_frame_review":"FRAME_REVIEW.md",
        "isolated_channel_checks":isolated_average_checks(c,p),
        "known_matrix_equivalence_reference":ref,
        "known_matrix_equivalence_alternative":alt,
        "three_IC_Z_word":{"actual_probability":str(actual),
                           "reference_probability":str(reference),
                           "difference":str(actual-reference),
                           "formula":"p*(1-s^2)/4"},
        "finite_program_plans":plans,
        "gap_promised_all_depth_plan":gap,
        "indistinguishability_obstruction":obstruction,
        "general_discrete_promise_costs":[discrete_model_contract(2,1,2,2,F(1,100)),
                                        discrete_model_contract(2,2,20,20,F(1,100))],
        "ordinary_prior":"finite-word bilinear/quantum-machine equivalence and process-tensor tomography",
        "elapsed_seconds":time.perf_counter()-started}
    folder=Path(__file__).resolve().parent
    (folder/"RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
