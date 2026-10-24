"""Source-obtained record operators for recurrent fast hidden gating.

Per-phase hazards may couple a connected graph of leaves.  The checked source
pass proves that their stationary mean is additive, and bounds their contrast
using only small rule scopes.  A uniform controller-bridge certificate then
compares the true first-event operator with independent averaged propagation
followed by the EXACT observed jump/reset.

These positive approximations are record-likelihood operators.  They are not
asserted to be the event operators of a conservative reduced Markov simulator.
Fully resetting every hazard-dependent leaf to public values permits exact
branch aggregation within each CP component, including the hidden controller.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import json
import sys
import time

from pro3_gate_experiment import I,D,UP
from source_interface_compiler import (Program,Rule,InitialBranch,InitialFactor,SourceError,
                                      assignments,rational,matching,local_generator)
from tensor_reuse_entrance import load_acquired_action
from conditioned_count_queries import tv_from_spread

# Generated exact-rational record densities can legitimately exceed Python's
# default decimal-conversion length after several conditional updates.
sys.set_int_max_str_digits(0)


@dataclass
class AveragedGateSource:
    source:Program
    nu:F
    generators:list
    mean_killing:list
    constant_killing:F
    contrast_bound:F
    marked_rules:list
    mean_polynomial:dict
    contrast_groups:list


def cycle_source(n=24,nu=F(10**6),kappa=F(3,2)):
    if n<3:
        raise ValueError('The connected-cycle demonstration needs at least three leaves')
    rules=[Rule('gate_opens',((0,0),),((0,1),),nu),
           Rule('gate_closes',((0,1),),((0,0),),nu)]
    factors=[]
    for i in range(n):
        site=i+1; alpha=F(3,5)+F(i,100); beta=F(2,5)+F(i%5,50)
        rules.extend([Rule(f'up_{i}',((site,0),),((site,1),),alpha),
                      Rule(f'down_{i}',((site,1),),((site,0),),beta)])
        factors.append(InitialFactor((site,),(F(1),F(0))))
    for edge in range(n):
        left=edge+1; right=(edge+1)%n+1; reset=((left,0),(right,0)); mark=f'edge_{edge}'
        rules.append(Rule(f'and_{edge}',((0,1),(left,1),(right,1)),reset,kappa,mark))
        for x,y in ((0,1),(1,0),(1,1)):
            rules.append(Rule(f'or_{edge}_{x}{y}',((0,0),(left,x),(right,y)),reset,kappa,mark))
    return Program(n+1,(0,),tuple(rules),(InitialBranch(F(1),((0,0),),tuple(factors)),))


def guard_polynomial(guard,rate):
    polynomial={frozenset():F(rate)}
    for site,bit in sorted(guard.items()):
        if site==0:
            continue
        updated={}
        for monomial,value in polynomial.items():
            enlarged=monomial|{site}
            if bit:
                updated[enlarged]=updated.get(enlarged,F(0))+value
            else:
                updated[monomial]=updated.get(monomial,F(0))+value
                updated[enlarged]=updated.get(enlarged,F(0))-value
        polynomial={key:value for key,value in updated.items() if value}
    return polynomial


def compile_source(source,max_guard_scope=8):
    """A new checked source pass; it never merges leaves because of hazards."""
    if type(source.nsites) is not int or source.nsites<2 or source.controller!=(0,):
        raise SourceError('fast_gate_source_scope',requirement='one Boolean controller at site0')
    data=[]; names=set(); marked=[]; controller=[]; leaves={i:[] for i in range(1,source.nsites)}
    for rule in source.rules:
        if not isinstance(rule.name,str) or not rule.name or rule.name in names:
            raise SourceError('invalid_rule_name',name=rule.name)
        names.add(rule.name); rate=rational(rule.rate,rule.name+'.rate')
        guard=assignments(rule.guard,source.nsites,rule.name+'.guard')
        update=assignments(rule.update,source.nsites,rule.name+'.update')
        entry=(rule,guard,update); data.append(entry)
        if rule.mark is None:
            if len(update)!=1:
                raise SourceError('silent_write_arity',rule=rule.name)
            written=next(iter(update))
            if written==0:
                if set(guard)-{0}:
                    raise SourceError('controller_not_autonomous',rule=rule.name)
                controller.append(entry)
            else:
                if set(guard)-{0,written}:
                    raise SourceError('coupled_silent_dynamics',rule=rule.name)
                leaves[written].append(entry)
        else:
            if not isinstance(rule.mark,str) or not rule.mark:
                raise SourceError('invalid_mark',rule=rule.name)
            if len(set(guard)-{0})>max_guard_scope:
                raise SourceError('local_guard_budget',rule=rule.name)
            if rate:
                marked.append(entry)
    cq=local_generator((0,),((0,),(1,)),controller,{})
    nu=cq[0][1]
    if nu<=0 or cq!=((-nu,nu),(nu,-nu)):
        raise SourceError('controller_not_symmetric_telegraph',generator=cq)
    generators=[]
    for site,rules in leaves.items():
        q0=local_generator((site,),((0,),(1,)),rules,{0:0})
        q1=local_generator((site,),((0,),(1,)),rules,{0:1})
        if q0!=q1 or min(q0[0][1],q0[1][0])<=0:
            raise SourceError('silent_generator_scope',site=site,
                              requirement='positive binary rates unchanged by controller')
        generators.append(q0)
    phase=[{},{}]; groups={}
    for rule,guard,update in marked:
        scope=tuple(sorted(set(guard)-{0})); groups.setdefault(scope,[]).append((rule,guard,update))
        polynomial=guard_polynomial(guard,rule.rate)
        for c in (0,1):
            if 0 in guard and guard[0]!=c:
                continue
            for monomial,value in polynomial.items():
                phase[c][monomial]=phase[c].get(monomial,F(0))+value
    mean={key:(phase[0].get(key,F(0))+phase[1].get(key,F(0)))/2
          for key in set(phase[0])|set(phase[1])}
    mean={key:value for key,value in mean.items() if value}
    higher={tuple(sorted(key)):value for key,value in mean.items() if len(key)>1}
    if higher:
        raise SourceError('stationary_mean_not_additive',witness={str(k):str(v) for k,v in higher.items()})
    coefficients=[mean.get(frozenset((site,)),F(0)) for site in leaves]
    constant=mean.get(frozenset(),F(0))+sum(min(F(0),x) for x in coefficients)
    if constant<0:
        raise SourceError('negative_additive_mean_offset')
    killing=[(max(F(0),-x),max(F(0),x)) for x in coefficients]
    contrast_groups=[]; total_min=F(0); total_max=F(0)
    for scope,rules in groups.items():
        contrasts=[]
        for values in product((0,1),repeat=len(scope)):
            env=dict(zip(scope,values)); hazards=[]
            for c in (0,1):
                hazards.append(sum(F(rule.rate) for rule,guard,_ in rules if matching(guard,env|{0:c})))
            contrasts.append((hazards[1]-hazards[0])/2)
        lo=min(contrasts); hi=max(contrasts); total_min+=lo; total_max+=hi
        contrast_groups.append({'scope':list(scope),'local_min_exact':str(lo),'local_max_exact':str(hi),
                                'local_assignments_checked':2**len(scope)})
    amplitude=max(abs(total_min),abs(total_max))
    return AveragedGateSource(source,nu,generators,killing,constant,amplitude,marked,mean,contrast_groups)


def bridge_bound(nu,amplitude,t):
    if nu<=0 or amplitude<0 or t<=0:
        raise ValueError('Invalid controller bridge parameters')
    if amplitude==0:
        return F(1),F(1),{'dyson_relative_upper_excess':'0','jensen_exponent_upper':'0'}
    nu_i=I(nu); a=I(amplitude); time_i=I(t)
    E=(-2*nu_i*time_i).exp(); E=I(max(D(0),E.lo),E.hi)
    root=(nu_i*nu_i+a*a).sqrt()
    slow=a*a/(root+nu_i)
    slow_exp=(slow*time_i).exp(); fast_exp=(-(root+nu_i)*time_i).exp()
    fast_exp=I(max(D(0),fast_exp.lo),fast_exp.hi)
    S=(1+a/root)*slow_exp+(1-a/root)*fast_exp-1-E
    excess=(I(max(D(0),S.hi))/(1-E)).hi
    theta=(1-E)/(1+E)
    jensen_exponent=a*theta/nu_i
    lower=F((-jensen_exponent).exp().lo)
    # Both the Dyson estimate and the trivial bounded-potential estimate are
    # valid upper bounds.  The latter protects short intervals.
    upper=min(F((1+I(excess)).hi),F((a*time_i).exp().hi))
    return lower,upper,{'dyson_relative_upper_excess':str(excess),
        'jensen_exponent_upper':str(jensen_exponent.hi),
        'stable_slow_exponent_rate_upper':str(slow.hi)}


def killed_matrix(q,killing,t):
    alpha,beta=I(q[0][1]),I(q[1][0]); d0,d1=map(I,killing)
    a0=alpha+d0; a1=beta+d1
    gap=((a0-a1)*(a0-a1)+4*alpha*beta).sqrt()
    slow=(a0+a1-gap)/2; fast=(a0+a1+gap)/2
    es=(-slow*I(t)).exp(); ef=(-fast*I(t)).exp()
    return [[((fast-a0)*es+(a0-slow)*ef)/gap,alpha*(es-ef)/gap],
            [beta*(es-ef)/gap,((fast-a1)*es+(a1-slow)*ef)/gap]]


def acquire_record_operators(compiled,t):
    lower,upper,bound=bridge_bound(compiled.nu,compiled.contrast_bound,F(t))
    decay=(-2*I(compiled.nu)*I(t)).exp(); decay=I(max(D(0),decay.lo),decay.hi)
    controller=[[(1+decay)/2,(1-decay)/2],[(1-decay)/2,(1+decay)/2]]
    matrices=[controller]+[killed_matrix(q,d,F(t)) for q,d in zip(compiled.generators,compiled.mean_killing)]
    scalar=I(1) if compiled.constant_killing==0 else (-I(compiled.constant_killing)*I(t)).exp()
    if scalar.lo<=0:
        raise ValueError('Positive propagation scalar unresolved')
    ratio=I(scalar.hi)/I(scalar.lo); rational_matrices=[]
    for matrix in matrices:
        if any(v.lo<=0 for row in matrix for v in row):
            raise ValueError('Positive average propagator support unresolved')
        local=max((I(v.hi)/I(v.lo)).hi for row in matrix for v in row)
        ratio=ratio*I(local)
        rational_matrices.append([[F(v.lo) for v in row] for row in matrix])
    numerical=F(ratio.hi); effective_upper=upper*numerical
    spread=effective_upper/lower
    certificate={'comparison':'lower_multiplier*Khat_mark <= Ktrue_mark <= upper_multiplier*Khat_mark entrywise for every checked mark and every joint controller/leaf input',
        'lower_multiplier_exact':str(lower),'upper_multiplier_exact':str(effective_upper),
        'analytic_upper_multiplier_exact':str(upper),'numerical_propagator_spread_upper_exact':str(numerical),
        'spread_factor_upper_exact':str(spread),'all_input_posterior_TV_upper':str(tv_from_spread(spread)),
        'controller_flip_rate_exact':str(compiled.nu),'half_contrast_bound_exact':str(compiled.contrast_bound),
        'elapsed_time':str(t),'controller_bridge_bound':bound,
        'leaf_switching_rates_enter_error_bound':False,
        'operator_scope':'positive first-event record-likelihood operators; no assertion of a conservative reduced marked CTMC'}
    return {'controller':rational_matrices[0],'leaves':rational_matrices[1:],
            'scalar':F(scalar.lo),'certificate':certificate,'duration':F(t)}


def fixed_reset_schema(compiled,mark):
    selected=[entry for entry in compiled.marked_rules if entry[0].mark==mark]
    if not selected:
        raise SourceError('missing_event_mark',mark=mark)
    resets=[{site-1:value for site,value in update.items() if site!=0} for _,_,update in selected]
    if any(reset!=resets[0] for reset in resets):
        raise SourceError('branch_dependent_leaf_reset',mark=mark)
    active={site-1 for _,guard,_ in selected for site in guard if site!=0}
    if not active<=set(resets[0]):
        raise SourceError('hazard_variable_not_fully_reset',mark=mark)
    return selected,resets[0],active


def workload_certificate(compiled,max_events,horizon,entrance_spread,numerical_spread=F(1)):
    """Certify every admitted identified-event record in a bounded workload.

    The numerical_spread argument is a multiplicative budget for all numerical
    propagation/application errors across the entire workload, not per event.
    A value of one certifies mathematical exact averaged operators.  No source
    parameter is changed to make the error small.  Terminal no-event tails are
    not included; count such an additional operator in an enlarged budget.
    """
    if type(max_events) is not int or max_events<0:
        raise ValueError('max_events must be a nonnegative integer')
    horizon=F(horizon); entrance_spread=F(entrance_spread); numerical_spread=F(numerical_spread)
    if horizon<0 or entrance_spread<1 or numerical_spread<1:
        raise ValueError('Invalid workload horizon or projective-spread budget')
    marks=sorted({rule.mark for rule,_,_ in compiled.marked_rules})
    if not marks:
        raise SourceError('empty_admitted_event_interface')
    for mark in marks:
        fixed_reset_schema(compiled,mark)
    A=compiled.contrast_bound; nu=compiled.nu
    # log(1+A/nu)<=A/nu gives this explicit source-only envelope.  The
    # bounded-potential alternative can be better for short workloads.
    log_upper=min((2*max_events*A+A*A*horizon/2)/nu,2*A*horizon)
    analytic=F((I(log_upper).exp()).hi) if log_upper else F(1)
    spread=entrance_spread*numerical_spread*analytic
    return {'scientific_object':'uniform certificate for an identified-reset-event workload',
        'max_observed_events':max_events,'total_event_lag_horizon_exact':str(horizon),
        'admitted_marks':marks,'every_admitted_mark_passes_fixed_reset_schema':True,
        'state_CP_component_count_cannot_increase':True,
        'analytic_log_spread_upper_exact':str(log_upper),
        'analytic_spread_upper_exact':str(analytic),
        'entrance_spread_exact':str(entrance_spread),
        'whole_workload_numerical_spread_budget_exact':str(numerical_spread),
        'whole_workload_projective_spread_upper_exact':str(spread),
        'uniform_posterior_TV_upper':str(tv_from_spread(spread)),
        'fixed_source_controller_flip_rate_exact':str(nu),
        'fixed_source_half_contrast_bound_exact':str(A),
        'source_parameters_altered_to_meet_budget':False,
        'scope':'all sequences of the admitted marks with at most max_events positive lags summing to at most horizon; exact common later conditioning preserves the certificate',
        'terminal_no_event_tail_included':False,
        'storage_bound':'R product components with O(R*n) scalar storage; precision and rational bit size are additional costs'}


def apply_cp_record(compiled,operator,weights,controller_one,leaf_one,mark):
    if not (len(weights)==len(controller_one)==len(leaf_one)) or not weights:
        raise ValueError('Mismatched or empty CP representation')
    if sum(weights,F(0))!=1 or any(w<=0 for w in weights):
        raise ValueError('CP weights must be strictly positive and sum exactly to one')
    if any(p<0 or p>1 for p in controller_one):
        raise ValueError('Invalid controller probability')
    if any(len(row)!=len(operator['leaves']) or any(p<0 or p>1 for p in row) for row in leaf_one):
        raise ValueError('Invalid leaf probability rows')
    selected,reset,active=fixed_reset_schema(compiled,mark)
    new_masses=[]; new_controller=[]; new_leaves=[]; application_spread=D(1)
    for weight,controller_p,leaves in zip(weights,controller_one,leaf_one):
        coefficient=I(weight)*I(operator['scalar'])
        if coefficient.lo<=0:
            raise ValueError('Positive component weight unresolved')
        ratio=I(coefficient.hi)/I(coefficient.lo)
        controller_before=(I(1-controller_p),I(controller_p))
        control=[sum((controller_before[x]*I(operator['controller'][x][y]) for x in (0,1)),I(0)) for y in (0,1)]
        ratio=ratio*I(max((I(v.hi)/I(v.lo)).hi for v in control))
        control_lower=[F(v.lo) for v in control]
        mass=F(coefficient.lo); probabilities=[]
        for p,matrix in zip(leaves,operator['leaves']):
            before=(I(1-p),I(p))
            after=[sum((before[x]*I(matrix[x][y]) for x in (0,1)),I(0)) for y in (0,1)]
            if min(v.lo for v in after)<=0:
                raise ValueError('Positive propagated leaf support unresolved')
            ratio=ratio*I(max((I(v.hi)/I(v.lo)).hi for v in after))
            zero,one=F(after[0].lo),F(after[1].lo); local_mass=zero+one
            mass*=local_mass; probabilities.append(one/local_mass)
        # Controller lower-row mass is retained here.  Hazard expectations
        # use normalized leaf factors, whose masses already multiply mass.
        output_controller=[F(0),F(0)]
        for rule,guard,update in selected:
            for c in (0,1):
                if 0 in guard and guard[0]!=c:
                    continue
                contribution=control_lower[c]*F(rule.rate)
                for site,bit in guard.items():
                    if site:
                        p=probabilities[site-1]; contribution*=p if bit else 1-p
                output_controller[update.get(0,c)]+=contribution
        hazard_mass=sum(output_controller,F(0))
        if hazard_mass<=0:
            raise ValueError('Observed event has zero retained density')
        mass*=hazard_mass
        for site,value in reset.items():
            probabilities[site]=F(value)
        new_masses.append(mass); new_leaves.append(probabilities)
        new_controller.append(output_controller[1]/hazard_mass)
        application_spread=max(application_spread,ratio.hi)
    normalizer=sum(new_masses,F(0))
    if normalizer<=0:
        raise ValueError('Record density is not positive')
    new_weights=[mass/normalizer for mass in new_masses]
    assert sum(new_weights,F(0))==1
    return new_weights,new_controller,new_leaves,normalizer,F(application_spread)


def serialize_operator(compiled,operator,path):
    jumps=[]
    for rule,guard,update in compiled.marked_rules:
        jumps.append({'name':rule.name,'mark':rule.mark,'guard':[list(x) for x in sorted(guard.items())],
                      'fixed_update':[list(x) for x in sorted(update.items())],'rate_exact':str(rule.rate)})
    data={'scientific_object':'all-input relative-certified recurrent-controller record-likelihood interface',
        'new_work':True,'controller_and_leaf_sites':compiled.source.nsites,
        'exact_rational_controller_propagator':[[str(x) for x in row] for row in operator['controller']],
        'exact_rational_leaf_propagators':[[[str(x) for x in row] for row in matrix] for matrix in operator['leaves']],
        'exact_rational_propagation_scalar':str(operator['scalar']),
        'exact_marked_guard_reset_rules':jumps,
        'checked_kinetic_source_rules':[
            {'name':rule.name,'guard':[list(x) for x in rule.guard],
             'fixed_update':[list(x) for x in rule.update],
             'rate_exact':str(rule.rate),'mark':rule.mark}
            for rule in compiled.source.rules],
        'operator_definition':'common positive product propagation followed by the exact sum of guard/reset branches with the observed mark; normalize only after the full input law is propagated',
        'mean_killing_exact':[[str(x) for x in row] for row in compiled.mean_killing],
        'mean_constant_killing_exact':str(compiled.constant_killing),
        'certificate':operator['certificate'],
        'normalizer_kind':'event-time density, not a probability',
        'initial_distribution_is_runtime_argument':True,
        'conservative_reduced_marked_CTMC_claimed':False}
    Path(path).write_text(json.dumps(data,separators=(',',':')))


def load_record_interface(path):
    """Reuse saved rational operators without reevaluating any exponential.

    Validate the compact kinetic source and the exact retained object.  The
    analytical/numerical certificate remains the stored construction witness;
    this loader does not silently reacquire the object it is meant to reuse.
    """
    data=json.loads(Path(path).read_text()); nsites=data['controller_and_leaf_sites']
    source_rules=[]
    for entry in data['checked_kinetic_source_rules']:
        source_rules.append(Rule(entry['name'],tuple(map(tuple,entry['guard'])),
            tuple(map(tuple,entry['fixed_update'])),F(entry['rate_exact']),entry['mark']))
    compiled=compile_source(Program(nsites,(0,),tuple(source_rules),()))
    if [[str(x) for x in row] for row in compiled.mean_killing]!=data['mean_killing_exact']:
        raise ValueError('Stored mean killing differs from the checked source')
    if F(data['mean_constant_killing_exact'])!=compiled.constant_killing:
        raise ValueError('Stored mean killing constant differs from the source')
    certificate=data['certificate']; duration=F(certificate['elapsed_time'])
    if duration<=0 or F(certificate['controller_flip_rate_exact'])!=compiled.nu:
        raise ValueError('Invalid retained time or controller parameter')
    if F(certificate['half_contrast_bound_exact'])!=compiled.contrast_bound:
        raise ValueError('Stored contrast bound differs from the checked source')
    lower=F(certificate['lower_multiplier_exact']); upper=F(certificate['upper_multiplier_exact'])
    if not (0<lower<=upper) or F(certificate['spread_factor_upper_exact'])!=upper/lower:
        raise ValueError('Invalid retained relative certificate')
    controller=[[F(x) for x in row] for row in data['exact_rational_controller_propagator']]
    leaves=[[[F(x) for x in row] for row in matrix] for matrix in data['exact_rational_leaf_propagators']]
    if len(leaves)!=nsites-1:
        raise ValueError('Wrong number of retained local propagators')
    for matrix in [controller]+leaves:
        if len(matrix)!=2 or any(len(row)!=2 or min(row)<=0 for row in matrix):
            raise ValueError('Invalid retained positive binary propagator')
    scalar=F(data['exact_rational_propagation_scalar'])
    if scalar<=0:
        raise ValueError('Invalid retained positive propagation scalar')
    saved_jumps=[(entry['name'],entry['mark'],dict(entry['guard']),dict(entry['fixed_update']),F(entry['rate_exact']))
                 for entry in data['exact_marked_guard_reset_rules']]
    source_jumps=[(rule.name,rule.mark,guard,update,F(rule.rate)) for rule,guard,update in compiled.marked_rules]
    if saved_jumps!=source_jumps:
        raise ValueError('Stored jump interface differs from the checked source')
    for mark in {rule.mark for rule,_,_ in compiled.marked_rules}:
        fixed_reset_schema(compiled,mark)
    return compiled,{'controller':controller,'leaves':leaves,'scalar':scalar,
                     'certificate':certificate,'duration':duration}


def load_cp_posterior(path):
    """Load the exact retained joint controller/leaf CP posterior."""
    data=json.loads(Path(path).read_text())
    weights=list(map(F,data['exact_rational_weights']))
    controller=list(map(F,data['exact_rational_controller_probability_one']))
    leaves=[list(map(F,row)) for row in data['exact_rational_leaf_probability_one']]
    if not weights or len(weights)!=len(controller) or len(weights)!=len(leaves):
        raise ValueError('Mismatched retained CP dimensions')
    if any(w<=0 for w in weights) or sum(weights,F(0))!=1:
        raise ValueError('Invalid retained exact CP weights')
    if any(p<0 or p>1 for p in controller) or any(p<0 or p>1 for row in leaves for p in row):
        raise ValueError('Invalid retained local probabilities')
    if len({len(row) for row in leaves})!=1:
        raise ValueError('Mismatched retained leaf dimensions')
    spread=F(data['posterior_projective_spread_upper_exact'])
    if spread<1:
        raise ValueError('Invalid retained posterior projective spread')
    return weights,controller,leaves,spread


def matrix_multiply(left,right):
    size=len(left)
    return [[sum((left[i][k]*right[k][j] for k in range(size)),I(0)) for j in range(size)] for i in range(size)]


def scaled_uniformization_reference(compiled,t,mark='edge_0'):
    """Independent full small-generator interval reference, including stiffness."""
    n=len(compiled.generators)
    if n>4:
        raise ValueError('Expanded reference restricted to at most four leaves')
    states=list(product((0,1),repeat=n+1)); index={x:i for i,x in enumerate(states)}; size=len(states)
    Q=[[F(0) for _ in states] for _ in states]
    for row,x in enumerate(states):
        y=(1-x[0],)+x[1:]; Q[row][index[y]]+=compiled.nu
        for i,q in enumerate(compiled.generators):
            y=list(x); y[i+1]=1-y[i+1]; Q[row][index[tuple(y)]]+=q[x[i+1]][1-x[i+1]]
        Q[row][row]=-sum(Q[row])
        env=dict(enumerate(x))
        Q[row][row]-=sum(F(rule.rate) for rule,guard,_ in compiled.marked_rules if matching(guard,env))
    rate=max(-Q[i][i] for i in range(size)); squarings=0; step=F(t)
    while rate*step>F(1,2):
        step/=2; squarings+=1
    transition=[[I(F(int(i==j))+Q[i][j]/rate) for j in range(size)] for i in range(size)]
    current=[[I(int(i==j)) for j in range(size)] for i in range(size)]
    accumulated=[[I(int(i==j)) for j in range(size)] for i in range(size)]
    z=rate*step; term=F(1); terms=40
    for order in range(1,terms+1):
        current=matrix_multiply(current,transition); term*=z/order
        accumulated=[[accumulated[i][j]+I(term)*current[i][j] for j in range(size)] for i in range(size)]
    exponential=(-I(z)).exp(); first=term*z/(terms+1)
    tail=I(F(exponential.hi)*first/(1-z/(terms+2)))
    reference=[]
    for row in accumulated:
        values=[]
        for value in row:
            partial=exponential*value
            values.append(I(max(D(0),partial.lo),min(D(1),UP.add(partial.hi,tail.hi))))
        reference.append(values)
    for _ in range(squarings):
        reference=matrix_multiply(reference,reference)
        reference=[[I(max(D(0),v.lo),min(D(1),v.hi)) for v in row] for row in reference]
    return states,reference,{'expanded_states':size,'uniformization_terms_per_scaled_step':terms+1,
                             'positive_matrix_squarings':squarings,'scaled_poisson_tail_upper':str(tail.hi)}


def small_operator_check():
    compiled=compile_source(cycle_source(3,nu=F(10**6)))
    operator=acquire_record_operators(compiled,F(1,10)); mark='edge_0'
    states,reference,information=scaled_uniformization_reference(compiled,F(1,10),mark)
    selected=[entry for entry in compiled.marked_rules if entry[0].mark==mark]
    lower=F(operator['certificate']['lower_multiplier_exact']); upper=F(operator['certificate']['upper_multiplier_exact'])
    positive=0; zeros=0
    for initial_index,initial in enumerate(states):
        exact_reference=[I(0) for _ in states]; approximate=[F(0) for _ in states]
        for before_index,before in enumerate(states):
            env=dict(enumerate(before))
            propagated=operator['scalar']*operator['controller'][initial[0]][before[0]]
            for i,matrix in enumerate(operator['leaves']):
                propagated*=matrix[initial[i+1]][before[i+1]]
            for rule,guard,update in selected:
                if matching(guard,env):
                    after=tuple((env|update)[i] for i in range(len(before)))
                    output=states.index(after)
                    exact_reference[output]=exact_reference[output]+reference[initial_index][before_index]*I(rule.rate)
                    approximate[output]+=propagated*F(rule.rate)
        for value,ref in zip(approximate,exact_reference):
            if value==0:
                assert ref.lo==0 and ref.hi==0; zeros+=1
            else:
                if not F(ref.lo)>=lower*value or not F(ref.hi)<=upper*value:
                    raise AssertionError('Full coupled recurrent-generator reference outside relative certificate')
                positive+=1
    information.update({'all_joint_controller_leaf_input_rows_checked':len(states),
        'positive_event_operator_entries_checked':positive,'structural_zero_entries_checked':zeros,
        'all_expanded_entry_enclosures_inside_operator_sandwich':True})
    return information


def run():
    started=time.perf_counter(); compiled=compile_source(cycle_source())
    duration=F(1,10); operator=acquire_record_operators(compiled,duration)
    serialize_operator(compiled,operator,'fast_switching_record_interface_24sites.json')
    compiled,operator=load_record_interface('fast_switching_record_interface_24sites.json')
    entrance_path=Path('relative_correlated_entrance_24sites.json')
    entrance=json.loads(entrance_path.read_text())
    modules,weights,leaves,_=load_acquired_action(entrance_path)
    if len(modules)!=len(compiled.generators) or any(
        module.alpha!=q[0][1] or module.beta!=q[1][0]
        for module,q in zip(modules,compiled.generators)):
        raise ValueError('Prepared entrance and new future source do not have the claimed common silent leaf generators')
    controller=[F(1) for _ in weights]
    inherited=F(entrance['relative_projective_certificate']['spread_factor_upper_exact'])
    spread=inherited; record_density=F(1); likelihood_lower=F(1); likelihood_upper=F(1); records=[]
    a=F(operator['certificate']['lower_multiplier_exact']); b=F(operator['certificate']['upper_multiplier_exact'])
    for mark in ('edge_0','edge_1','edge_2','edge_0'):
        before_count=len(weights)
        weights,controller,leaves,density,numerical=apply_cp_record(compiled,operator,weights,controller,leaves,mark)
        assert len(weights)==before_count==256
        record_density*=density; likelihood_lower*=a; likelihood_upper*=b*numerical
        spread*=b*numerical/a
        records.append({'mark':mark,'elapsed_since_previous_event':str(duration),
            'phase_observed':False,'controller_reset_between_events':False,
            'positive_product_components':len(weights),
            'application_numerical_spread_minus_one_upper':str(I(numerical-1).hi),
            'whole_joint_controller_leaf_posterior_TV_upper':str(tv_from_spread(spread))})
    posterior={'scientific_object':'conditional joint controller and leaf posterior after recurrent coupled-gate edge record',
        'new_work':True,'prepared_entrance_file':str(entrance_path),
        'new_future_kinetic_source':'connected cycle of AND hazards in controller1 and OR hazards in controller0; symmetric recurrent controller; same silent leaf generators',
        'record_interface_file':'fast_switching_record_interface_24sites.json','record':records,
        'exact_rational_weights':[str(w) for w in weights],
        'exact_rational_controller_probability_one':[str(p) for p in controller],
        'exact_rational_leaf_probability_one':[[str(p) for p in row] for row in leaves],
        'normalization_checked_exactly':sum(weights,F(0))==1,
        'posterior_projective_spread_upper_exact':str(spread),
        'whole_joint_controller_leaf_posterior_TV_upper':str(tv_from_spread(spread)),
        'approximate_record_density_exact':str(record_density),
        'normalizer_kind':'joint density of the four event times and observed edge marks, not a probability',
        'full_correlated_input_retained':True,'component_count_preserved':True,
        'conservative_reduced_marked_CTMC_claimed':False}
    Path('fast_switching_record_posterior_24sites.json').write_text(json.dumps(posterior,separators=(',',':')))
    controller_p=sum(w*p for w,p in zip(weights,controller))
    site23_p=sum(w*p[-1] for w,p in zip(weights,leaves))
    error=I(tv_from_spread(spread))
    def bounded(p):
        return [str(max(D(0),(I(p)-error).lo)),str(min(D(1),(I(p)+error).hi))]
    output={'new_work':True,'source_rules':len(compiled.source.rules),'source_leaves':len(compiled.generators),
        'source_state_count':str(2**compiled.source.nsites),
        'per_phase_hazard_graph':'one connected cycle; phasewise killing is not additive across leaves',
        'stationary_mean_killing_obtained_exactly':[[str(x) for x in row] for row in compiled.mean_killing],
        'mean_polynomial_higher_order_coefficients_cancelled':True,
        'contrast_bound_exact':str(compiled.contrast_bound),'contrast_scope_checks':compiled.contrast_groups,
        'acquired_record_operator_certificate':operator['certificate'],
        'record_updates':records,'final_positive_product_components':len(weights),
        'controller_phase_observed':False,'controller_reset_between_events':False,
        'whole_record_density_interval':[str(I(record_density*likelihood_lower/inherited).lo),
                                         str(I(record_density*likelihood_upper*inherited).hi)],
        'final_whole_joint_posterior_TV_upper':str(tv_from_spread(spread)),
        'final_controller_on_probability_interval':bounded(controller_p),
        'final_site23_active_probability_interval':bounded(site23_p),
        'prepared_entrance_acquisition_recomputed':False,
        'prepared_entrance_silent_generator_compatibility_checked_exactly':True,
        'record_updates_consumed_reloaded_retained_interface':True,
        'uniform_exact_averaged_operator_workload_certificate':workload_certificate(compiled,4,4*duration,inherited),
        'controller_rate_status':'supplied synthetic kinetic parameter; no empirical fast-controller or incumbent-speed claim',
        'independent_small_coupled_reference':small_operator_check(),
        'elapsed_seconds':time.perf_counter()-started,
        'scope':'record-likelihood approximation with an all-input relative certificate; no claim of a conservative reduced simulator or fixed-width unresolved-count-history filtering'}
    Path('fast_switching_event_kernel_results.json').write_text(json.dumps(output,indent=2))
    return output


if __name__=='__main__':
    result=run()
    print(json.dumps({k:v for k,v in result.items() if k not in ('contrast_scope_checks','stationary_mean_killing_obtained_exactly')},indent=2))
