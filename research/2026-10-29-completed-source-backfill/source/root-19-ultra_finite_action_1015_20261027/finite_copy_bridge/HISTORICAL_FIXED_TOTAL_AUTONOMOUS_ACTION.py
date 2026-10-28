#!/usr/bin/env python3
"""Construct a finite-copy, rate-bounded, autonomous one-shot majority action.

The compiler combines known six-state consensus and an ordinary Erlang delay.
It claims an explicit model interface, not a new device or a new majority method.
"""
from pathlib import Path
import hashlib
import json
import math
import time
from bridge import six_generator, SIX_RULES


HERE=Path(__file__).resolve().parent


def compile_action(nmax, volume, epsilon, kmin=1., kmax=1.,
                   clock_rate_ratio=2., trigger_min=1., dmin=0,
                   fixed_clock_rate_upper=None):
    """One-shot leader commits YES iff unknown input count A>B.

    nmax >= total computation agents (excluding the one clock/action leader).
    All inputs allowed when dmin=0; dmin>0 requires |A-B|>=dmin.
    The clock primitive must be acquired with step rates in [lambda-/lambda+].
    Supplied or bounded rates are not learned for free by this compiler.
    """
    assert nmax>=1 and volume>0 and 0<epsilon<1
    assert kmax>=kmin>0 and clock_rate_ratio>=1 and trigger_min>0
    eps_component=epsilon/4
    d=dmin
    theta=kmin*(d+1)/(2*volume)
    m=nmax//2
    log_mgf=sum(-math.log1p(-theta/(kmin*j*(j+d)/volume))
                for j in range(1,m+1))
    t_ann=(log_mgf+math.log(3/eps_component))/theta if m else 0
    clear=2*volume/(kmin*max(1,d))*math.log(3*nmax/eps_component)
    t_comp=t_ann+clear
    h_confidence=math.ceil(math.log(4/epsilon)/(math.log(2)-0.5))
    if fixed_clock_rate_upper is None:
        h=h_confidence
        clock_max=h/(2*t_comp)
        timer_interface='selectable slow clock rate; acquisition NOT established'
    else:
        assert fixed_clock_rate_upper>0
        h=max(h_confidence,math.ceil(2*fixed_clock_rate_upper*t_comp))
        clock_max=fixed_clock_rate_upper
        timer_interface='fixed clock rate bound; potentially large stage/species cost'
    clock_min=clock_max/clock_rate_ratio
    # Initial population is known to be nonempty. Using n>=1 is conservative.
    trigger_delay=volume/trigger_min*math.log(4/epsilon)
    upper_deadline=2*h/clock_min+trigger_delay
    mean_latency=h/clock_min+volume/trigger_min
    qmax=len(SIX_RULES)*kmax*nmax*nmax/volume
    clock_early=math.exp(-h*(math.log(2)-.5))
    clock_late=math.exp(-h*(1-math.log(2)))
    assert clock_early<=epsilon/4 and clock_late<=epsilon/4
    return {'nmax':nmax,'volume':volume,'epsilon_total':epsilon,
            'input_promise':'all A,B including ties' if not dmin else f'abs(A-B)>={dmin}',
            'computation_rate_interval':[kmin,kmax],
            'computation_failure_budget':eps_component,
            'computation_certificate_time':t_comp,
            'clock_stages':h,'clock_rate_interval':[clock_min,clock_max],
            'timer_interface':timer_interface,
            'clock_early_probability_bound':clock_early,
            'clock_late_probability_bound':clock_late,
            'trigger_rate_lower_bound':trigger_min,
            'trigger_tail_delay_using_n_ge_1':trigger_delay,
            'correct_action_by_deadline_probability_lower_bound':1-epsilon,
            'deadline':upper_deadline,'mean_action_latency_upper_bound':mean_latency,
            'computation_agents_at_most':nmax,'clock_action_leaders':1,
            'abstract_species':h+9,'abstract_reaction_channels':len(SIX_RULES)+h+6,
            'mean_computation_updates_before_action_upper_bound':qmax*mean_latency,
            'clock_updates_exact':h,'irreversible_action_updates_exact':1,
            'free_energy_joules':'UNKNOWN: no physical chemistry/fuel implementation acquired',
            'input_acquisition_and_single_leader_preparation':'SUPPLIED interface; physical costs UNKNOWN'}


def erlang_average(Q, p0, rate, stages):
    """Exact finite-dimensional phase-type formula; ordinary reference tool."""
    from scipy.sparse import eye
    from scipy.sparse.linalg import spsolve
    p=p0.copy()
    matrix=rate*eye(Q.shape[0],format='csc')-Q.T.tocsc()
    for _ in range(stages):p=spsolve(matrix,rate*p)
    return p


def action_error(Q,p_ready,wrong,total_rate):
    import numpy as np
    from scipy.sparse import eye
    from scipy.sparse.linalg import spsolve
    # Uniform local trigger rates give total collision hazard total_rate.
    # Nonuniform positive trigger rates are covered by the consensus theorem.
    b=spsolve(total_rate*eye(Q.shape[0],format='csc')-Q.tocsc(),total_rate*wrong)
    assert np.min(b)>-1e-12 and np.max(b)<1+1e-12
    return float(p_ready@b)


