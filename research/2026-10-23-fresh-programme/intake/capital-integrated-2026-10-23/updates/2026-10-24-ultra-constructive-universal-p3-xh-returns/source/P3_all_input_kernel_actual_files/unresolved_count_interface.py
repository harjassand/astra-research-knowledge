"""A positive count-accumulator interface for an unresolved total turnover.

The observation is only sum_i N_i(T)=K.  Count allocations and final leaf
configurations stay implicit.  Each retained component is a nonnegative
counter tensor train with bond K+1 and physical local indices (N_i, X_i).
Its factors are exact integers, its component normalizer is exact, and its
mixture weights are exact rational numbers.  Entrywise operator enclosures
propagate the acquired entrance's projective certificate.

This is new work and uses the available local count-kernel implementation.
It neither reacquires the entrance nor repeats an earlier count record.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import lcm, prod
from pathlib import Path
import itertools
import json
import time

from pro3_gate_experiment import I, D
from tensor_separator_entrance import BinaryModule
from tensor_reuse_entrance import load_acquired_action
from conditioned_count_queries import count_kernel, tv_from_spread


def coefficient_integer(polynomials,total):
    """Extract [z^total] by nonnegative integer coefficient convolution."""
    accumulator=[1]+[0]*total
    for polynomial in polynomials:
        accumulator=[sum(accumulator[j]*polynomial[k-j] for j in range(k+1))
                     for k in range(total+1)]
    return accumulator[total]


def coefficient_interval(polynomials,total):
    accumulator=[I(1)]+[I(0) for _ in range(total)]
    for polynomial in polynomials:
        accumulator=[sum((accumulator[j]*polynomial[k-j] for j in range(k+1)),I(0))
                     for k in range(total+1)]
    return accumulator[total]


def integerize(values):
    values=[F(x) for x in values]
    denominator=lcm(*(x.denominator for x in values))
    return [x.numerator*(denominator//x.denominator) for x in values],denominator


@dataclass
class CountInterface:
    modules: list
    total: int
    duration: F
    weights: list
    factors: list
    component_normalizers: list
    factor_denominators: list
    input_weights: list
    record_mass: F
    entrance_spread: F
    numerical_spread: F

    @property
    def spread(self):
        return self.entrance_spread*self.numerical_spread


def compile_interface(modules,weights,probabilities,duration,total,entrance_spread=F(1)):
    if type(total) is not int or total<0 or duration<=0 or entrance_spread<1:
        raise ValueError('Positive duration, nonnegative total count, and valid source spread required')
    if not modules or len(weights)!=len(probabilities) or not weights:
        raise ValueError('Invalid initial mixture dimensions')
    if any(w<0 for w in weights) or sum(weights,F(0))!=1:
        raise ValueError('Initial mixture weights must form an exact probability law')
    if any(len(row)!=len(modules) or any(p<0 or p>1 for p in row) for row in probabilities):
        raise ValueError('Invalid initial local probabilities')
    kernels=[]; tail=F(0)
    for module in modules:
        local=[]
        for count in range(total+1):
            matrix,omitted,_=count_kernel(module.alpha,module.beta,module.kappa,duration,count)
            local.append(matrix); tail=max(tail,omitted)
        kernels.append(local)
    all_factors=[]; all_denominators=[]; component_normalizers=[]; masses=[]
    numerical_spread=D(1); zero_factors=0
    for weight,probability_row in zip(weights,probabilities):
        factors=[]; denominators=[]; term_spread=I(1)
        for probability,local_kernels in zip(probability_row,kernels):
            before=(I(1-probability),I(probability))
            lower=[]; local_spread=D(1)
            for matrix in local_kernels:
                for final in (0,1):
                    value=sum((before[initial]*matrix[initial][final] for initial in (0,1)),I(0))
                    if value.hi==0:
                        if value.lo!=0:
                            raise ValueError('Inconsistent structural zero')
                        zero_factors+=1
                    elif value.lo<=0:
                        raise ValueError('Positive local count support unresolved at this precision')
                    else:
                        local_spread=max(local_spread,(I(value.hi)/I(value.lo)).hi)
                    lower.append(F(value.lo))
            integers,denominator=integerize(lower)
            factors.append([integers[2*k:2*k+2] for k in range(total+1)])
            denominators.append(denominator)
            term_spread=term_spread*I(local_spread)
        numerical_spread=max(numerical_spread,term_spread.hi)
        normalizer=coefficient_integer([[a+b for a,b in factor] for factor in factors],total)
        if normalizer<=0:
            raise ValueError('Observed total count has zero lower-mixture mass')
        masses.append(weight*F(normalizer,prod(denominators)))
        all_factors.append(factors); all_denominators.append(denominators)
        component_normalizers.append(normalizer)
    record_mass=sum(masses,F(0))
    if not 0<record_mass<=1:
        raise ValueError('Invalid retained total-count record mass')
    posterior_weights=[mass/record_mass for mass in masses]
    assert sum(posterior_weights,F(0))==1
    interface=CountInterface(modules,total,F(duration),posterior_weights,all_factors,
        component_normalizers,all_denominators,list(weights),record_mass,
        F(entrance_spread),F(numerical_spread))
    information={'largest_local_counter_states':2*(total+1),
        'local_increment_operators':len(modules)*(total+1),
        'largest_local_uniformization_tail_upper':str(I(tail).hi),
        'structural_zero_local_factors':zero_factors,
        'bond_dimension_per_mixture_component':total+1,
        'allocations_or_product_configurations_enumerated':False}
    return interface,information


def save_interface(interface,path,source_file=None):
    data={
        'scientific_object':'positive counter tensor-train posterior for an unresolved total turnover count',
        'new_work':True,
        'source_entrance_file':source_file,
        'source_parameters':{'modules':[{'alpha':str(m.alpha),'beta':str(m.beta),'kappa':str(m.kappa)} for m in interface.modules]},
        'observation':{'duration':str(interface.duration),'total_turnovers':interface.total,
                       'per_site_counts_and_event_times_unobserved':True},
        'known_controller_state':1,
        'physical_local_output_indices':['site_turnover_count','final_binary_state'],
        'counter_boundary_indices':[0,interface.total],
        'counter_transition':'a to b=a+k with stored coefficient at local increment k and final state x; all other entries exactly zero',
        'bond_dimension_per_mixture_component':interface.total+1,
        'component_law':'1{sum_i k_i=K} product_i integer_factor[r][i][k_i][x_i] / component_normalizer[r]',
        'exact_rational_mixture_weights':[str(w) for w in interface.weights],
        'local_increment_output_integer_factors':[[[[str(x) for x in row] for row in factor] for factor in component] for component in interface.factors],
        'component_normalizers_integer':[str(x) for x in interface.component_normalizers],
        'local_factor_denominators_exact':[[str(x) for x in row] for row in interface.factor_denominators],
        'input_exact_rational_mixture_weights':[str(w) for w in interface.input_weights],
        'unnormalized_lower_record_mass_exact':str(interface.record_mass),
        'normalization_checked_exactly':True,
        'entrance_projective_spread_upper_exact':str(interface.entrance_spread),
        'local_operator_numerical_spread_upper_exact':str(interface.numerical_spread),
        'posterior_projective_spread_upper_exact':str(interface.spread),
        'whole_joint_count_and_state_posterior_TV_upper':str(tv_from_spread(interface.spread)),
        'certificate_scope':'joint hidden site-count allocation and final leaf state conditional on this total count; same exact later positive operations preserve spread; later numerical approximation needs its own enclosure',
        'representation_scope':'one total-count window; additional unresolved global counts can increase the carry dimensions; mixture labels are representation indices'
    }
    Path(path).write_text(json.dumps(data,separators=(',',':')))


def load_interface(path,verify_normalization=True):
    """Load and evaluate the mathematical law without acquisition or filtering."""
    data=json.loads(Path(path).read_text())
    if data['scientific_object']!='positive counter tensor-train posterior for an unresolved total turnover count':
        raise ValueError('Unsupported retained object')
    modules=[BinaryModule(*(F(m[k]) for k in ('alpha','beta','kappa'))) for m in data['source_parameters']['modules']]
    if not modules or any(min(m.alpha,m.beta,m.kappa)<=0 for m in modules):
        raise ValueError('Positive local rates are required')
    observation=data['observation']; total=observation['total_turnovers']; duration=F(observation['duration'])
    if type(total) is not int or total<0 or duration<=0 or data['known_controller_state']!=1:
        raise ValueError('Invalid count observation or controller state')
    if data['counter_boundary_indices']!=[0,total] or data['bond_dimension_per_mixture_component']!=total+1:
        raise ValueError('Invalid counter boundary or dimension')
    weights=list(map(F,data['exact_rational_mixture_weights']))
    initial=list(map(F,data['input_exact_rational_mixture_weights']))
    factors=[[[list(map(int,row)) for row in factor] for factor in component]
             for component in data['local_increment_output_integer_factors']]
    normalizers=list(map(int,data['component_normalizers_integer']))
    denominators=[list(map(int,row)) for row in data['local_factor_denominators_exact']]
    size=len(weights); n=len(modules)
    if not size or any(len(x)!=size for x in (initial,factors,normalizers,denominators)):
        raise ValueError('Invalid mixture dimensions')
    if any(w<0 for w in weights+initial) or sum(weights,F(0))!=1 or sum(initial,F(0))!=1:
        raise ValueError('Mixture weights are not exactly normalized')
    for component,normalizer,scales in zip(factors,normalizers,denominators):
        if len(component)!=n or len(scales)!=n or normalizer<=0 or min(scales)<=0:
            raise ValueError('Invalid local factor dimensions or scale')
        if any(len(factor)!=total+1 or any(len(row)!=2 or min(row)<0 for row in factor) for factor in component):
            raise ValueError('Invalid nonnegative local factor')
        if verify_normalization:
            mass=coefficient_integer([[sum(row) for row in factor] for factor in component],total)
            if mass!=normalizer:
                raise ValueError('Stored component normalizer is incorrect')
    record_mass=F(data['unnormalized_lower_record_mass_exact'])
    if not 0<record_mass<=1:
        raise ValueError('Invalid record mass')
    for w,w0,normalizer,scales in zip(weights,initial,normalizers,denominators):
        if w!=w0*F(normalizer,prod(scales))/record_mass:
            raise ValueError('Mixture weight and retained record mass disagree')
    entrance=F(data['entrance_projective_spread_upper_exact'])
    numerical=F(data['local_operator_numerical_spread_upper_exact'])
    if min(entrance,numerical)<1 or entrance*numerical!=F(data['posterior_projective_spread_upper_exact']):
        raise ValueError('Inconsistent projective certificate')
    error=F(data['whole_joint_count_and_state_posterior_TV_upper'])
    if not 0<=error<1 or entrance*numerical>((1+error)/(1-error))**2:
        raise ValueError('Reported TV bound does not cover the retained spread')
    return CountInterface(modules,total,duration,weights,factors,normalizers,denominators,
                          initial,record_mass,entrance,numerical)


def product_query_exact(interface,local_tests=None):
    """Expectation of a product of supplied rational local tests f_i(k,x).

    Unspecified local tests are one.  Nonnegative tests need not be indicator
    functions; certificate interpretation must respect the queried range.
    No count allocation or physical product state is enumerated.
    """
    tests={} if local_tests is None else local_tests
    n=len(interface.modules); total=interface.total
    if any(type(i) is not int or not 0<=i<n for i in tests):
        raise ValueError('Invalid local test index')
    for test in tests.values():
        if len(test)!=total+1 or any(len(row)!=2 or any(F(x)<0 for x in row) for row in test):
            raise ValueError('Expected a nonnegative rational test on local (count,state)')
    answer=F(0)
    for weight,component,normalizer in zip(interface.weights,interface.factors,interface.component_normalizers):
        polynomials=[]; extra_denominator=1
        for i,factor in enumerate(component):
            if i not in tests:
                polynomials.append([sum(row) for row in factor])
            else:
                values=[sum(F(row[x])*F(tests[i][k][x]) for x in (0,1)) for k,row in enumerate(factor)]
                integers,scale=integerize(values)
                polynomials.append(integers); extra_denominator*=scale
        numerator=coefficient_integer(polynomials,total)
        answer+=weight*F(numerator,normalizer*extra_denominator)
    return answer


def future_all_active(interface,lag):
    """Interval contraction after continued local turnover, preserving bonds."""
    if lag<=0:
        raise ValueError('Use the exact product query for zero elapsed time')
    transitions=[]
    for module in interface.modules:
        rate=module.alpha+module.beta+module.kappa
        stationary=I(module.alpha/rate); decay=(-I(rate*lag)).exp()
        transitions.append((stationary*(1-decay),stationary+(1-stationary)*decay))
    answer=I(0)
    for weight,component,normalizer in zip(interface.weights,interface.factors,interface.component_normalizers):
        polynomials=[]
        for factor,(p01,p11) in zip(component,transitions):
            polynomials.append([I(row[0])*p01+I(row[1])*p11 for row in factor])
        numerator=coefficient_interval(polynomials,interface.total)
        answer=answer+I(weight)*numerator/I(normalizer)
    return answer


def probability_certificate(approximate,spread):
    q=I(approximate)
    if not 0<=q.lo<=q.hi<=1:
        raise ValueError('An event-probability enclosure in [0,1] is required')
    lower=I(q.lo)/(I(q.lo)+I(spread)*(1-I(q.lo)))
    upper=I(spread)*I(q.hi)/(1-I(q.hi)+I(spread)*I(q.hi))
    result={'approximate_probability_interval':[str(q.lo),str(q.hi)],
            'true_probability_interval':[str(lower.lo),str(upper.hi)]}
    if lower.lo>0:
        result['certified_upper_over_lower_minus_one']=str((I(upper.hi)/I(lower.lo)-1).hi)
    return result


def queries(interface):
    total=interface.total; n=len(interface.modules)
    active=[[F(0),F(1)] for _ in range(total+1)]
    contributed=[[F(int(k>0)),F(int(k>0))] for k in range(total+1)]
    marginal=product_query_exact(interface,{0:active})
    attribution=product_query_exact(interface,{0:contributed})
    all_active=product_query_exact(interface,{i:active for i in range(n)})
    future=future_all_active(interface,F(1,10))
    return {'site_0_active_after_window':probability_certificate(marginal,interface.spread),
            'site_0_contributed_at_least_one_of_observed_turnovers':probability_certificate(attribution,interface.spread),
            'all_sites_active_after_window':probability_certificate(all_active,interface.spread),
            'all_sites_active_after_additional_time_1_10':probability_certificate(future,interface.spread),
            'future_dynamics':'original local turnover continues; no additional count conditioning or cooperative reaction is applied',
            'rare_guard_interpretation':'all-active probability is also instantaneous hazard divided by rate for an AND probe introduced at the query time'}


def small_expanded_check():
    """Independent full killed-counter propagation of a three-leaf source."""
    modules=[BinaryModule(F(3,5)+F(i,100),F(2,5)+F(i%5,50),F(3,2)+F(i%3,10)) for i in range(3)]
    weights=[F(1,3),F(2,3)]; probabilities=[[F(0),F(1,3),F(2,3)],[F(3,5),F(1,4),F(4,5)]]
    duration=F(1,2); total=2
    interface,_=compile_interface(modules,weights,probabilities,duration,total)
    configurations=list(itertools.product((0,1),repeat=3))
    states=[(count,x) for count in range(total+1) for x in configurations]
    index={state:i for i,state in enumerate(states)}; size=len(states)
    Q=[[F(0) for _ in states] for _ in states]; initial=[F(0) for _ in states]
    for row,(count,x) in enumerate(states):
        if count==0:
            initial[row]=sum(w*prod(p if bit else 1-p for bit,p in zip(x,ps)) for w,ps in zip(weights,probabilities))
        overflow=F(0)
        for i,module in enumerate(modules):
            flipped=list(x); flipped[i]=1-flipped[i]
            Q[row][index[(count,tuple(flipped))]]+=module.alpha if x[i]==0 else module.beta
            if x[i]:
                if count<total:
                    Q[row][index[(count+1,tuple(flipped))]]+=module.kappa
                else:
                    overflow+=module.kappa
        Q[row][row]=-sum(Q[row])-overflow
    rate=max(-Q[i][i] for i in range(size)); z=rate*duration
    transition=[[(j,F(int(i==j))+q/rate) for j,q in enumerate(row) if F(int(i==j))+q/rate]
                for i,row in enumerate(Q)]
    exponential=(-I(z)).exp(); vector=initial[:]; accumulated=initial[:]; term=F(1); order=0
    while True:
        first=term*z/(order+1)
        if order+2>z:
            tail=F(exponential.hi)*first/(1-z/(order+2))
            if tail<F(1,10**60):
                break
        order+=1; term*=z/order; updated=[F(0) for _ in states]
        for i,row in enumerate(transition):
            for j,p in row:
                updated[j]+=vector[i]*p
        vector=updated; accumulated=[a+term*v for a,v in zip(accumulated,vector)]
        if order>1000:
            raise RuntimeError('Independent reference series budget exceeded')
    contained=0
    for x in configurations:
        tests={i:[[F(int(state==bit)) for state in (0,1)] for _ in range(total+1)] for i,bit in enumerate(x)}
        lower=interface.record_mass*product_query_exact(interface,tests)
        upper=lower*interface.numerical_spread
        partial=accumulated[index[(total,x)]]
        reference_lo=F(exponential.lo)*partial
        reference_hi=F(exponential.hi)*partial+tail
        if upper<reference_lo or reference_hi<lower:
            raise AssertionError('Counter tensor-train and expanded generator enclosures are disjoint')
        contained+=int(lower<=reference_lo and reference_hi<=upper)
    return {'leaves':3,'observed_total_count':total,'expanded_counter_states':size,
            'uniformization_terms':order+1,'poisson_tail_upper':str(I(tail).hi),
            'final_state_coordinates_checked':len(configurations),
            'all_independent_coordinate_enclosures_overlap_TT_bounds':True,
            'independent_coordinate_enclosures_fully_inside_TT_bounds':contained,
            'role':'independent indexing/counter-direction check; source certificate comes from local positive operator enclosures'}


def run(total=8,duration=F(1,2)):
    started=time.perf_counter(); source=Path('relative_correlated_entrance_24sites.json')
    source_data=json.loads(source.read_text())
    modules,weights,probabilities,_=load_acquired_action(source)
    entrance=F(source_data['relative_projective_certificate']['spread_factor_upper_exact'])
    interface,information=compile_interface(modules,weights,probabilities,duration,total,entrance)
    path=Path('unresolved_count_posterior_24sites.json')
    save_interface(interface,path,str(source))
    # The executed queries consume the serialized object, including its exact
    # integer normalizers, not an unretained transient approximation.
    retained=load_interface(path)
    assert retained.record_mass==interface.record_mass and retained.weights==interface.weights
    output={'new_work':True,'source_acquisition_or_earlier_filter_recomputed':False,
        'source_modules':len(modules),'initial_positive_product_components':len(weights),
        'observation_duration':str(duration),'observed_total_turnovers':total,
        'count_allocation_observed':False,'retained_interface_file':str(path),
        'retained_mixture_components':len(retained.weights),
        'record_probability_interval':[str(I(retained.record_mass/entrance).lo),
                                       str(I(retained.record_mass*entrance*retained.numerical_spread).hi)],
        'whole_joint_count_and_state_posterior_TV_upper':str(tv_from_spread(retained.spread)),
        'later_local_numerical_spread_minus_one_upper':str(I(retained.numerical_spread-1).hi),
        'loader_checked_exact_integer_normalizers_and_rational_weights':True,
        'construction':information,'queries_from_retained_object':queries(retained),
        'independent_small_check':small_expanded_check(),
        'elapsed_seconds':time.perf_counter()-started,
        'scope':'one unresolved total-count window; positive count-accumulator tensor structure and source-derived certificate; no bounded width claim for repeated unresolved global records'}
    Path('unresolved_count_interface_results.json').write_text(json.dumps(output,indent=2))
    return output


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