def test_compiler():
    import numpy as np
    from scipy.sparse import bmat, eye, csr_matrix
    from scipy.sparse.linalg import expm_multiply
    data=[]
    # Unknown logical inputs: both signs and the tie. Same9agent budget/volume.
    cases=[(2,2,5),(3,2,4),(2,3,4)]
    for a,b,spare in cases:
        total=a+b+spare;V=total
        Q,p0,wrong,nc,states=six_generator(a,b,spare,V)
        spec=compile_action(total,V,epsilon=.05,clock_rate_ratio=2)
        h=spec['clock_stages'];lo,hi=spec['clock_rate_interval']
        # Source/no-clock diagnosis is not the strongest comparator.
        unclocked=action_error(Q,p0,wrong,total/V)
        outcomes=[]
        for rate in [lo,hi]:
            ready=erlang_average(Q,p0,rate,h)
            err=action_error(Q,ready,wrong,total/V)
            assert abs(ready.sum()-1)<1e-11 and err<=spec['epsilon_total']/2+1e-10
            outcomes.append({'clock_rate':rate,'wrong_irreversible_action_probability':err,
                             'exact_model_mean_action_time':h/rate+V/total})
        # Equally informed ordinary implementation is exactly this six-state
        # protocol with the same Erlang clock and trigger: no invented uplift.
        # A deterministic external-clock benchmark gets stronger clock access.
        t=spec['computation_certificate_time']
        at_deadline=expm_multiply(Q.T*t,p0,traceA=float(Q.diagonal().sum()*t))
        external=action_error(Q,at_deadline,wrong,total/V)
        data.append({'a':a,'b':b,'spare':spare,'same_total_agents':total,
                     'reachable_computation_states':len(states),'compiler_spec':spec,
                     'unclocked_action_diagnostic_error':unclocked,
                     'rate_interval_endpoint_model_values':outcomes,
                     'ordinary_same_clock_comparator':'IDENTICAL channel and costs',
                     'stronger_external_deterministic_clock_error':external})
    # Independent full phase-state generator cross-check on one nontrivial case.
    a,b,spare=3,2,2;V=7
    Q,p0,wrong,nc,states=six_generator(a,b,spare,V)
    h=4;rate=.2;trigger=1.;n=Q.shape[0]
    # Transient row generator: computation evolves in each clock phase;
    # after final phase, trigger kills at constant hazard.
    blocks=[]
    I=eye(n,format='csr');Z=csr_matrix((n,n))
    for j in range(h+1):
        row=[]
        for k in range(h+1):
            if k==j: row.append(Q-(rate if j<h else trigger)*I)
            elif k==j+1 and j<h:row.append(rate*I)
            else:row.append(Z)
        blocks.append(row)
    T=bmat(blocks,format='csr')
    from scipy.sparse.linalg import spsolve
    p=np.zeros((h+1)*n);p[:n]=p0
    rhs=np.zeros((h+1)*n);rhs[h*n:]=trigger*wrong
    direct=float(p@spsolve(-T.tocsc(),rhs))
    reduced=action_error(Q,erlang_average(Q,p0,rate,h),wrong,trigger)
    assert abs(direct-reduced)<1e-12
    return {'matched_input_cases':data,'full_phase_generator_crosscheck':{
        'states':(h+1)*n,'clock_stages':h,'direct_absorption_error':direct,
        'ordinary_resolvent_composition_error':reduced,'absolute_difference':abs(direct-reduced)}}


def main():
    started=time.perf_counter()
    result={'status':'AUTONOMOUS_FINITE_COPY_ACTION_CONSTRUCTED_IN_ABSTRACT_RATE_BOUNDED_MODEL',
            'not_a_new_device_or_advantage':True,
            'derivation':'PROOF.md sections4-6','full_computation':test_compiler(),
            'large_population_contract_examples':[
                compile_action(1000,1000,.01,clock_rate_ratio=2),
                compile_action(1000,1000,.01,clock_rate_ratio=2,dmin=100),
                compile_action(1000,1000,.01,clock_rate_ratio=2,
                               fixed_clock_rate_upper=1.)],
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'wall_seconds':time.perf_counter()-started}
    # An actual serialized CRN for the unknown-input, upper-bound-only contract.
    spec=compile_action(9,9,.05,clock_rate_ratio=2)
    names=['P','N','Z','p','n','z']
    rules=[]
    for reactants,products in SIX_RULES:
        rules.append({'reactants':[names[x] for x in reactants],
                      'products':[names[x] for x in products],
                      'rate_interval':spec['computation_rate_interval']})
    h=spec['clock_stages']
    for j in range(h):
        rules.append({'reactants':[f'L{j}'],'products':[f'L{j+1}'],
                      'rate_interval':spec['clock_rate_interval']})
    for voter in names:
        rules.append({'reactants':[f'L{h}',voter],
                      'products':['ACTION_YES' if voter in ['P','p'] else 'ACTION_NO',voter],
                      'rate_lower_bound':spec['trigger_rate_lower_bound']})
    crn={'spec':spec,'input_species':['P','N'],
         'unknown_nonnegative_integer_inputs':'P+N<=8',
         'prepared_context':{'z':1,'L0':1},
         'species':names+[f'L{j}' for j in range(h+1)]+['ACTION_YES','ACTION_NO'],
         'reactions':rules,
         'physical_realization':'NOT_ACQUIRED; no sequences or experimental protocol'}
    assert len(crn['species'])==spec['abstract_species']
    assert len(crn['reactions'])==spec['abstract_reaction_channels']
    (HERE/'GENERATED_ACTION_CRN.json').write_text(json.dumps(crn,indent=2)+'\n')
    (HERE/'AUTONOMOUS_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
